from django.contrib import admin
from .models import (
    User, Lead , Agent ,UserProfile,Category,Campaign,
# Plan,Subscription
)
# Register your models here.
admin.site.register(Category)
admin.site.register(User)
admin.site.register(UserProfile)
admin.site.register(Lead)
admin.site.register(Agent)
admin.site.register(Campaign)
# admin.site.register(Plan)
# admin.site.register(Subscription)


