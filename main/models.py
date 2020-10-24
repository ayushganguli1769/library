from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
class UserType(models.Model):
    curr_user = models.OneToOneField(User,on_delete= models.CASCADE, related_name='type_user')
    is_admin = models.BooleanField(default= False)
    is_librarian = models.BooleanField(default= False)
    designation = models.CharField(max_length= 1000,blank= False,null= True)
    def __str__(self):
        return self.curr_user.username + "'s user type"
class Book(models.Model):
    name = models.CharField(max_length= 1000,blank= False,null= True)
    author = models.CharField(max_length= 1000,blank= False,null= True)
    def __str__(self):
        return self.name + " by " + self.author
class Customer(models.Model):#Here customer is the student
    name = models.CharField(max_length= 1000,blank= False,null= True)
    phone_no = models.IntegerField(null= True,blank= False)
    image = models.ImageField(null = True)
    def __str__(self):
        return self.name 
class OrderList(models.Model):
    customer_related = models.ForeignKey(Customer,on_delete= models.CASCADE, related_name='customer_order')
    book_related = models.ForeignKey(Book,on_delete= models.CASCADE)
    issue_date = models.DateTimeField(auto_now_add=True)
    return_date = models.DateTimeField()
    is_returned = models.BooleanField(default=False)
    def __str__(self):
        return self.customer_related.name + "'s Order List"
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        my_extended_user = UserType(curr_user = instance)
        my_extended_user.save()
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.type_user.save()