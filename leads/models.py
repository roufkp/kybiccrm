from django.db import models
from django.db.models.signals import post_save,pre_save
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_migrate
from datetime import timedelta
from django.utils import timezone
import datetime as dt
from datetime import date, timedelta


class User(AbstractUser):
    is_organiser = models.BooleanField(default=True)
    is_agent = models.BooleanField(default=False)
    

#create organisational connection usinf=g this
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


# Create your models here.
class LeadManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()


class Campaign(models.Model):
    name = models.CharField(max_length=50, default=3)
    organisation = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    agent = models.ManyToManyField("Agent", blank=True)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField()
    description = models.TextField()
    ad_id = models.CharField(max_length=50, null=True, blank=True)

    objects = LeadManager()
 
    def __str__(self):
        return self.name


class Lead(models.Model):
    first_name = models.CharField(max_length=200, null=True)
    last_name = models.CharField(max_length=200, null=True,blank=True)
    age = models.IntegerField(default=0, null=True,blank=True,)
    # organisation = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    # agent = models.ForeignKey("Agent", null=True, blank=True, on_delete=models.SET_NULL)
    category = models.ForeignKey("Category", related_name="leads", null=True, blank=True, on_delete=models.SET_NULL)
    campaign = models.ForeignKey("Campaign", related_name='leads', null=True, blank=True, on_delete=models.SET_NULL)
    description = models.TextField(null=True,blank=True,)
    city = models.CharField(max_length=100, null=True,blank=True)
    q1 = models.TextField(null=True,blank=True,)
    a1 = models.TextField(null=True,blank=True,)
    job_title = models.CharField(max_length=100,null=True,blank=True,)
    date_added = models.DateField(auto_now_add=True, null=True)
    phone_number = models.CharField(max_length=20)
    whatsapp_number = models.CharField(max_length=20,null=True,blank=True,)
    email = models.EmailField()
    source = models.CharField(max_length=20,default='Manual')
    # profile_picture = models.ImageField(null=True, blank=True, upload_to="profile_pictures/")
    converted_date = models.DateTimeField(null=True, blank=True)
        # define default category function
    def get_default_category():
        category, created = Category.objects.get_or_create(name='New')
        return category
    category = models.ForeignKey(
        "Category", related_name="leads", null=True, blank=True,
        on_delete=models.SET_NULL, default=get_default_category)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def next_follow_up_date(self):
        follow_ups = self.followups.order_by('-next_date')
        if follow_ups.exists():
            return follow_ups[0].next_date
        else:
            return None

    def days_until_next_follow_up(self):
        next_date = self.next_follow_up_date()
        if next_date:
            today = dt.date.today()
            return (next_date - today).days
        else:
            return None
    
    class Meta:
        ordering = ['-id']



def handle_upload_follow_ups(instance, filename):
    return f"lead_followups/lead_{instance.lead.pk}/{filename}"



class FollowUp(models.Model):
    lead = models.ForeignKey(Lead, related_name="followups", on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)
    next_date = models.DateField(blank=True, null=True, default=timezone.localdate() + timedelta(days=1))
    notes = models.TextField(blank=True, null=True)
    # file = models.FileField(null=True, blank=True, upload_to=handle_upload_follow_ups)
    file = models.ImageField(null=True, blank=True, upload_to="images/")

    class Meta:
        ordering = ['-id'] 

    def __str__(self):
        return f"{self.lead.first_name} {self.lead.last_name}"

class Agent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    organisation = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    ROLE_CHOICES = (
        ('Telecaller', 'Telecaller'),
        ('Marketing Staff', 'Marketing Staff'),
        ('Monitor', 'Monitor'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES,default=True)

    def __str__(self):
        return self.user.email 

class Category(models.Model):
    name = models.CharField(max_length=30,default="New")   #new , contcetd , converted , rejected
    # organisation = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    def __str__(self):
        return self.name

class LeadFormSubmission(models.Model):
    full_name = models.CharField(max_length=255,null=True)
    email = models.EmailField(null=True)
    phone_number = models.CharField(max_length=20,null=True)
    job_title = models.CharField(max_length=20,null=True)
    q1 = models.CharField(max_length=255,null=True)
    form_id = models.CharField(max_length=255,null=True)
    # date_submitted = models.DateTimeField()




def post_user_created_signal(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)



# handle post_user_created_signal once the user is created
post_save.connect(post_user_created_signal,sender=User)


