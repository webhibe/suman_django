from rest_framework import generics, permissions
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.models import User,Group
from .models import Product,Category, SubCategory,Order,CartItem,ImageVideo


class GroupSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Group
        fields = ('name',)

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    groups = GroupSerializer(many=True)
    class Meta:
        model = User
        fields = ("id", "first_name", "last_name", "username", "is_active", "groups")

# Register Serializer
# class RegisterSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('id', 'username', 'email', 'password')
#         extra_kwargs = {'password': {'write_only': True}}

#     def create(self, validated_data):
#         user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])

#         return user

class RegisterSerializer(serializers.ModelSerializer):
  email = serializers.EmailField(
    required=True,
    validators=[UniqueValidator(queryset=User.objects.all())]
  )
  password = serializers.CharField(
    write_only=True, required=True, validators=[validate_password])
  password2 = serializers.CharField(write_only=True, required=True)
  class Meta:
    model = User
    fields = ('username', 'password', 'password2',
         'email', 'first_name', 'last_name')
    extra_kwargs = {
      'first_name': {'required': True},
      'last_name': {'required': True}
    }
  def validate(self, attrs):
    if attrs['password'] != attrs['password2']:
      raise serializers.ValidationError(
        {"password": "Password fields didn't match."})
    return attrs
  def create(self, validated_data):
    user = User.objects.create(
      username=validated_data['username'],
      email=validated_data['email'],
      first_name=validated_data['first_name'],
      last_name=validated_data['last_name']
    )
    user.set_password(validated_data['password'])
    user.save()
    return user

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'category_name']

class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory 
        fields = ['id', 'sub_category_name','category']

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        
        fields = ['id', 'product_name', 'price', 'on_discount', 'discount_price','category','subcategory', 'stock','image_url','description']

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        
        fields = ['id', 'product', 'user', 'quantity', 'price','address','phone','date','status']

class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(max_length=200)
    product_price = serializers.FloatField()
    product_quantity = serializers.IntegerField(required=False, default=1)

    class Meta:
        model = CartItem
        fields = ('__all__')

class ImageVideoSerializer(serializers.ModelSerializer):

    class Meta:
        model = ImageVideo
        fields = ('id','product','image_url','video_url')