from django.core.mail import send_mail
import datetime as dt
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render,redirect,reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.views import generic 
from .models import Lead,Agent,Category
from .forms import LeadModelForm,LeadForm,CustomUserCreationForm,AssignAgentForm,LeadCategoryUpdateForm,CategoryModelForm,FollowUpModelForm
from agents.mixins import OrganiserAndLoginRequiredMixin
from facebook import GraphAPI
from .models import LeadFormSubmission,FollowUp
from itertools import groupby
from campaign.views import Campaign
from django.utils import timezone
from django.db.models import Count, Q, Sum,Max
from django.utils.timezone import make_aware
from datetime import timedelta, datetime
from django.views.generic import ListView,TemplateView
from django.db.models import Count
from .models import Lead, Category, FollowUp
from datetime import date
from django.views import View
from twilio.rest import Client
from django.core.mail import EmailMessage
from campaign.forms import ContactForm


#CRUD - create,retreive,update,delete + list


def lead_form_submissions(request):
    submissions = LeadFormSubmission.objects.all()
    context = {'submissions': submissions}
    return render(request, 'lead_form_submissions.html', context)


class SignupView(generic.CreateView):
    template_name = "registration/signup.html"
    form_class = CustomUserCreationForm
    
    def get_success_url(self):
        return reverse("login") 



class LandingPageView(generic.TemplateView):
    template_name = "landing.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("dashboard")
        return super().dispatch(request, *args, **kwargs)


def landing_page(request):
    return render(request,"landing.html")


def pricing_page(request):
    return render(request,"pricing.html")

def services_page(request):
    return render(request,"services.html")





def contactus_page(request):
    return render(request,"contactus.html")

def aboutus_page(request):
    return render(request,"aboutus.html")

def dashboard(request):
    return render(request,"dashboard.html")


