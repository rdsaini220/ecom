from django.db import models

# Create your models here.
class Product(models.Model):
    product_id=models.AutoField
    product_name = models.CharField(max_length=50)
    category = models.CharField(max_length=50, default="")
    subcategory = models.CharField(max_length=50,default="")
    price = models.IntegerField(default="0")
    desc = models.CharField(max_length=300)
    pub_date = models.DateField()
    image = models.ImageField(upload_to="shop/images",default="")


    def __str__(self):
        return self.product_name

class Contact(models.Model):
    msg_id=models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    email = models.EmailField()
    mobile = models.IntegerField(default="0")
    desc = models.CharField(max_length=300)

    def __str__(self):
        return self.name

class Orders(models.Model):
    order_id= models.AutoField(primary_key=True)
    items_json = models.CharField(max_length=300)
    name = models.CharField(max_length=90)
    email = models.EmailField()
    address = models.CharField(max_length=500)
    address2 = models.CharField(max_length=500)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    phone_no = models.IntegerField(default="0")
    zip_code = models.IntegerField(default="0")
    Amount = models.IntegerField(default="0")

    # def __str__(self):
    #     return self.name,self.order_id

class OrderUpdate(models.Model):
    update_id = models.AutoField(primary_key=True)
    order_id = models.IntegerField(default="")
    update_desc = models.CharField(max_length=5000)
    timestamp = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.update_desc[0:7] + "..."
