from django.contrib import admin
from .models import Product,Category,SubCategory,Order,CartItem,ImageVideo
from django.contrib.auth.models import User,Group
# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'product_name', 'price', 'on_discount', 'discount_price','category','subcategory', 'stock','description','created_at','updated_at']
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'user', 'quantity', 'price','address','phone','date','status','created_at','updated_at']
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'category_name']

class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'sub_category_name','category']

class CartItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'product','product_price','product_quantity','created_at','updated_at']
class ImageVideoAdmin(admin.ModelAdmin):
    list_display = ['id', 'product','image_url','video_url']
admin.site.register(Product, ProductAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(SubCategory,SubCategoryAdmin)
admin.site.register(Order,OrderAdmin)
admin.site.register(CartItem,CartItemAdmin)
admin.site.register(ImageVideo,ImageVideoAdmin)