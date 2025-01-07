from rest_framework import status, permissions, viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import *
from .serializers import *
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes



@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    data = request.data
    referral_code = data.get("referral_code", None)

    referrer = None
    if referral_code:
        referrer = User.objects.filter(referral_code=referral_code).first()
        if not referrer:
            return Response(
                {"referral_code": "Invalid referral code"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    serializer = UserRegistrationSerializer(data=data)
    if serializer.is_valid():
        
        user = serializer.save()
        
        if referrer:
            user.referred_by = referrer
            user.save()
        
        return Response(
            {
                "message": "User registered successfully",
                "user_id": user.id,
                "email": user.email,
                "referral_code": user.referral_code,
                "referred_by": referrer.email if referrer else None,
            },
            status=status.HTTP_201_CREATED,
        )

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    if request.method == 'POST':
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            return Response({
                'user_id': user.id,
                'email': user.email
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_referrals(request, referral_code):
    if request.method == 'GET':
        referrer = User.objects.filter(referral_code=referral_code).first()
        if not referrer:
            return Response({"message": "Invalid referral code"}, status=status.HTTP_400_BAD_REQUEST)
        
        referrals = User.objects.filter(referred_by=referrer)
        serializer = ReferralSerializer(referrals, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
