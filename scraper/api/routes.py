from django.urls import path
from scraper.api.views import ScraperAPIView

urlpatterns = [
    path('scrape/', ScraperAPIView.as_view(), name='scrape'),
]