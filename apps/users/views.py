from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes

from .serializers import (
    UserSerializer,
    UserRegistrationSerializer,
    UserUpdateSerializer,
    ChangePasswordSerializer,
    CustomTokenObtainPairSerializer,
    SkillSerializer
)

User = get_user_model()


class UserRegistrationView(generics.CreateAPIView):
    """
    POST /api/auth/register/
    Register a new user.
    """
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Generate tokens for the new user
        refresh = RefreshToken.for_user(user)

        return Response({
            'user': UserSerializer(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            },
            'message': 'User registered successfully'
        }, status=status.HTTP_201_CREATED)


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    POST /api/auth/login/
    Login with email and password, returns JWT tokens and user data.
    """
    serializer_class = CustomTokenObtainPairSerializer


class UserDetailView(generics.RetrieveUpdateAPIView):
    """
    GET /api/auth/user/
    PUT /api/auth/user/
    Get or update current user profile.
    """
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return UserUpdateSerializer
        return UserSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        # Return updated user data with full serializer
        return Response(
            UserSerializer(instance).data,
            status=status.HTTP_200_OK
        )


class ChangePasswordView(APIView):
    """
    POST /api/auth/change-password/
    Change user password.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(
            data=request.data,
            context={'request': request}
        )

        if serializer.is_valid():
            user = request.user
            user.set_password(serializer.validated_data['new_password'])
            user.save()

            return Response({
                'message': 'Password changed successfully'
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    """
    POST /api/auth/logout/
    Logout by blacklisting the refresh token.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            if not refresh_token:
                return Response(
                    {'error': 'Refresh token is required'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({
                'message': 'Logout successful'
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class AddSkillView(APIView):
    """
    POST /api/auth/skills/add/
    Add a skill to user's skill list.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = SkillSerializer(data=request.data)

        if serializer.is_valid():
            skill = serializer.validated_data['skill']
            user = request.user

            if skill in user.skills:
                return Response(
                    {'message': 'Skill already exists'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            user.add_skill(skill)

            return Response({
                'message': 'Skill added successfully',
                'skills': user.skills
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RemoveSkillView(APIView):
    """
    POST /api/auth/skills/remove/
    Remove a skill from user's skill list.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = SkillSerializer(data=request.data)

        if serializer.is_valid():
            skill = serializer.validated_data['skill']
            user = request.user

            if skill not in user.skills:
                return Response(
                    {'message': 'Skill not found'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            user.remove_skill(skill)

            return Response({
                'message': 'Skill removed successfully',
                'skills': user.skills
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_stats(request):
    """
    GET /api/auth/stats/
    Get user statistics (applications count, etc.)
    """
    user = request.user

    # Import MongoDB helper
    from config.mongodb import get_collection

    # Get applications collection
    applications_collection = get_collection('applications')

    # Count total applications for user
    total_applications = applications_collection.count_documents(
        {'user_id': user.id})

    # Count by status
    pipeline = [
        {'$match': {'user_id': user.id}},
        {'$group': {
            '_id': '$application.status',
            'count': {'$sum': 1}
        }}
    ]

    status_breakdown = {}
    for result in applications_collection.aggregate(pipeline):
        status_breakdown[result['_id']] = result['count']

    stats = {
        'total_applications': total_applications,
        'status_breakdown': status_breakdown,
        'total_skills': len(user.skills),
        'profile_completion': calculate_profile_completion(user)
    }

    return Response(stats, status=status.HTTP_200_OK)


def calculate_profile_completion(user):
    """Calculate profile completion percentage."""
    fields = [
        user.first_name,
        user.last_name,
        user.email,
        user.skills,
        user.resume_url,
        user.phone,
        user.location,
        user.current_role,
        user.linkedin_url,
    ]

    filled_fields = sum(1 for field in fields if field)
    total_fields = len(fields)

    return round((filled_fields / total_fields) * 100, 2)
