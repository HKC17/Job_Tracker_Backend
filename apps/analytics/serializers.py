from rest_framework import serializers


class DashboardStatsSerializer(serializers.Serializer):
    """Serializer for dashboard statistics."""
    total_applications = serializers.IntegerField()
    status_breakdown = serializers.DictField()
    success_rate = serializers.FloatField()
    response_rate = serializers.FloatField()
    applications_last_30_days = serializers.IntegerField()
    average_days_in_pipeline = serializers.IntegerField()
    top_companies = serializers.ListField()
    top_sources = serializers.ListField()


class TimeSeriesDataSerializer(serializers.Serializer):
    """Serializer for time series data."""
    period = serializers.CharField()
    count = serializers.IntegerField()


class SuccessRateSerializer(serializers.Serializer):
    """Serializer for success rate over time."""
    period = serializers.CharField()
    success_rate = serializers.FloatField()
    total = serializers.IntegerField()
    success = serializers.IntegerField()


class SkillDemandSerializer(serializers.Serializer):
    """Serializer for skill demand data."""
    skill = serializers.CharField()
    count = serializers.IntegerField()


class TimelineAnalysisSerializer(serializers.Serializer):
    """Serializer for timeline analysis."""
    event_type = serializers.CharField()
    count = serializers.IntegerField()


class SalaryInsightsSerializer(serializers.Serializer):
    """Serializer for salary insights."""
    average_min = serializers.IntegerField()
    average_max = serializers.IntegerField()
    lowest = serializers.IntegerField()
    highest = serializers.IntegerField()
    total_with_salary = serializers.IntegerField()


class ResponseTimeSerializer(serializers.Serializer):
    """Serializer for response time analysis."""
    average_days = serializers.FloatField()
    fastest = serializers.IntegerField()
    slowest = serializers.IntegerField()
    total_responses = serializers.IntegerField()
