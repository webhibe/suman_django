from django.shortcuts import render
from knox.settings import CONSTANTS
from rest_framework import status
# Create your views here.
from django.contrib.auth import login, logout
from django.contrib.auth.models import Group,User
from .models import Category,Product,SubCategory,Order,CartItem,ImageVideo
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView,LogoutView
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions
from rest_framework.response import Response
from knox.models import AuthToken
from .serializers import (UserSerializer, RegisterSerializer,CategorySerializer,
                            ProductSerializer,SubCategorySerializer,
                            OrderSerializer,CartItemSerializer,ImageVideoSerializer,ChangePasswordSerializer)
from django.views.decorators.debug import sensitive_post_parameters
from rest_framework import viewsets
from rest_framework.views import APIView
import os
from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail  
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema


# Register API
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        my_user_group = Group.objects.get_or_create(name='USER')
        my_user_group[0].user_set.add(user)
        return Response({
        "user": UserSerializer(user, context=self.get_serializer_context()).data,
        "token": AuthToken.objects.create(user)[1]
        })
class AdminRegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        my_user_group = Group.objects.get_or_create(name='ADMIN')
        my_user_group[0].user_set.add(user)
        return Response({
        "user": UserSerializer(user, context=self.get_serializer_context()).data,
        "token": AuthToken.objects.create(user)[1]
        })
# Login API
class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        if user.is_active:
            login(request, user)
            return super(LoginAPI, self).post(request, format=None)
        else:
            return Response({"status": "faild", "user_active": user.is_active})

class LogoutAPI(LogoutView):

    def post(self,request, format=None):
        logout(request)
        super(LogoutAPI, self).post(request, format=None)
        data = {"status": "success",'message': 'Sucessfully logged out'}
        return Response(data=data, status=status.HTTP_200_OK)



#Get User API
class AllUserAPI(APIView):

    permission_classes = [permissions.IsAuthenticated,]
    serializer_class = UserSerializer

    def get(self, request):
        if request.user.groups.filter(name='ADMIN').exists():
            queryset = User.objects.all()
            #serializer = serializer = UserSerializer(queryset, many=True)
            user_list=[]
            for user in queryset:
                if user.groups.filter(name='USER').exists():
                    user_list.append(user)
            serializer = UserSerializer(user_list, many=True)    
            return Response({"status": "success", "data": serializer.data})
        return Response({"status": "error", "message": "user can't do this operation"})