class DashboardView(LoginRequiredMixin, generic.TemplateView):
    template_name = "dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user
        thirty_days_ago = timezone.now() - timedelta(days=30)
        converted_category = Category.objects.get(name="Converted")
        followup_category = Category.objects.get(name="Follow Up")
        start_date_str = self.request.GET.get('start_date')
        end_date_str = self.request.GET.get('end_date')
        
        converted_data = []
        if user.is_organiser:
            campaigns = Campaign.objects.filter(organisation=user.userprofile)     
            # How many leads we have in total
            total_campaign_count = Campaign.objects.filter(organisation=user.userprofile).count()
            total_lead_count=Lead.objects.filter(campaign__organisation=user.userprofile).count()
            # How many new leads in the last 30 days      
            total_in_past30 = Campaign.objects.filter(
                organisation=user.userprofile,
                start_date__gte=thirty_days_ago
            ).count()
            # How many converted leads in the last 30 days        
            converted_in_past30 = Lead.objects.filter(
                category=converted_category,
                campaign__organisation=user.userprofile,
                converted_date__gte=thirty_days_ago
            ).count()        
            total_followup_leads = Lead.objects.filter(
                campaign__organisation=user.userprofile,
                category=followup_category,
            ).count()
            # Total leads converted in a date range       
            if start_date_str and end_date_str:
                start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
                end_date = datetime.strptime(end_date_str, "%Y-%m-%d") + timedelta(days=1)
                leads_converted_in_date_range = Lead.objects.filter(
                    Q(category=converted_category),
                    Q(converted_date__range=[start_date, end_date]),
                    Q(campaign__organisation=user.userprofile)
                ).count()
                total_followup_leads_in_date_range = Lead.objects.filter(
                    Q(category=followup_category),
                    Q(converted_date__range=[start_date, end_date]),
                    Q(campaign__organisation=user.userprofile)
                ).count()
            else:
                leads_converted_in_date_range = 0
                # total_followup_leads_in_date_range= 0
                start_date = thirty_days_ago
                end_date = timezone.now()
            # Chart data for leads converted in date range
            date_range = (end_date - start_date).days
            for i in range(date_range+1):
                day = start_date + timedelta(days=i)
                count = Lead.objects.filter(
                    Q(category=converted_category),
                    Q(converted_date__year=day.year),
                    Q(converted_date__month=day.month),
                    Q(converted_date__day=day.day),
                    Q(campaign__organisation=user.userprofile)
                ).count()
                converted_data.append(count)
        else:
            campaigns = Campaign.objects.filter(organisation = user.agent.organisation).filter(agent__user = user)   
            # How many leads we have in total
            total_campaign_count = Campaign.objects.filter(organisation = user.agent.organisation).filter(agent__user = user).count()
            total_lead_count=Lead.objects.filter(campaign__organisation = user.agent.organisation).filter(campaign__agent__user = user).count()
            # How many new leads in the last 30 days      
            total_in_past30 = Campaign.objects.filter(
                organisation = user.agent.organisation,
                start_date__gte=thirty_days_ago
            ).filter(agent__user = user).count()
            # How many converted leads in the last 30 days        
            converted_in_past30 = Lead.objects.filter(
                category=converted_category,
                campaign__organisation = user.agent.organisation,
                converted_date__gte=thirty_days_ago
            ).filter(campaign__agent__user = user).count()        
            total_followup_leads = Lead.objects.filter(
                campaign__organisation = user.agent.organisation,
                category=followup_category,
            ).filter(campaign__agent__user = user).count()
            # Total leads converted in a date range       
            if start_date_str and end_date_str:
                start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
                end_date = datetime.strptime(end_date_str, "%Y-%m-%d") + timedelta(days=1)
                leads_converted_in_date_range = Lead.objects.filter(
                    Q(category=converted_category),
                    Q(converted_date__range=[start_date, end_date]),
                    Q(campaign__organisation = user.agent.organisation)
                ).filter(campaign__agent__user = user).count()
            else:
                leads_converted_in_date_range = 0
                start_date = thirty_days_ago
                end_date = timezone.now()
            # Chart data for leads converted in date range
            date_range = (end_date - start_date).days
            for i in range(date_range+1):
                day = start_date + timedelta(days=i)
                count = Lead.objects.filter(
                    Q(category=converted_category),
                    Q(converted_date__year=day.year),
                    Q(converted_date__month=day.month),
                    Q(converted_date__day=day.day),
                    Q(campaign__organisation = user.agent.organisation)
                ).filter(campaign__agent__user = user).count()
                converted_data.append(count)





        chart_data = {
            "labels": [day.strftime("%Y-%m-%d") for day in
                       (start_date + timedelta(days=i) for i in range(date_range+1))],
            "datasets": [{
                "label": "Converted Leads",
                "data": converted_data,
                "borderColor": 'rgb(255, 99, 132)',
                "backgroundColor": 'rgba(255, 99, 132, 0.2)',
                "tension": 0.1
            }]
            
        }
        
        context.update({
            "campaigns":campaigns,
            "total_lead_count": total_lead_count,
            "total_campaign_count": total_campaign_count,
            "total_followup_leads":total_followup_leads,
            "total_in_past30": total_in_past30,
            "converted_in_past30": converted_in_past30,
            "chart_data": chart_data,
            "start_date_str": start_date_str,
            "end_date_str": end_date_str,
            "leads_converted_in_date_range": leads_converted_in_date_range,
            # 'total_followup_leads_in_date_range':total_followup_leads_in_date_range
        })

        return context


class LeadListView(LoginRequiredMixin, generic.ListView):
    template_name = "leads/lead_list.html"
    context_object_name = "leads"
    
    def get_queryset(self):
        user = self.request.user
        
        # Get the campaigns of the current user
        campaigns = Campaign.objects.filter(Q(organisation = user.userprofile) | Q(organisation = user.agent.organisation))
        
        # Get the leads associated with these campaigns
        queryset = Lead.objects.filter(campaign__in=campaigns)

        return queryset
    
    def get_context_data(self, **kwargs):
        context = super(LeadListView, self).get_context_data(**kwargs)
        user = self.request.user
        
        # If the user is an admin, show the unassigned leads
        if user.is_organiser:
            queryset = Lead.objects.filter(campaign__organisation=user, agent=None)
            context.update({
                "unassigned_leads":queryset
            })
            
        return context
   

