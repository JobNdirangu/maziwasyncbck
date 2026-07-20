from datetime import timedelta
from django.utils import timezone
from django.db.models import Sum

from django.shortcuts import render
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from collector.serilaizer import MilkCollectionSerializer, RecentCollectionSerializer
from cooperative.serializer import NoticeSerializer
from core.models import FarmerProfile, MilkCollection, Notice, PorterProfile
from rest_framework  import generics 
# Create your views here.

# Porter dashboard
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def PorterDashboard(request):
    # get the logged porter/user from the token
    try:
        porter= request.user.porter_profile
    except PorterProfile.DoesNotExist:
        return Response({"error": "Only porters can access this dashboard"})
    
    # time settings
    today= timezone.now().date()
    week_start=today-timedelta(days=7)
    month_start= today.replace(day=1)

    # Todays collections
    today_collections=MilkCollection.objects.filter(porter=porter ,collection_date=today)
    total_collection_today= today_collections.count()
    total_litters_today=today_collections.aggregate(total=Sum('liters'))["total"] or 0
    total_amount_today= today_collections.aggregate(total=Sum('total_amount'))['total'] or 0

    # weekly/monthly
    weekly_collections=MilkCollection.objects.filter(porter=porter, collection_date__gte=week_start)
    total_liters_week=weekly_collections.aggregate(total=Sum('liters'))["total"] or 0

    monthly_collections=MilkCollection.objects.filter(porter=porter, collection_date__gte=month_start)
    total_liters_month=monthly_collections.aggregate(total=Sum('liters'))["total"] or 0

    # current 5 collections
    last_collections=MilkCollection.objects.filter(porter=porter).order_by("created_at")[:5]

    # serialize the multiple milk collecton record since last_collections  is a queryset -multiple objects
    last_collections_list=RecentCollectionSerializer(
        last_collections,
        many=True # DRF serializes each collection individually- without it it we treat it as a sinlge object
    ).data  #returns the serilaized JSON-ready representation of the query

    response_data={
        'date':today,
        'assigned_farmers':porter.assigned_farmers.count(),
        'total_collections_today':total_collection_today,
        'total_liters_today':total_litters_today,
        'total_amount_today':total_amount_today,
        'total_liters_week':total_liters_week,
        'total_liters_month':total_liters_month,
        'last_collections':last_collections_list,
        'porter_name':f'{porter.first_name} {porter.last_name}',
        'route_name':porter.route_name,
        'employee_id':porter.employee_id
    }
    return Response(response_data)
    




@api_view(["POST"])
@permission_classes([IsAuthenticated])
def AddMilkCollection(request):
    # get the logged in user - porter
    try:
        porter= request.user.porter_profile
    except PorterProfile.DoesNotExist:
        return Response({"error":"Only porter can add milk collection"})
    
    # check if the farmer exist  first then pick the object
    try:
        national_id=request.data.get("national_id")
        farmer= FarmerProfile.objects.get(national_id=national_id)
    except FarmerProfile.DoesNotExist:
        return Response({"error": "Farmer not found"})
    
    collection= MilkCollection.objects.create(
        farmer=farmer,
        porter=porter,
        liters=request.data.get("liters"),
        session=request.data.get("session")
    )
    return Response({
        "message":"Milk collection recorderd successfully",
        "collection_id":collection.id,
        "farmer":f"{farmer.first_name} {farmer.last_name}",
        "porter":f"{porter.first_name} {porter.last_name}",
        "liters":collection.liters
    })
    
    
# view porter collections List 
class MyCollections(generics.ListAPIView):
    serializer_class=MilkCollectionSerializer
    permission_classes=[IsAuthenticated]

    def get_queryset(self):
        porter =self.request.user.porter_profile
        colections=(
            MilkCollection.objects
            .filter(porter=porter)
            .select_related('farmer')
            .order_by('created_at')
        )
        return colections

class PorterNoticeView(generics.ListAPIView):
    serializer_class = NoticeSerializer
    permission_classes=[IsAuthenticated]

    def get_queryset(self):
        notices=(
            Notice.objects
            .filter(target__in=['ALL','PORTERS'])
            .order_by('-created_at')
        )
        return notices

