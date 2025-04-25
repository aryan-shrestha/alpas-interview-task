from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from scraper.api.serializer import URLArraySerializer
from scraper.utils import extract_data_from_urls

class ScraperAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = URLArraySerializer(data=request.data)

        if serializer.is_valid():
            urls = serializer.validated_data['urls']
            extracted_data = extract_data_from_urls(urls)
            return Response(data=extracted_data, status=status.HTTP_200_OK)
        else:
            # Return validation errors
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
