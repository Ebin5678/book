from django.db import models


class Books(models.Model):
    bookname=models.CharField(max_length=200)
    authorname=models.CharField(max_length=200)
    price=models.PositiveIntegerField()
    category=models.CharField(max_length=200)
    publishdate=models.DateField(null=True,blank=True)
    profile_pic=models.ImageField(upload_to="images",null=True,blank=True)


    def __str__(self):
        return self.bookname
    
