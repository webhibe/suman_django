from knox import views as knox_views
from .views import (LoginAPI, RegisterAPI, UserAPI,AdminRegisterAPI,
                    AdminAPI,AllUserAPI,UserEnableDisable,LogoutAPI)
from django.urls import path

urlpatterns = [
    path('api/register/', RegisterAPI.as_view(), name='register'),
    path('api/admin/register/', AdminRegisterAPI.as_view(), name='admin_register'),
    path('api/login/', LoginAPI.as_view(), name='login'),
    # path('api/logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('api/logout/', LogoutAPI.as_view(), name='logout'),
    path('api/logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),
    path('api/user/', UserAPI.as_view(), name='user'),
    path('api/alluser/', AllUserAPI.as_view(), name='user'),
    path('api/admin/', AdminAPI.as_view(), name='user'),
    path('api/disable/<int:id>', UserEnableDisable.as_view(), name='disable'),
    path('api/enable/<int:id>', UserEnableDisable.as_view(), name='enable'),
    ]