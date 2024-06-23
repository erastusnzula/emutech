from django.db import models
from django.utils.text import slugify
from django.shortcuts import reverse
from django.conf import settings
import itertools
import random


class Category(models.Model):
    name = models.CharField(max_length= 255)
    
    class Meta:
        verbose_name_plural = 'Categories'
        
    def __str__(self):
        return self.name


class Item(models.Model):
    name = models.CharField(max_length=255, default=f"Item {random.randint(1, 100)}")
    category = models.ManyToManyField('Category', related_name='categories', default='shirts')
    price = models.DecimalField(max_digits= 10, decimal_places = 2, default = 10.00)
    discount = models.DecimalField(max_digits= 10, decimal_places = 2, default = 5.00)
    is_digital = models.BooleanField(blank=True, null=True, default=False)
    description = models.TextField(default='Buy emu tech products', blank=True, null=True)
    stock = models.IntegerField(default=10, null=True, blank = True)
    slug = models.SlugField(unique=True, editable=False, max_length=5, null=True, blank=True)
    seller = models.CharField(max_length=255, blank=True, null=True)  
    created_on = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='emu/items', blank=True, null=True)
    
    def item_price(self):
        if self.discount:
            price = self.price
            discount = self.discount / 100 * price
            return round(price - discount, 2)
        return self.price
    
    @property
    def get_image_url(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url
    
    
    def __str__(self):
        return self.name
    
   
    def _get_slug(self):
        max_length = self._meta.get_field('slug').max_length
        value = random.randint(1, 10000) #self.name[:max_length]
        slug_candidate = slug_original = slugify(value, allow_unicode=True)
        for i in itertools.count(1):
            if not Item.objects.filter(slug=slug_candidate).exists():
                break
            slug_candidate = '{}-{}'.format(slug_original, (i+1))
        self.slug = slug_candidate
        
    def save(self, *args, **kwargs):
        if not self.pk:
            self._get_slug()
        super().save(*args, **kwargs)
        

    def get_absolute_url(self):
        return reverse("item-list", kwargs={"id": self.id})
    
    
class CartItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    is_complete = models.BooleanField(default=False)
    quantity = models.IntegerField(default=1)
    size = models.CharField(max_length=255, null=True, blank=True)
    
    def __str__(self):
        return f"{self.item.name} - {self.quantity}"
    
    
        
    def get_price(self):
        if self.item.discount:
            price = self.item.price * self.quantity
            discount = self.item.discount / 100 * price
            return round(price - discount, 2)
        return round((self.item.price * self.quantity), 2)

    
class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    transaction_id = models.CharField(blank=True, null=True, max_length=255)
    items = models.ManyToManyField(CartItem, related_name='order_items')
    created_on = models.DateTimeField(auto_now_add = True)
    is_complete = models.BooleanField(default=False)
    shipping_addess  = models.ForeignKey('ShippingAddress', related_name='shipping_address', on_delete=models.SET_NULL, blank=True,  null=True)
    coupon = models.ForeignKey('Coupon', on_delete=models.SET_NULL, blank=True, null=True)
    
    class Meta:
        ordering = ['-created_on']
        
    def get_total(self):
        total = 0
        for item in self.items.all():
            total += item.get_price()
        if self.coupon:
            total -= self.coupon.amount
        return round(total, 2)
    
    def get_cart_items(self):
        return self.items.count()
    
    def __str__(self):
        return self.user.username
    
    @property
    def for_shipping(self):
        shipping = False
        for item in self.items.all():
            if item.item.is_digital == False:
                shipping = True
        return shipping
        
            
        
class Coupon(models.Model):
    code = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits =  10 , decimal_places= 2)
    
    def __str__(self):
        return self.code 
    
class ShippingAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    town = models.CharField(max_length= 255, blank=True, null=True)
    city = models.CharField(max_length= 255, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    zipe_code = models.CharField(max_length=255, blank=True, null=True)
    default = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering=['-created_on']
    def __str__(self):
        return self.user.username
    
    
    
    
    
    
    
    
    