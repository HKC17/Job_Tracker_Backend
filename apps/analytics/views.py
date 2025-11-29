from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .services import AnalyticsService
from .serializers import (
    DashboardStatsSerializer,
    TimeSeriesDataSerializer,
    SuccessRateSerializer,
    SkillDemandSerializer,
    TimelineAnalysisSerializer,
    SalaryInsightsSerializer,
    ResponseTimeSerializer
)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_stats(request):
    """
    GET /api/analytics/dashboard/
    Get comprehensive dashboard statistics.
    """
    service = AnalyticsService()
    stats = service.get_dashboard_stats(request.user.id)

    serializer = DashboardStatsSerializer(stats)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def applications_over_time(request):
    """
    GET /api/analytics/applications-over-time/?period=month
    Get application counts over time.
    Parameters:
    - period: 'day', 'week', or 'month' (default: month)
    """
    period = request.GET.get('period', 'month')

    if period not in ['day', 'week', 'month']:
        return Response(
            {'error': 'Invalid period. Must be day, week, or month.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    service = AnalyticsService()
    data = service.get_applications_over_time(request.user.id, period)

    serializer = TimeSeriesDataSerializer(data, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def success_rate_over_time(request):
    """
    GET /api/analytics/success-rate/
    Get success rate over time (by month).
    """
    service = AnalyticsService()
    data = service.get_success_rate_over_time(request.user.id)

    serializer = SuccessRateSerializer(data, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def skills_demand(request):
    """
    GET /api/analytics/skills/
    Get most demanded skills from job postings.
    """
    service = AnalyticsService()
    data = service.get_skills_demand(request.user.id)

    serializer = SkillDemandSerializer(data, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def timeline_analysis(request):
    """
    GET /api/analytics/timeline/
    Analyze interview stages and events.
    """
    service = AnalyticsService()
    data = service.get_application_timeline_analysis(request.user.id)

    serializer = TimelineAnalysisSerializer(data, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def salary_insights(request):
    """
    GET /api/analytics/salary/
    Get salary statistics and insights.
    """
    service = AnalyticsService()
    data = service.get_salary_insights(request.user.id)

    serializer = SalaryInsightsSerializer(data)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def response_time_analysis(request):
    """
    GET /api/analytics/response-time/
    Analyze how long companies take to respond.
    """
    service = AnalyticsService()
    data = service.get_response_time_analysis(request.user.id)

    serializer = ResponseTimeSerializer(data)
    return Response(serializer.data)
