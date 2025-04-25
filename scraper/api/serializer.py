from rest_framework import serializers


class URLArraySerializer(serializers.Serializer):
    # A list of URLs
    urls = serializers.ListField(
        child=serializers.URLField(),  # Each element inside the list must be a valid URL
        allow_empty=False,             # Optionally, you can disable empty lists
    )
