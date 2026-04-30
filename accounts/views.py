from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework.generics import ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny

from .models import Franchise
from .permissions import *
from .serializers import FranchiseSerializer
from .pagination import FranchisePagination

from core.models import Team
from core.serializers import TeamSerializer
from core.pagination import TeamPagination

from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenSerializer


User = get_user_model()


# ✅ CREATE FRANCHISE
class CreateFranchiseView(APIView):
    permission_classes = [IsAdmin]

    @transaction.atomic
    def post(self, request):
        data = request.data

        required_fields = ["username", "password", "franchise_name", "company_name", "owner_name"]

        for field in required_fields:
            if not data.get(field):
                return Response({field: "This field is required"}, status=400)

        if User.objects.filter(username=data.get("username")).exists():
            return Response({"error": "Username already exists"}, status=400)

        try:
            user = User.objects.create_user(
                username=data.get("username"),
                email=data.get("email"),
                password=data.get("password"),
                role="FRANCHISE"
            )

            logo = request.FILES.get('logo')

            franchise = Franchise.objects.create(
                user=user,
                name=data.get("franchise_name"),
                company_name=data.get("company_name"),
                owner_name=data.get("owner_name"),
                contact_email=data.get("contact_email"),
                contact_phone=data.get("contact_phone"),
                address=data.get("address"),
                website=data.get("website"),
                logo=logo
            )

            return Response({
                "message": "Franchise created successfully",
                "franchise_id": franchise.id
            }, status=201)

        except Exception as e:
            return Response({"error": str(e)}, status=400)


# ✅ LIST FRANCHISES (PAGINATED)
class FranchiseListView(ListAPIView):
    queryset = Franchise.objects.all()
    serializer_class = FranchiseSerializer
    pagination_class = FranchisePagination


# ✅ GET SINGLE FRANCHISE
class FranchiseDetailView(RetrieveAPIView):
    queryset = Franchise.objects.all()
    serializer_class = FranchiseSerializer


# ✅ UPDATE FRANCHISE
class FranchiseUpdateView(UpdateAPIView):
    queryset = Franchise.objects.all()
    serializer_class = FranchiseSerializer
    permission_classes = [IsAuthenticated, IsAdminOrFranchise]

    def get_object(self):
        obj = super().get_object()
        self.check_object_permissions(self.request, obj)  # 🔥 THIS LINE IS IMPORTANT
        return obj

    def get_serializer_context(self):
        return {'request': self.request}
from django.db.models import Count

# ✅ DELETE FRANCHISE
class FranchiseDeleteView(DestroyAPIView):
    queryset = Franchise.objects.all()
    permission_classes = [IsAuthenticated, IsAdmin]


# GET TEAMS OF A FRANCHISE (WITH / WITHOUT PAGINATION)
class FranchiseTeamsView(ListAPIView):
    serializer_class = TeamSerializer
    pagination_class = TeamPagination
 
    def get_queryset(self):
        franchise_id = self.kwargs.get('pk')
        return Team.objects.filter(franchise_id=franchise_id).annotate(
            player_count=Count('players')   # ✅ ADD THIS LINE
        )
 
        # get teams for this franchise
        queryset = Team.objects.filter(franchise_id=franchise_id)
 
        #  optional filter (recommended)
        # queryset = queryset.filter(is_approved=True)
 
        return queryset
 
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
 
        #  WITHOUT PAGINATION
        if request.query_params.get('all') == 'true':
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
 
        # WITH PAGINATION
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
 
        # fallback
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
      
      
      
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenSerializer
    # 🔥 BEST WAY: control pagination here
def paginate_queryset(self, queryset):
        if self.request.query_params.get('all', '').lower().strip() == 'true':
            return None  # ❌ disable pagination
        return super().paginate_queryset(queryset)


# ✅ LOGIN VIEW (JWT)
class CustomLoginView(TokenObtainPairView):
    serializer_class = CustomTokenSerializer
    permission_classes = [AllowAny]
