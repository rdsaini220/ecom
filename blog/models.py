from django.db import models

# Create your models here.
class Blogpost(models.Model):
    post_id=models.AutoField(primary_key=True)
    title = models.CharField(max_length=50)
    head1 = models.CharField(max_length=500, default="")
    chead1 = models.CharField(max_length=5000, default="")
    head2 = models.CharField(max_length=500, default="")
    chead2 = models.CharField(max_length=5000, default="")
    head3 = models.CharField(max_length=500, default="")
    chead3 = models.CharField(max_length=5000, default="")
    pub_date = models.DateField()
    thumbnail = models.ImageField(upload_to="shop/images",default="")