# from django.urls import path
# from .views import PlanListView,SubscriptionCreateView,UserProfileView

# app_name = 'membership'

# urlpatterns = [
#     path('profile/',UserProfileView.as_view(), name='user_profile'),

#     # Subscription Plans
#     path('plans/', PlanListView.as_view(), name='plan_list'),
#     # path('plans/subscribe/<int:plan_id>/', SubscriptionCreateView.as_view(), name='subscribe_plan'),
#     # path('membership/plans/subscribe/<int:plan_id>/', SubscriptionCreateView.as_view(), name='subscribe_plan')
#      path('plans/subscribe/<int:plan_id>/', SubscriptionCreateView.as_view(), name='subscription_create'),


#     # Razorpay Webhook
#     # path('razorpay/webhook/', views.razorpay_webhook, name='razorpay_webhook'),

# ]