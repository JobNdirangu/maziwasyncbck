from django.db import IntegrityError,transaction
from django.shortcuts import render
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import AllowAny,IsAdminUser,IsAuthenticated
from rest_framework.response import Response
from rest_framework.authentication import authenticate
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from core.models import FarmerProfile, PorterProfile, User
# Create your views here.

@api_view(['POST'])
@permission_classes([IsAdminUser])
@transaction.atomic
def Register(request):
    # print("register function")
    username=request.data.get("username")
    email=request.data.get("email")
    password=request.data.get("password")
    role=request.data.get("role")
    phone_number=request.data.get("phone_number")

    # print(username,email,password,role, phone_number)
    # check emptys
    if not username or not email or not password:
        return Response({"error":"Email, Username and Password are required"}, status=400)
    
    # cehck if the user already exist
    if User.objects.filter(username=username).exists():
        return Response({"error": "Username already taken"}, status=400)
    if User.objects.filter(email=email).exists():
        return Response({"error": "Email already registered"}, status=400)
    
    try:
        # user accoutn creation 
        user= User.objects.create_user(
            username=username,
            email=email,
            password=password,
            role=role,
            phone_number=phone_number,
        )
        if role=='farmer':
            FarmerProfile.objects.create(
                user=user,
                phone_number=phone_number,
                first_name=request.data.get("first_name"),
                last_name=request.data.get("last_name"),
                national_id=request.data.get("national_id"),
                farm_name=request.data.get("farm_name")
            )
        elif role=='porter':
            PorterProfile.objects.create(
                user=user,
                phone_number=phone_number,
                first_name=request.data.get("first_name"),
                last_name=request.data.get("last_name"),
                national_id=request.data.get("national_id"),
                employee_id=request.data.get("employee_id"),
                route_name=request.data.get("route_name")
            )
        return Response({
                "user_id": user.id,
                "username":user.username,
                "role":user.role,
                "message":f"{role.capitalize()} Registered sussessfully"
            })
    

    # error caught from the db
    except IntegrityError as e:
        return Response({"error": "Integrity Error" + str(e)})
    except Exception as e:
        return Response({"error": str(e)})
        

# Login
@api_view(["POST"])
@permission_classes([AllowAny])
def Login(request):
    username=request.data.get("username")
    password=request.data.get("password")
    # print(username,password)

    user=authenticate(username=username, password=password)
    if not user:
        return Response({"error":"Invalid Credentials"})

    refresh=RefreshToken.for_user(user)

    return Response({
        "username":user.username,
        'role':user.role,
        'refresh':str(refresh),
        'access_token':str(refresh.access_token)
    })

# ================================
# Get user/profile of the logged in user
# ==========================
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def MyProfile(request):
    user= request.user
    print(user)

    profile_data={}
    if user.role=='farmer' and hasattr (user, 'farmer_profile'):
        p=user.farmer_profile
        profile_data={
            'first_name':p.first_name,
            'last_name':p.last_name,
            'phone_number':p.phone_number,
            'farm_name':p.farm_name
        }
    elif user.role=='porter' and hasattr(user,'porter_profile'):
        p=user.porter_profile
        profile_data={
            'first_name':p.first_name,
            'last_name':p.last_name,
            'employee_id':p.employee_id,
            'route_name':p.route_name
        }
    return Response({
        'id':user.id,
        'username':user.username,
        'role':user.role,
        'profile':profile_data
    })

# ===============
# logout
# ===============
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def Logout(request):
    try:
        refresh_token = request.data.get("refresh")
        token= RefreshToken(refresh_token)
        token.blacklist()
        return Response({"message": "Logout successfull"})
    except TokenError:
        return  Response({"error": "Invalid or expired token"})
    except Exception as e:
        return Response({"error": str(e)})