#display leads list
def lead_list(request):
    #return HttpResponse("hello world")
    leads=Lead.objects.all()
    context={
        "leads":leads
    }
    return render(request,'leads/lead_list.html',context)



class LeadDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = "leads/lead_detail.html"
    context_object_name = "lead"  

    def get_queryset(self):
        user = self.request.user
        # Get the campaign ID from the URL parameter
        campaign_id = self.kwargs.get('campaign_id')
        # Get the campaign object based on the ID
        campaign = get_object_or_404(Campaign, id=campaign_id)
        # Check if the user has access to the campaign
        if user.is_organiser or user.agent.organisation == campaign.organisation:
            # Filter the leads by the campaign
            queryset = Lead.objects.filter(campaign=campaign)
        else:
            # If the user doesn't have access to the campaign, return an empty queryset
            queryset = Lead.objects.none()
        return queryset
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     lead = self.get_object()
    #     context['days_until_follow_up'] = lead.days_until_next_follow_up()
    #     return context
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lead = self.get_object()
        context["category"] = lead.category
        context['next_follow_up_date'] = lead.next_follow_up_date()
        # Only show the "Add Follow-up" button if the lead's category is "Follow Up"
        context["show_follow_up_button"] = lead.category.name == "Follow Up"
        context["show_lead_waiting"] = lead.category.name == "New"
        context["show_converted"] = lead.category.name == "Converted"
        context["show_rejected"] = lead.category.name == "Rejected"
        context["show_change_status_button"] = lead.category.name not in ["Converted", "Rejected"]
        return context

        
#individual lead display
def lead_detail(request,pk):
    lead = Lead.objects.get(id=pk)
    context={
        "lead":lead
    }
    return render(request,'leads/lead_detail.html',context) 



class LeadCreateView(OrganiserAndLoginRequiredMixin, generic.CreateView):
    template_name = "leads/lead_create.html"
    form_class = LeadModelForm

    def form_valid(self, form):
        campaign = get_object_or_404(Campaign, id=self.kwargs['pk'])
        lead = form.save(commit=False)
        lead.campaign = campaign
        lead.save()
        print("hi")
        # send mail
        send_mail(
            subject="A lead has been created",
            message="Go to the site to see the lead",
            from_email="test@test.com",
            recipient_list=["test2@test.com"],
        )
        # return super(LeadCreateView, self).form_valid(form)
        return super(LeadCreateView,self).form_valid(form)

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse("campaigns:campaign-detail", kwargs={"pk": pk})

#create lead and store using ModelForm


class LeadUpdateView(LoginRequiredMixin,generic.UpdateView):
    template_name = "leads/lead_update.html"
    form_class = LeadModelForm

    # def get_success_url(self):
    #     return reverse("leads:lead-detail")
    def get_success_url(self):
        return reverse("leads:lead-detail", kwargs={"campaign_id": self.kwargs["campaign_id"], "pk": self.kwargs["pk"]})

    def get_queryset(self):
        user = self.request.user    
        return  Lead.objects.filter(campaign__organisation = user.userprofile) 
#Update Lead /

def lead_update(request,pk):
    lead=Lead.objects.get(id=pk)
    form=LeadModelForm(instance=lead)
    if request.method=="POST":
        form=LeadModelForm(request.POST,instance=lead)
        if form.is_valid():
            form.save()
            return redirect("/leads")
    context={
        "form":form,
        "lead":lead
    }

    return render(request,"leads/lead_update.html",context)


class LeadDeleteView(LoginRequiredMixin,generic.DeleteView):
    template_name = "leads/lead_delete.html"

    def get_success_url(self):
        return reverse("campaign:campaign-detail", kwargs={"pk": self.kwargs["campaign_id"],"pk": self.kwargs["pk"]})

    def get_queryset(self):
        user = self.request.user      
        return  Lead.objects.filter(campaign__organisation = user.userprofile) 

def lead_delete(request,pk):
    lead=Lead.objects.get(id=pk)
    lead.delete()
    return redirect("/leads")


# category list display using for loop method 
# class CategoryListView(LoginRequiredMixin, generic.ListView):
#     template_name = "leads/category_list.html"
#     context_object_name = "category_list"

