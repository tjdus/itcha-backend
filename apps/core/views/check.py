from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.core.models import User
from apps.core.serializers.member import MemberSerializer


class EmailDuplicationCheckView(APIView):
    def get(self, request):
        email = request.query_params.get('email')

        if email is None:
            return Response({'error': 'Email parameter is required.'}, status=status.HTTP_400_BAD_REQUEST)

        is_taken = User.objects.filter(email=email).exists()
        is_available = not is_taken

        return Response({'email': email, 'available': is_available}, status=status.HTTP_200_OK)


class UsernameDuplicationCheckView(APIView):
    def get(self, request):
        username = request.query_params.get('username')
        if username is None:
            return Response({'error': 'Username parameter is required.'}, status=status.HTTP_400_BAD_REQUEST)

        is_taken = User.objects.filter(username=username).exists()
        is_available = not is_taken

        return Response({'username': username, 'is_taken': is_available}, status=status.HTTP_200_OK)