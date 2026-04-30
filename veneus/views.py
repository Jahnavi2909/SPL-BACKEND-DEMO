from rest_framework import generics
from .models import Venue
from .serializers import VenueSerializer
from .permissions import IsAdminOrReadOnly
 
 

class VenueListCreateView(generics.ListCreateAPIView):
    queryset = Venue.objects.all()
    serializer_class = VenueSerializer
    permission_classes = [IsAdminOrReadOnly]
 
 

class VenueDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Venue.objects.all()
    serializer_class = VenueSerializer
    permission_classes = [IsAdminOrReadOnly]
 
from rest_framework import generics
from .models import Sponsor
from .serializers import SponsorSerializer
from .permissions import IsAdminOrReadOnly
 
 

class SponsorListCreateView(generics.ListCreateAPIView):
    queryset = Sponsor.objects.all()
    serializer_class = SponsorSerializer
    permission_classes = [IsAdminOrReadOnly]
 
 

class SponsorDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Sponsor.objects.all()
    serializer_class = SponsorSerializer
    permission_classes = [IsAdminOrReadOnly]
 