from rest_framework import generics
from django.utils import timezone
from .models import Announcements, News
from .serializers import AnnouncementSerializer, NewsSerializer
from .permissions import IsAdminOrReadOnly
 
  
class AnnouncementListCreateView(generics.ListCreateAPIView):
    serializer_class = AnnouncementSerializer
    permission_classes = [IsAdminOrReadOnly]
 
    def get_queryset(self):
    
        Announcements.objects.filter(expires_at__lte=timezone.now()).delete()
        return Announcements.objects.filter(expires_at__gt=timezone.now())
 
 
class AnnouncementDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AnnouncementSerializer
    permission_classes = [IsAdminOrReadOnly]
 
    def get_queryset(self):
        Announcements.objects.filter(expires_at__lte=timezone.now()).delete()
        return Announcements.objects.filter(expires_at__gt=timezone.now())
 

 
class NewsListCreateView(generics.ListCreateAPIView):
    serializer_class = NewsSerializer
    permission_classes = [IsAdminOrReadOnly]
 
    def get_queryset(self):
        News.objects.filter(expires_at__lte=timezone.now()).delete()
        return News.objects.filter(expires_at__gt=timezone.now())
 
 
class NewsDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = NewsSerializer
    permission_classes = [IsAdminOrReadOnly]
 
    def get_queryset(self):
        News.objects.filter(expires_at__lte=timezone.now()).delete()
        return News.objects.filter(expires_at__gt=timezone.now())
 