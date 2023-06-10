from django.db import models
from django.db.models.signals import post_save,pre_save
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_migrate
from datetime import timedelta
from django.utils import timezone
import datetime as dt
from datetime import date, timedelta
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
import razorpay

class User(AbstractUser):
    is_organiser = models.BooleanField(default=True)
    is_agent = models.BooleanField(default=False)
    razorpay_customer_id = models.CharField(max_length=255, null=True, blank=True)


#create organisational connection usinf=g this
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    subscription = models.OneToOneField('Subscription', on_delete=models.CASCADE, null=True, blank=True)
    plan = models.ForeignKey('Plan', on_delete=models.CASCADE, null=True, blank=True)


    def __str__(self):
        return self.user.username

#   subscription section 
class Plan(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=False)
    duration_in_days = models.IntegerField()

    def __str__(self):
        return self.name

class Subscription(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField()
    razorpay_subscription_id = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.plan.name}"

    def is_active(self):
        return self.end_date >= timezone.now().date()


# Create your models here.
class LeadManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()


class Campaign(models.Model):
    name = models.CharField(max_length=50, default="")
    organisation = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    agent = models.ManyToManyField("Agent", blank=True)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    ad_id = models.CharField(max_length=50, null=True, blank=True)

    objects = LeadManager()
 
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['-id']




class Lead(models.Model):
    first_name = models.CharField(max_length=200, null=True)
    last_name = models.CharField(max_length=200, null=True,blank=True)
    age = models.IntegerField(default=0, null=True,blank=True,)
    # organisation = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    # agent = models.ForeignKey("Agent", null=True, blank=True, on_delete=models.SET_NULL)
    category = models.ForeignKey("Category", related_name="leads", null=True, blank=True,default='New', on_delete=models.SET_NULL)
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
    rejected_date = models.DateTimeField(null=True, blank=True)
    followup_date = models.DateTimeField(null=True, blank=True)
    is_read = models.BooleanField(default=False)
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
    
    def save(self, *args, **kwargs):
        created = self.pk is None  # Check if the lead is being created or updated
        super().save(*args, **kwargs)
        if created:
            user = get_user_model().objects.get(pk=self.campaign.organisation.pk)
    #         notification = Notification(user=user, lead=self)
    #         notification.save()

    # def create_lead_notification(sender, instance, created, **kwargs):
    #     if created:
    #         instance.save()

    
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
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

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



# # notification



def post_user_created_signal(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def create_subscription(sender, instance, created, **kwargs):
    if created:
        # Assuming Trial plan is the first plan in the database
        trial_plan = Plan.objects.first()
        end_date = timezone.now().date() + timedelta(days=trial_plan.duration_in_days)
        Subscription.objects.create(user=instance, plan=trial_plan, end_date=end_date)

# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from .models import Lead, Notification


# @receiver(post_save, sender=Lead)
# def create_lead_notification(sender, instance, created, **kwargs):
#     if created:
#         campaign = instance.campaign
#         user = campaign.organisation.user
#         lead_name = f"{instance.first_name} {instance.last_name}"
#         message = f"New lead created: {lead_name}"
#         Notification.objects.create(user=user, message=message)


# handle post_user_created_signal once the user is created
post_save.connect(post_user_created_signal,sender=User)