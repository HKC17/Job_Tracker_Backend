from rest_framework import serializers


class ContactInfoSerializer(serializers.Serializer):
    """Serializer for contact information."""
    recruiter_name = serializers.CharField(
        max_length=200, required=False, allow_blank=True)
    recruiter_email = serializers.EmailField(required=False, allow_blank=True)
    recruiter_phone = serializers.CharField(
        max_length=20, required=False, allow_blank=True)
    hr_contact = serializers.CharField(
        max_length=200, required=False, allow_blank=True)


class CompanySerializer(serializers.Serializer):
    """Main serializer for companies."""
    id = serializers.CharField(source='_id', read_only=True)
    user_id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=200)
    website = serializers.URLField(required=False, allow_blank=True)
    industry = serializers.CharField(
        max_length=100, required=False, allow_blank=True)
    size = serializers.CharField(
        max_length=50, required=False, allow_blank=True)
    location = serializers.CharField(
        max_length=200, required=False, allow_blank=True)
    logo_url = serializers.URLField(required=False, allow_blank=True)
    description = serializers.CharField(required=False, allow_blank=True)
    glassdoor_rating = serializers.FloatField(required=False, allow_null=True)
    notes = serializers.CharField(required=False, allow_blank=True)
    is_favorite = serializers.BooleanField(default=False)
    tags = serializers.ListField(child=serializers.CharField(), default=list)
    contact_info = ContactInfoSerializer(required=False)
    application_count = serializers.IntegerField(
        read_only=True, required=False)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    def to_representation(self, instance):
        """Convert ObjectId to string for JSON serialization."""
        rep = super().to_representation(instance)
        if '_id' in instance:
            rep['id'] = str(instance['_id'])
        return rep


class CompanyCreateSerializer(serializers.Serializer):
    """Serializer for creating companies."""
    name = serializers.CharField(max_length=200)
    website = serializers.URLField(required=False, allow_blank=True)
    industry = serializers.CharField(
        max_length=100, required=False, allow_blank=True)
    size = serializers.CharField(
        max_length=50, required=False, allow_blank=True)
    location = serializers.CharField(
        max_length=200, required=False, allow_blank=True)
    logo_url = serializers.URLField(required=False, allow_blank=True)
    description = serializers.CharField(required=False, allow_blank=True)
    glassdoor_rating = serializers.FloatField(required=False, allow_null=True)
    notes = serializers.CharField(required=False, allow_blank=True)
    is_favorite = serializers.BooleanField(default=False)
    tags = serializers.ListField(child=serializers.CharField(), default=list)
    contact_info = ContactInfoSerializer(required=False)


class CompanyUpdateSerializer(serializers.Serializer):
    """Serializer for updating companies."""
    name = serializers.CharField(max_length=200, required=False)
    website = serializers.URLField(required=False, allow_blank=True)
    industry = serializers.CharField(
        max_length=100, required=False, allow_blank=True)
    size = serializers.CharField(
        max_length=50, required=False, allow_blank=True)
    location = serializers.CharField(
        max_length=200, required=False, allow_blank=True)
    logo_url = serializers.URLField(required=False, allow_blank=True)
    description = serializers.CharField(required=False, allow_blank=True)
    glassdoor_rating = serializers.FloatField(required=False, allow_null=True)
    notes = serializers.CharField(required=False, allow_blank=True)
    is_favorite = serializers.BooleanField(required=False)
    tags = serializers.ListField(child=serializers.CharField(), required=False)
    contact_info = ContactInfoSerializer(required=False)


class CompanyStatsSerializer(serializers.Serializer):
    """Serializer for company statistics."""
    company = CompanySerializer()
    total_applications = serializers.IntegerField()
    status_breakdown = serializers.DictField()
    average_response_time = serializers.FloatField()


class IndustryBreakdownSerializer(serializers.Serializer):
    """Serializer for industry breakdown."""
    industry = serializers.CharField()
    count = serializers.IntegerField()
