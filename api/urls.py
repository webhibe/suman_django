from knox import views as knox_views
from .views import (LoginAPI, RegisterAPI, UserAPI,AdminRegisterAPI,
                    AdminAPI,AllUserAPI,UserEnableDisable,LogoutAPI,
                    CategoryViewSet,ProductViewSet,SubProductViewSet,
                    OrderViewSet,CartItemViews,UserViews,ImageVideoViewSet,ChangePasswordView)
from django.urls import path,include
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'category', CategoryViewSet)
router.register(r'subcategory', SubProductViewSet)
router.register(r'product', ProductViewSet)
router.register(r'order', OrderViewSet)
router.register(r'imagevideo', ImageVideoViewSet)


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
    path('api/', include(router.urls)),
    path('api/cart-items/', CartItemViews.as_view()),
    path('api/cart-items/<int:id>/', CartItemViews.as_view()),
    path('api/userop/<int:id>/', UserViews.as_view()),
    path('api/change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('api/email/password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    ]