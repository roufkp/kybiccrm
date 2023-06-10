from django.shortcuts import render
from leads.models import Plan,Subscription,UserProfile
# Create your views here.
from django.shortcuts import render, redirect
from django.views import View

class PlanListView(View):
    def get(self, request):
        plans = Plan.objects.filter(is_active=True)
        context = {'plans': plans}
        return render(request, 'plan_list.html', context)


class SubscriptionCreateView(View):
    template_name = 'membership/subscription_create.html'

    def get(self, request, plan_id):
        return render(request, self.template_name, {'plan_id': plan_id})

    def post(self, request, plan_id):
        name = request.POST.get('name')
        card_number = request.POST.get('card_number')
        expiration_date = request.POST.get('expiration_date')
        cvv = request.POST.get('cvv')

        # Perform validation on the form data
        if not name or not card_number or not expiration_date or not cvv:
            error_message = "Please fill in all the required fields."
            return render(request, self.template_name, {'plan_id': plan_id, 'error_message': error_message})

        # Process the payment and create the subscription
        # Replace this with your own logic to create the subscription using a payment gateway

        # Assuming the subscription creation is successful
        subscription = Subscription(name=name, card_number=card_number, expiration_date=expiration_date, cvv=cvv)
        subscription.save()

        # Update the user's subscription status
        user_profile = UserProfile.objects.get(user=request.user)
        user_profile.subscription = subscription
        user_profile.save()

        return redirect('dashboard')  # Redirect to the dashboard or any other appropriate page

class UserProfileView(View):
    def get(self, request):
        user_profile = request.user.userprofile
        
        # Check if the user has an active subscription
        has_active_subscription = False
        if user_profile.subscription and user_profile.subscription.status == 'active':
            has_active_subscription = True
        
        return render(request, 'user_profile.html', {'user_profile': user_profile, 'has_active_subscription': has_active_subscription})
