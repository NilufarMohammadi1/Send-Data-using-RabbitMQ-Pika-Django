from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.response import Response
from knox.models import AuthToken
from .serializers import UserSerializer, RegisterSerializer
from django.contrib.auth import login
from rest_framework import permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView
from .producer import log


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


# Register API
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })


class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        print('request.data---->', request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        user_ip = get_client_ip(request)
        user_agent = request.META['HTTP_USER_AGENT']
        updated_request = request.data.copy()
        updated_request.update({'user_ip': user_ip, 'user_agent': user_agent})

        print(user_ip)
        print(user_agent)
        login(request, user)
        print('serializer dataaaa->', serializer.data)
        log('log', updated_request)
        return super(LoginAPI, self).post(request, format=None)
