from django.db import models
from django.contrib.auth.models import User
import datetime

from django.core.validators import FileExtensionValidator

# Create your models here.
class Category(models.Model):
    category_name = models.CharField(max_length=100)

    def __str__(self):
        return self.category_name

class SubCategory(models.Model):
    sub_category_name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.sub_category_name

def image_upload(instance, filename):
    return 'images/{filename}'.format(filename=filename)
def video_upload(instance, filename):
    return 'videos/{filename}'.format(filename=filename)

class Product(models.Model):
    product_name = models.CharField(max_length=100)
    price = models.FloatField(default=0)
    on_discount = models.BooleanField(default=False)
    discount_price = models.FloatField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    stock = models.IntegerField(default=0)
    description = models.TextField()

    def __str__(self):
        return self.product_name

class ImageVideo(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    image_url = models.ImageField(upload_to=image_upload, blank=True, null=True)
    video_url = models.FileField(upload_to=video_upload,blank=True, null=True, validators=[FileExtensionValidator( ['MP4','WEBM','MPG','MP2','MPEG','MPE','MPV','OGG','M4P','M4V','AVI','WMV'] ) ])

    def __str__(self):
        return self.product.product_name

class Order(models.Model):
    product = models.ForeignKey(Product,
                                on_delete=models.CASCADE)
    user = models.ForeignKey(User,
                                 on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.IntegerField()
    address = models.CharField(max_length=50, default='', blank=True)
    phone = models.CharField(max_length=50, default='', blank=True)
    date = models.DateField(default=datetime.datetime.today)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.user.first_name

class CartItem(models.Model):
    product_name = models.CharField(max_length=200)
    product_price = models.FloatField()
    product_quantity = models.PositiveIntegerField()

    def __str__(self):
        return self.product_name
  

