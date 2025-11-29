from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from bson.errors import InvalidId

from .services import CompanyService
from .serializers import (
    CompanySerializer,
    CompanyCreateSerializer,
    CompanyUpdateSerializer,
    CompanyStatsSerializer,
    IndustryBreakdownSerializer
)


class CompanyListCreateView(APIView):
    """
    GET  /api/companies/  - List all companies
    POST /api/companies/  - Create new company
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """List all companies for current user."""
        service = CompanyService()

        # Get query parameters
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 20))
        skip = (page - 1) * page_size

        # Filters
        filters = {}
        if request.GET.get('industry'):
            filters['industry'] = request.GET.get('industry')
        if request.GET.get('location'):
            filters['location'] = request.GET.get('location')
        if request.GET.get('is_favorite'):
            filters['is_favorite'] = request.GET.get(
                'is_favorite').lower() == 'true'
        if request.GET.get('tags'):
            filters['tags'] = request.GET.get('tags').split(',')

        result = service.get_companies(
            user_id=request.user.id,
            filters=filters,
            skip=skip,
            limit=page_size
        )

        serializer = CompanySerializer(result['companies'], many=True)

        return Response({
            'count': result['total'],
            'next': page + 1 if skip + page_size < result['total'] else None,
            'previous': page - 1 if page > 1 else None,
            'results': serializer.data
        })

    def post(self, request):
        """Create a new company."""
        serializer = CompanyCreateSerializer(data=request.data)

        if serializer.is_valid():
            service = CompanyService()

            # Check if company already exists
            existing = service.get_company_by_name(
                serializer.validated_data['name'],
                request.user.id
            )

            if existing:
                return Response(
                    {'error': 'Company with this name already exists'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            company = service.create_company(
                user_id=request.user.id,
                data=serializer.validated_data
            )

            response_serializer = CompanySerializer(company)
            return Response(
                response_serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CompanyDetailView(APIView):
    """
    GET    /api/companies/{id}/  - Get company details
    PUT    /api/companies/{id}/  - Update company
    DELETE /api/companies/{id}/  - Delete company
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        """Get company by ID."""
        try:
            service = CompanyService()
            company = service.get_company(pk, request.user.id)

            if not company:
                return Response(
                    {'error': 'Company not found'},
                    status=status.HTTP_404_NOT_FOUND
                )

            # Add application count
            app_count = service.applications_collection.count_documents({
                'user_id': request.user.id,
                'company.name': company['name']
            })
            company['application_count'] = app_count

            serializer = CompanySerializer(company)
            return Response(serializer.data)

        except InvalidId:
            return Response(
                {'error': 'Invalid company ID'},
                status=status.HTTP_400_BAD_REQUEST
            )

    def put(self, request, pk):
        """Update company."""
        try:
            serializer = CompanyUpdateSerializer(data=request.data)

            if serializer.is_valid():
                service = CompanyService()
                company = service.update_company(
                    pk,
                    request.user.id,
                    serializer.validated_data
                )

                if not company:
                    return Response(
                        {'error': 'Company not found'},
                        status=status.HTTP_404_NOT_FOUND
                    )

                response_serializer = CompanySerializer(company)
                return Response(response_serializer.data)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except InvalidId:
            return Response(
                {'error': 'Invalid company ID'},
                status=status.HTTP_400_BAD_REQUEST
            )

    def delete(self, request, pk):
        """Delete company."""
        try:
            service = CompanyService()
            deleted = service.delete_company(pk, request.user.id)

            if deleted:
                return Response(
                    {'message': 'Company deleted successfully'},
                    status=status.HTTP_204_NO_CONTENT
                )

            return Response(
                {'error': 'Company not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        except InvalidId:
            return Response(
                {'error': 'Invalid company ID'},
                status=status.HTTP_400_BAD_REQUEST
            )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_companies(request):
    """
    GET /api/companies/search/?q=term
    Search companies by name, industry, or location.
    """
    search_term = request.GET.get('q', '')

    if not search_term:
        return Response(
            {'error': 'Search term is required'},
            status=status.HTTP_400_BAD_REQUEST
        )

    service = CompanyService()
    companies = service.search_companies(request.user.id, search_term)

    serializer = CompanySerializer(companies, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def autocomplete_companies(request):
    """
    GET /api/companies/autocomplete/?q=prefix
    Autocomplete company names.
    """
    prefix = request.GET.get('q', '')

    if not prefix:
        return Response([], status=status.HTTP_200_OK)

    limit = int(request.GET.get('limit', 10))

    service = CompanyService()
    companies = service.autocomplete(request.user.id, prefix, limit)

    # Return simplified format for autocomplete
    results = [
        {
            'id': str(company['_id']),
            'name': company['name'],
            'industry': company.get('industry', ''),
            'location': company.get('location', '')
        }
        for company in companies
    ]

    return Response(results)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def company_applications(request, pk):
    """
    GET /api/companies/{id}/applications/
    Get all applications for a specific company.
    """
    try:
        service = CompanyService()
        result = service.get_company_applications(pk, request.user.id)

        if not result:
            return Response(
                {'error': 'Company not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        from apps.applications.serializers import ApplicationSerializer

        company_serializer = CompanySerializer(result['company'])
        applications_serializer = ApplicationSerializer(
            result['applications'], many=True)

        return Response({
            'company': company_serializer.data,
            'applications': applications_serializer.data
        })

    except InvalidId:
        return Response(
            {'error': 'Invalid company ID'},
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def company_stats(request, pk):
    """
    GET /api/companies/{id}/stats/
    Get statistics for a specific company.
    """
    try:
        service = CompanyService()
        stats = service.get_company_stats(pk, request.user.id)

        if not stats:
            return Response(
                {'error': 'Company not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = CompanyStatsSerializer(stats)
        return Response(serializer.data)

    except InvalidId:
        return Response(
            {'error': 'Invalid company ID'},
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def sync_companies(request):
    """
    POST /api/companies/sync/
    Sync companies from existing applications.
    """
    service = CompanyService()
    created_count = service.sync_companies_from_applications(request.user.id)

    return Response({
        'message': f'Successfully synced {created_count} companies',
        'created_count': created_count
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def industry_breakdown(request):
    """
    GET /api/companies/industry-breakdown/
    Get breakdown of companies by industry.
    """
    service = CompanyService()
    data = service.get_industry_breakdown(request.user.id)

    serializer = IndustryBreakdownSerializer(data, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def top_companies(request):
    """
    GET /api/companies/top/
    Get companies with most applications.
    """
    limit = int(request.GET.get('limit', 10))

    service = CompanyService()
    data = service.get_top_companies_by_applications(request.user.id, limit)

    results = []
    for item in data:
        company_data = CompanySerializer(item['company']).data
        company_data['application_count'] = item['application_count']
        results.append(company_data)

    return Response(results)
