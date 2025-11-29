from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from bson.errors import InvalidId

from .services import ApplicationService
from .serializers import (
    ApplicationSerializer,
    ApplicationCreateSerializer,
    ApplicationUpdateSerializer,
    StatusUpdateSerializer,
    TimelineEventSerializer,
    ApplicationStatisticsSerializer
)


class ApplicationListCreateView(APIView):
    """
    GET  /api/applications/  - List all applications
    POST /api/applications/  - Create new application
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """List all applications for current user."""
        service = ApplicationService()

        # Get query parameters
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 20))
        skip = (page - 1) * page_size

        # Filters
        filters = {}
        if request.GET.get('status'):
            filters['status'] = request.GET.get('status')
        if request.GET.get('company'):
            filters['company'] = request.GET.get('company')
        if request.GET.get('job_title'):
            filters['job_title'] = request.GET.get('job_title')
        if request.GET.get('is_favorite'):
            filters['is_favorite'] = request.GET.get(
                'is_favorite').lower() == 'true'

        result = service.get_applications(
            user_id=request.user.id,
            filters=filters,
            skip=skip,
            limit=page_size
        )

        serializer = ApplicationSerializer(result['applications'], many=True)

        return Response({
            'count': result['total'],
            'next': page + 1 if skip + page_size < result['total'] else None,
            'previous': page - 1 if page > 1 else None,
            'results': serializer.data
        })

    def post(self, request):
        """Create a new application."""
        serializer = ApplicationCreateSerializer(data=request.data)

        if serializer.is_valid():
            service = ApplicationService()
            application = service.create_application(
                user_id=request.user.id,
                data=serializer.validated_data
            )

            response_serializer = ApplicationSerializer(application)
            return Response(
                response_serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ApplicationDetailView(APIView):
    """
    GET    /api/applications/{id}/  - Get application details
    PUT    /api/applications/{id}/  - Update application
    DELETE /api/applications/{id}/  - Delete application
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        """Get application by ID."""
        try:
            service = ApplicationService()
            application = service.get_application(pk, request.user.id)

            if not application:
                return Response(
                    {'error': 'Application not found'},
                    status=status.HTTP_404_NOT_FOUND
                )

            serializer = ApplicationSerializer(application)
            return Response(serializer.data)

        except InvalidId:
            return Response(
                {'error': 'Invalid application ID'},
                status=status.HTTP_400_BAD_REQUEST
            )

    def put(self, request, pk):
        """Update application."""
        try:
            serializer = ApplicationUpdateSerializer(data=request.data)

            if serializer.is_valid():
                service = ApplicationService()
                application = service.update_application(
                    pk,
                    request.user.id,
                    serializer.validated_data
                )

                if not application:
                    return Response(
                        {'error': 'Application not found'},
                        status=status.HTTP_404_NOT_FOUND
                    )

                response_serializer = ApplicationSerializer(application)
                return Response(response_serializer.data)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except InvalidId:
            return Response(
                {'error': 'Invalid application ID'},
                status=status.HTTP_400_BAD_REQUEST
            )

    def delete(self, request, pk):
        """Delete application."""
        try:
            service = ApplicationService()
            deleted = service.delete_application(pk, request.user.id)

            if deleted:
                return Response(
                    {'message': 'Application deleted successfully'},
                    status=status.HTTP_204_NO_CONTENT
                )

            return Response(
                {'error': 'Application not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        except InvalidId:
            return Response(
                {'error': 'Invalid application ID'},
                status=status.HTTP_400_BAD_REQUEST
            )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_timeline_event(request, pk):
    """
    POST /api/applications/{id}/timeline/
    Add a timeline event to an application.
    """
    try:
        serializer = TimelineEventSerializer(data=request.data)

        if serializer.is_valid():
            service = ApplicationService()
            success = service.add_timeline_event(
                pk,
                request.user.id,
                serializer.validated_data
            )

            if success:
                return Response(
                    {'message': 'Timeline event added successfully'},
                    status=status.HTTP_201_CREATED
                )

            return Response(
                {'error': 'Application not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except InvalidId:
        return Response(
            {'error': 'Invalid application ID'},
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_status(request, pk):
    """
    PATCH /api/applications/{id}/status/
    Update application status.
    """
    try:
        serializer = StatusUpdateSerializer(data=request.data)

        if serializer.is_valid():
            service = ApplicationService()
            application = service.update_status(
                pk,
                request.user.id,
                serializer.validated_data['status'],
                serializer.validated_data.get('notes')
            )

            if application:
                response_serializer = ApplicationSerializer(application)
                return Response(response_serializer.data)

            return Response(
                {'error': 'Application not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except InvalidId:
        return Response(
            {'error': 'Invalid application ID'},
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def application_statistics(request):
    """
    GET /api/applications/stats/
    Get application statistics for current user.
    """
    service = ApplicationService()
    stats = service.get_statistics(request.user.id)

    serializer = ApplicationStatisticsSerializer(stats)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_applications(request):
    """
    GET /api/applications/search/?q=term
    Search applications by company, job title, or notes.
    """
    search_term = request.GET.get('q', '')

    if not search_term:
        return Response(
            {'error': 'Search term is required'},
            status=status.HTTP_400_BAD_REQUEST
        )

    service = ApplicationService()
    applications = service.search_applications(request.user.id, search_term)

    serializer = ApplicationSerializer(applications, many=True)
    return Response(serializer.data)
