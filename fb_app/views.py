from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.conf import settings
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from leads.models import LeadFormSubmission,Lead,Campaign

@csrf_exempt
def fb_callback(request):
    if request.method == 'POST':
        # Get the lead data from the request
        a = json.loads(request.body)
        print(a)
        
        # Check if the form_id is provided in the request
        ad_id = a.get('ad_id')
        if not ad_id:
            return JsonResponse({'status': 'error', 'message': 'Missing ad_id'}, status=400)
        
        # Check if the campaign with the given form_id exists
        try:
            campaign = Campaign.objects.get(ad_id=ad_id)
        except Campaign.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Campaign not found'}, status=404)
        
        # Map the lead data to your Django model fields
        new_lead = Lead.objects.create(
            first_name=a.get('first_name','full_name'),
            email=a.get('email'),
            city = a.get('city'),
            phone_number=a.get('phone_number'), # use default value for optional fields
            job_title=a.get('job_title'), # use default value for optional fields
            q1=a.get('q1'), # use default value for optional fields
            campaign=campaign,
            source = 'facebook'
        )
        
        # Return a success response
        return JsonResponse({'status': 'success'})
    else:
        # Return a 405 Method Not Allowed error for any other HTTP method
        return JsonResponse({'status': 'error', 'message': 'Method Not Allowed'}, status=405)
