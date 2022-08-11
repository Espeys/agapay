from rest_framework import serializers


class ErrorSerializer(serializers.Serializer):
    code = serializers.IntegerField()
    message = serializers.CharField()
    field = serializers.CharField()


class GenericSerializer(serializers.Serializer):
    success = serializers.BooleanField()
    errors = serializers.ListField(ErrorSerializer)
    data = serializers.JSONField()


class PaginatedObject(serializers.Serializer):
    count_per_page = serializers.IntegerField()
    start_page = serializers.IntegerField()
    page = serializers.IntegerField()
    last_page = serializers.IntegerField()
    total_pages = serializers.IntegerField()
    start_index = serializers.IntegerField()
    last_index = serializers.IntegerField()
    total_count = serializers.IntegerField()
    total_results = serializers.IntegerField()
    items = serializers.JSONField()