class UserEnableDisable(APIView):
    permission_classes = [permissions.IsAuthenticated,]
    serializer_class = UserSerializer

    def delete(self, request, id=None):
        if request.user.groups.filter(name='ADMIN').exists():
            try:
                item = User.objects.get(id=id)
            except Exception as ex:
                return Response({"status": "error", "data": str(ex)})
            if request.data["is_active"]=="True":
                return Response({"status": "error", "message": "wrong request"})
            if item.is_active:
                serializer = UserSerializer(item, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    logout(request)
                    return Response({"status": "success", "data": serializer.data})
                else:
                    return Response({"status": "error", "data": serializer.errors})
            return Response({"status": "error", "message": "user already deactive"})
        return Response({"status": "error", "message": "user can't do this operation"})
    def patch(self, request, id=None):
        if request.user.groups.filter(name='ADMIN').exists():
            try:
                item = User.objects.get(id=id)
            except Exception as ex:
                return Response({"status": "error", "data": str(ex)})
            if request.data["is_active"]=="False":
                return Response({"status": "error", "message": "wrong request"})
            if not item.is_active:
                serializer = UserSerializer(item, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response({"status": "success", "data": serializer.data})
                else:
                    return Response({"status": "error", "data": serializer.errors})
            return Response({"status": "error", "message": "user already active"})
        return Response({"status": "error", "message": "user can't do this operation"})

class UserAPI(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated,]
    serializer_class = UserSerializer
    

    def get_object(self):

        if self.request.user.groups.filter(name='USER').exists():
            return self.request.user
        data ={ "first_name": "","last_name": "","username": "","is_active": False,"groups": []}
        return data

class AdminAPI(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated,]
    serializer_class = UserSerializer

    def get_object(self):
        if self.request.user.groups.filter(name='ADMIN').exists():
            return self.request.user

        data ={ "first_name": "","last_name": "","username": "","is_active": False,"groups": []}
        return data

class CategoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows category to be viewed or edited.
    """
    permission_classes = [permissions.IsAuthenticated,]
    serializer_class = UserSerializer

    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({ "message":'delete resource success', "status":status.HTTP_204_NO_CONTENT})



class ProductViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows items to be viewed or edited.
    """
    permission_classes = [permissions.IsAuthenticated,]
    serializer_class = UserSerializer

    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({ "message":'delete resource success', "status":status.HTTP_204_NO_CONTENT})



class SubProductViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows items to be viewed or edited.
    """
    permission_classes = [permissions.IsAuthenticated,]
    serializer_class = UserSerializer
    
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({ "message":'delete resource success', "status":status.HTTP_204_NO_CONTENT})

class OrderViewSet(viewsets.ModelViewSet):


    permission_classes = [permissions.IsAuthenticated,]
    serializer_class = UserSerializer
    
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({ "message":'delete resource success', "status":status.HTTP_204_NO_CONTENT})

class CartItemViews(APIView):
    permission_classes = [permissions.IsAuthenticated,]
    serializer_class = UserSerializer
    def post(self, request):
        serializer = CartItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    def get(self, request, id=None):
        if id:
            try:
                item = CartItem.objects.get(id=id)
            except Exception as ex:
                return Response({"status": "error", "data": str(ex)})
            serializer = CartItemSerializer(item)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

        items = CartItem.objects.all()
        serializer = CartItemSerializer(items, many=True)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
    def patch(self, request, id=None):
        try:
            item = CartItem.objects.get(id=id)
        except Exception as ex:
            return Response({"status": "error", "data": str(ex)})
        serializer = CartItemSerializer(item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data})
        else:
            return Response({"status": "error", "data": serializer.errors})
    def delete(self, request, id=None):
        item = get_object_or_404(CartItem, id=id)
        item.delete()
        return Response({"status": "success", "data": "Item Deleted"})

    def put(self, request, id=None):
        try:
            item = CartItem.objects.get(id=id)
        except Exception as ex:
            return Response({"status": "error", "data": str(ex)})
        serializer = CartItemSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data})
        return Response({"status": "error", "data": serializer.errors})


class UserViews(APIView):
    permission_classes = [permissions.IsAuthenticated,]
    serializer_class = UserSerializer
    
    def patch(self, request, id=None):
        try:
            item = User.objects.get(id=id)
        except Exception as ex:
            return Response({"status": "error", "data": str(ex)})
        serializer = UserSerializer(item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data})
        else:
            return Response({"status": "error", "data": serializer.errors})
    def delete(self, request, id=None):
        item = get_object_or_404(User, id=id)
        item.delete()
        return Response({"status": "success", "data": "Item Deleted"})


class ImageVideoViewSet(viewsets.ModelViewSet):


    permission_classes = [permissions.IsAuthenticated,]
    serializer_class = UserSerializer
    
    queryset = ImageVideo.objects.all()
    serializer_class = ImageVideoSerializer


    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if os.path.exists(instance.image_url.path):
            os.remove(instance.image_url.path)
            os.remove(instance.video_url.path)
        self.perform_destroy(instance)
        return Response({ "message":'delete resource success', "status":status.HTTP_204_NO_CONTENT})



class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = [permissions.IsAuthenticated,]

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': serializer.data
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    
    email_plaintext_message = "{}?token={}".format(reverse('password_reset:reset-password-request'), reset_password_token.key)
    send_mail(
        # title:
        "Password Reset for {title}".format(title="webhibe"),
        # message:
        email_plaintext_message,
        # from:
        settings.EMAIL_HOST_USER,
        # to:
        [reset_password_token.user.email]
    )

class UserOrderViews(APIView):
    permission_classes = [permissions.IsAuthenticated,]
    serializer_class = UserSerializer
    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def get(self, request, id=None):
        self.object = self.get_object()
        if id:
            try:
                item = Order.objects.get(id=id)
            except Exception as ex:
                return Response({"status": "error", "data": str(ex)})
            serializer = OrderSerializer(item)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

        items = Order.objects.filter(user=self.object.id)
        print(self.object.id)
        serializer = OrderSerializer(items, many=True)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
    
    