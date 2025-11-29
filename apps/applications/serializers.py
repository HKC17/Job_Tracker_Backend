from rest_framework import serializers
from datetime import datetime


class CompanySerializer(serializers.Serializer):
    """Serializer for company information."""
    name = serializers.CharField(max_length=200)
    website = serializers.URLField(required=False, allow_blank=True)
    industry = serializers.CharField(
        max_length=100, required=False, allow_blank=True)
    size = serializers.CharField(
        max_length=50, required=False, allow_blank=True)
    location = serializers.CharField(
        max_length=200, required=False, allow_blank=True)
    logo_url = serializers.URLField(required=False, allow_blank=True)


class JobSerializer(serializers.Serializer):
    """Serializer for job information."""
    title = serializers.CharField(max_length=200)
    description = serializers.CharField(required=False, allow_blank=True)
    job_url = serializers.URLField(required=False, allow_blank=True)
    employment_type = serializers.CharField(
        max_length=50, required=False, allow_blank=True)
    work_mode = serializers.CharField(
        max_length=50, required=False, allow_blank=True)
    experience_level = serializers.CharField(
        max_length=50, required=False, allow_blank=True)
    salary_min = serializers.IntegerField(required=False, allow_null=True)
    salary_max = serializers.IntegerField(required=False, allow_null=True)
    currency = serializers.CharField(max_length=10, default='USD')


class ApplicationInfoSerializer(serializers.Serializer):
    """Serializer for application status information."""
    applied_date = serializers.DateTimeField(default=datetime.utcnow)
    source = serializers.CharField(
        max_length=100, required=False, allow_blank=True)
    status = serializers.CharField(max_length=50, default='applied')
    resume_version = serializers.CharField(
        max_length=200, required=False, allow_blank=True)
    cover_letter = serializers.CharField(required=False, allow_blank=True)
    referral_name = serializers.CharField(
        max_length=200, required=False, allow_blank=True)


class RequirementsSerializer(serializers.Serializer):
    """Serializer for job requirements."""
    skills_required = serializers.ListField(
        child=serializers.CharField(), default=list)
    skills_preferred = serializers.ListField(
        child=serializers.CharField(), default=list)
    years_experience = serializers.FloatField(required=False, allow_null=True)
    education = serializers.CharField(
        max_length=200, required=False, allow_blank=True)


class TimelineEventSerializer(serializers.Serializer):
    """Serializer for timeline events."""
    date = serializers.DateTimeField(default=datetime.utcnow)
    event_type = serializers.CharField(max_length=50)
    title = serializers.CharField(max_length=200)
    notes = serializers.CharField(required=False, allow_blank=True)
    interviewer_name = serializers.CharField(
        max_length=200, required=False, allow_blank=True)
    interview_type = serializers.CharField(
        max_length=50, required=False, allow_blank=True)


class AttachmentSerializer(serializers.Serializer):
    """Serializer for file attachments."""
    filename = serializers.CharField(max_length=255)
    file_url = serializers.CharField(max_length=500)
    uploaded_at = serializers.DateTimeField(default=datetime.utcnow)
    file_type = serializers.CharField(
        max_length=50, required=False, allow_blank=True)


class ApplicationSerializer(serializers.Serializer):
    """Main serializer for job applications."""
    id = serializers.CharField(source='_id', read_only=True)
    user_id = serializers.IntegerField(read_only=True)
    company = CompanySerializer()
    job = JobSerializer()
    application = ApplicationInfoSerializer()
    requirements = RequirementsSerializer(required=False)
    timeline = TimelineEventSerializer(many=True, required=False, default=list)
    attachments = AttachmentSerializer(many=True, required=False, default=list)
    notes = serializers.CharField(required=False, allow_blank=True)
    is_favorite = serializers.BooleanField(default=False)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    def to_representation(self, instance):
        """Convert ObjectId to string for JSON serialization."""
        rep = super().to_representation(instance)
        if '_id' in instance:
            rep['id'] = str(instance['_id'])
        return rep


class ApplicationCreateSerializer(serializers.Serializer):
    """Serializer for creating applications."""
    company = CompanySerializer()
    job = JobSerializer()
    application = ApplicationInfoSerializer(required=False)
    requirements = RequirementsSerializer(required=False)
    notes = serializers.CharField(required=False, allow_blank=True)
    is_favorite = serializers.BooleanField(default=False)


class ApplicationUpdateSerializer(serializers.Serializer):
    """Serializer for updating applications."""
    company = CompanySerializer(required=False)
    job = JobSerializer(required=False)
    application = ApplicationInfoSerializer(required=False)
    requirements = RequirementsSerializer(required=False)
    notes = serializers.CharField(required=False, allow_blank=True)
    is_favorite = serializers.BooleanField(required=False)


class StatusUpdateSerializer(serializers.Serializer):
    """Serializer for updating application status."""
    status = serializers.CharField(max_length=50, required=True)
    notes = serializers.CharField(required=False, allow_blank=True)

    def validate_status(self, value):
        """Validate status is one of allowed values."""
        allowed_statuses = [
            'applied', 'screening', 'interview', 'technical_test',
            'offer', 'rejected', 'accepted', 'withdrawn'
        ]
        if value not in allowed_statuses:
            raise serializers.ValidationError(
                f"Status must be one of: {', '.join(allowed_statuses)}"
            )
        return value


class ApplicationStatisticsSerializer(serializers.Serializer):
    """Serializer for application statistics."""
    total_applications = serializers.IntegerField()
    status_breakdown = serializers.DictField()