#     def get_queryset(self):
#         user = self.request.user

#         if user.is_organiser:
#             # Get all the campaigns created by the user's organisation
#             campaigns = Campaign.objects.filter(organisation=user.userprofile)

#             # Get all the leads associated with the user's organisation's campaigns
#             queryset = Lead.objects.filter(campaign__in=campaigns)
#         else:
#             # Get all the campaigns assigned to the user
#             campaigns = Campaign.objects.filter(Q(agent=user.agent) | Q(organisation=user.agent.organisation))

#             # Get all the leads associated with the campaigns assigned to the user
#             queryset = Lead.objects.filter(campaign__in=campaigns).filter(campaign__agent__user = user)

#         return queryset

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         user = self.request.user
#         if user.is_organiser:
#             # Get all the campaigns created by the user's organisation
#             campaigns = Campaign.objects.filter(organisation=user.userprofile)
#         else:
#             # Get all the campaigns assigned to the user
#             campaigns = Campaign.objects.filter(Q(agent=user.agent) | Q(organisation=user.agent.organisation)).filter(agent__user = user)
#         # Get the counts of leads associated with each category for the user's campaigns
#         lead_counts = (
#             Lead.objects.filter(campaign__in=campaigns)
#             .values("category__name")
#             .annotate(count=Count("category__name"))
#         )
#         # Get all the leads associated with the user's campaigns
#         leads = Lead.objects.filter(campaign__in=campaigns)
#         categories = Category.objects.all()
#         category_leads = {}
#         for category in categories:
#             category_leads[category.name] = leads.filter(category=category)

#         context.update(
#             {
#                 "categories": categories,
#                 "category_leads": category_leads,
#                 "lead_counts": lead_counts,
#             }
#         )

#         return context

class CategoryListView(LoginRequiredMixin, generic.ListView):
    template_name = "leads/category_list.html"
    context_object_name = "category_list"

    def get_queryset(self):
        user = self.request.user

        if user.is_organiser:
            # Get all the campaigns created by the user's organisation
            campaigns = Campaign.objects.filter(organisation=user.userprofile)

            # Get all the leads associated with the user's organisation's campaigns
            queryset = Lead.objects.filter(campaign__in=campaigns)
        else:
            # Get all the campaigns assigned to the user
            campaigns = Campaign.objects.filter(Q(agent=user.agent) | Q(organisation=user.agent.organisation))

            # Get all the leads associated with the campaigns assigned to the user
            queryset = Lead.objects.filter(campaign__in=campaigns).filter(campaign__agent__user = user)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if user.is_organiser:
            # Get all the campaigns created by the user's organisation
            campaigns = Campaign.objects.filter(organisation=user.userprofile)
        else:
            # Get all the campaigns assigned to the user
            campaigns = Campaign.objects.filter(Q(agent=user.agent) | Q(organisation=user.agent.organisation)).filter(agent__user=user)

        # Get the counts of leads associated with each category for the user's campaigns
        # lead_counts = (
        #     Lead.objects.filter(campaign__in=campaigns)
        #     .values("category__name")
        #     .annotate(count=Count("category__name"))
        # )

        # Get all the leads associated with the user's campaigns
        leads = Lead.objects.filter(campaign__in=campaigns)
         # Get the total lead counts for each category
        lead_counts = (
            leads.values("category__name")
            .annotate(count=Count("category__name"))
            .values_list("category__name", "count")
        )
        # Create empty dictionaries to store leads for each category
        follow_up_leads = {}
        new_leads = {}
        converted_leads = {}
        rejected_leads = {}

    # Iterate through each lead and add it to the appropriate dictionary based on its category
        for lead in leads:
            if lead.category.name == "Follow Up":
                follow_up_leads[lead.id] = lead
            elif lead.category.name == "New":
                new_leads[lead.id] = lead
            elif lead.category.name == "Converted":
                converted_leads[lead.id] = lead
            elif lead.category.name == "Rejected":
                rejected_leads[lead.id] = lead

        # Add the dictionaries to the context
        context.update(
            {
                "follow_up_leads": follow_up_leads,
                "new_leads": new_leads,
                "converted_leads": converted_leads,
                "rejected_leads": rejected_leads,
                "lead_counts": lead_counts,
            }
        )

        return context



class LeadCategoryUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = "leads/lead_category_update.html"
    form_class = LeadCategoryUpdateForm

    def get_queryset(self):
        user = self.request.user
        campaign_id = self.kwargs['campaign_id']
        # filter leads for the current campaign
        queryset = Lead.objects.filter(campaign__id=campaign_id)
        return queryset

    def get_success_url(self):
        return reverse("leads:lead-detail", kwargs={"campaign_id": self.object.campaign.id, "pk": self.object.id})

    def form_valid(self, form):
        lead_before_update = self.get_object()
        instance = form.save(commit=False)
        converted_category = Category.objects.get(name="Converted")
        if form.cleaned_data["category"] == converted_category:
            # update the date at which this lead was converted
            if lead_before_update.category != converted_category:
                # this lead has now been converted 
                instance.converted_date = dt.datetime.now()
        instance.save()
        return super(LeadCategoryUpdateView, self).form_valid(form)


class FollowUpListView(LoginRequiredMixin, View):
    template_name = 'leads/followup_list.html'

    def get(self, request, campaign_id=None):
        user = self.request.user
        if user.is_organiser:
            user_profile = request.user.userprofile
        else:
            user_profile = request.user.agent.organisation

        today = timezone.localdate()
        upcoming = today + timedelta(days=7)
        if user.is_organiser:
            today_followups = FollowUp.objects.filter(next_date=today, lead__campaign__organisation=user_profile)
            upcoming_followups = FollowUp.objects.filter(next_date__gt=today, next_date__lte=upcoming, lead__campaign__organisation=user_profile)
            someday_followups = FollowUp.objects.filter(next_date__gt=upcoming, lead__campaign__organisation=user_profile)
            overdue_followups = FollowUp.objects.filter(next_date__lt=today, lead__campaign__organisation=user_profile)
            today_leads = [f.lead for f in today_followups if f.lead.category.name not in ['Converted', 'Rejected']]
            upcoming_leads = [f.lead for f in upcoming_followups if f.lead.category.name not in ['Converted', 'Rejected']]
            someday_leads = [f.lead for f in someday_followups if f.lead.category.name not in ['Converted', 'Rejected']]
            overdue_leads = [f.lead for f in overdue_followups if f.lead.category.name not in ['Converted', 'Rejected']]
            no_follow_up_leads = Lead.objects.filter(campaign__organisation=user_profile).filter(category__name="Follow Up").exclude(id__in=[l.id for l in today_leads+upcoming_leads+someday_leads+overdue_leads]).exclude(followups__next_date__isnull=False)

        else:
            today_followups = FollowUp.objects.filter(next_date=today, lead__campaign__organisation=user_profile).filter(lead__campaign__agent__user = user)
            upcoming_followups = FollowUp.objects.filter(next_date__gt=today, next_date__lte=upcoming, lead__campaign__organisation=user_profile).filter(lead__campaign__agent__user = user)
            someday_followups = FollowUp.objects.filter(next_date__gt=upcoming, lead__campaign__organisation=user_profile).filter(lead__campaign__agent__user = user)
            overdue_followups = FollowUp.objects.filter(next_date__lt=today, lead__campaign__organisation=user_profile).filter(lead__campaign__agent__user = user)
            today_leads = [f.lead for f in today_followups if f.lead.category.name not in ['Converted', 'Rejected']]
            upcoming_leads = [f.lead for f in upcoming_followups if f.lead.category.name not in ['Converted', 'Rejected']]
            someday_leads = [f.lead for f in someday_followups if f.lead.category.name not in ['Converted', 'Rejected']]
            overdue_leads = [f.lead for f in overdue_followups if f.lead.category.name not in ['Converted', 'Rejected']]
            no_follow_up_leads = Lead.objects.filter(campaign__organisation=user_profile).filter(category__name="Follow Up").filter(campaign__agent__user = user).exclude(id__in=[l.id for l in today_leads+upcoming_leads+someday_leads+overdue_leads]).exclude(followups__next_date__isnull=False)




      
        leads_by_status = {
            'Follow-up Due': overdue_leads,
            'Today': today_leads,
            'Upcoming': upcoming_leads,
            'Someday': someday_leads,
            'No Follow-up Date': no_follow_up_leads,
        }

        context = {
            'leads_by_status': leads_by_status,
            'campaign_id': campaign_id,
        }

        return render(request, self.template_name, context)

class FollowUpCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = "leads/followup_create.html"
    form_class = FollowUpModelForm

    def get_success_url(self):
        return reverse("leads:lead-detail", kwargs={"campaign_id": self.kwargs["campaign_id"], "pk": self.kwargs["pk"]})


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["lead"] = get_object_or_404(Lead, pk=self.kwargs["pk"])
        return context

    def form_valid(self, form):
        lead = get_object_or_404(Lead, pk=self.kwargs["pk"])
        followup = form.save(commit=False)
        followup.lead = lead
        followup.save()
        return super().form_valid(form)



class FollowUpUpdateView(LoginRequiredMixin,generic.UpdateView):
    model = FollowUp
    fields = ['next_date', 'notes', 'file']
    template_name = 'followup_update.html'
    success_url = reverse_lazy('leads:followup-list')

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(lead__campaign__organisation=self.request.user.userprofile)
        return queryset

class FollowUpDeleteView(OrganiserAndLoginRequiredMixin, generic.DeleteView):
    template_name = "leads/followup_delete.html"

    def get_success_url(self):
        followup = FollowUp.objects.get(id=self.kwargs["pk"])
        return reverse("leads:lead-detail", kwargs={"pk": followup.lead.pk})

    def get_queryset(self):
        user = self.request.user
        # initial queryset of leads for the entire organisation
        if user.is_organiser:
            queryset = FollowUp.objects.filter(lead__organisation=user.userprofile)
        else:
            queryset = FollowUp.objects.filter(lead__organisation=user.agent.organisation)
            # filter for the agent that is logged in
            queryset = queryset.filter(lead__agent__user=user)
        return queryset


# class WhatsappMessagingView
# class WhatsappMessagingView(OrganiserAndLoginRequiredMixin, View):

#     def get(self, request, pk):
#         # Handle GET requests, for example to show a confirmation page
#         return render(request, 'leads/whatsapp_confirm.html')

#     def post(self, request, pk):
#         lead = get_object_or_404(Lead, id=pk)

#         # check if lead has a WhatsApp number
#         if not lead.whatsapp_number:
#             return HttpResponse("Lead does not have a WhatsApp number.")

#         # set up Twilio client with your credentials
#         account_sid = 'AC7ceee1e881b956cfad4c29a4a6728439'
#         auth_token = '03e85dbe2d59e9555d8e9b8725fc29f0'
#         client = Client(account_sid, auth_token)

#         # define the message to send
#         message_body = 'Hello from your lead management system!'

#         # use the Twilio client to send the message via WhatsApp
#         message = client.messages.create(
#             from_='whatsapp:+919061713244',
#             to='whatsapp:+lead.whatsapp_number',
#             body=message_body
#         )

#         # print the message SID for debugging purposes
#         print(message.sid)

#         return HttpResponse("WhatsApp message sent successfully.")

"""
#Update Lead /normal mode
def lead_update(request,pk):
    lead = Lead.objects.get(id=pk)
    form=LeadForm()
    if request.method=="POST":
        form=LeadForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            age = form.cleaned_data['age']
            lead.first_name = first_name
            lead.last_name = last_name
            lead.age = age
            lead.save()
            return redirect("/leads")
    context={
        "form":form,
        "lead":lead
    }

    return render(request,"leads/lead_update.html",context)
"""

#create lead and store usinf normal django form
"""def lead_create(request):
    form=LeadForm()
    if request.method=="POST":
        form=LeadForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            age = form.cleaned_data['age']
            #grab a agent from database(model Agent)
            agent = Agent.objects.first()
            #create new row in table
            Lead.objects.create(
                first_name=first_name,
                last_name = last_name,
                age = age,
                agent = agent
            )
            return redirect("/leads")
    context={
        "form":form
    }
    return render(request,"leads/lead_create.html",context)
    """