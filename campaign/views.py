import random
from django.db.models import OuterRef, Subquery, Count
from django.shortcuts import render
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.views import generic
from django.shortcuts import reverse,redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from leads.models import Campaign
from leads.models import Agent
from .mixins import OrganiserAndLoginRequiredMixin
from .forms import CampaignModelForm,CampaignAddAgentModelForm,ContactForm
from leads.forms import AssignAgentForm
from leads.views import Lead
from django.core.mail import EmailMessage
from django.urls import reverse
from django.http import HttpResponse


class CampaignListView(LoginRequiredMixin,generic.ListView):
    template_name = "campaigns/campaign_list.html"
    context_object_name = "campaigns"
    print("campaign list view")

    def get_queryset(self):
        user = self.request.user

        #inistial query set for the entireorganisation
        if user.is_organiser:
            queryset = Campaign.objects.filter(
                organisation = user.userprofile,
                agent__isnull = False
            ) 
        else: 
            queryset = Campaign.objects.filter(
                organisation = user.agent.organisation,
                agent__isnull = False
            ) 

            # query set for the agent logged in
            queryset = queryset.filter(agent__user = user)
                # Add a subquery to count the total number of leads for each campaign
        subquery = Lead.objects.filter(campaign=OuterRef('pk')).order_by().values('campaign__id').annotate(count=Count('*')).values('count')
        queryset = queryset.annotate(total_leads=Subquery(subquery))

        return queryset.distinct()
    
    # def get_context_data(self, **kwargs):
    #     context = super(CampaignListView, self).get_context_data(**kwargs)
    #     user = self.request.user
    #     if user.is_organiser:
    #         queryset = Campaign.objects.filter(
    #             organisation = user.userprofile,
    #             agent__isnull=True
    #         ) 
    #         context.update({
    #             "unassigned_campaigns":queryset
    #         })
    #     return context

  
# Create Campaignshere.


# class CampaignCreateView(OrganiserAndLoginRequiredMixin,generic.CreateView):
#     template_name = "campaigns/campaign_create.html"
#     form_class = CampaignModelForm

#     def get_success_url(self):
#         return reverse("campaign:campaign-list")

#     def form_valid(self,form):
#         campaign = form.save(commit=False)
#         organisation = self.request.user.userprofile
#         campaign.organisation = organisation
#         campaign.save()
#         # send mail
#         send_mail(
#             subject="A campaign has been created",
#             message="Go to the site to see the lead",
#             from_email="test@test.com",
#             recipient_list=["test2@test.com"],
#         )
#         return super(CampaignCreateView,self).form_valid(form)


# class CampaignCreateView(OrganiserAndLoginRequiredMixin,generic.CreateView):
#     template_name = "campaigns/campaign_create.html"
#     form_class = CampaignModelForm

#     def get_success_url(self):
#         return reverse("campaign:campaign-list")

#     def form_valid(self,form):
#         campaign = form.save(commit=False)
#         organisation = self.request.user.userprofile
#         campaign.organisation = organisation
#         campaign.save()
#         # send mail
#         send_mail(
#             subject="A campaign has been created",
#             message="Go to the site to see the lead",
#             from_email="test@test.com",
#             recipient_list=["test2@test.com"],
#         )
#         return super(CampaignCreateView,self).form_valid(form)

#     def get_form_kwargs(self):
#         kwargs = super().get_form_kwargs()
#         kwargs['user'] = self.request.user
#         return kwargs
class CampaignCreateView(OrganiserAndLoginRequiredMixin, generic.CreateView):
    template_name = "campaigns/campaign_create.html"
    form_class = CampaignModelForm
    print("campaign create view")

    def get_success_url(self):
        return reverse("campaign:campaign-list")

    def form_valid(self, form):
        print("hi")
        campaign = form.save(commit=False)
        organisation = self.request.user.userprofile
        campaign.organisation = organisation
        campaign.save()

        # Add agents to the campaign
        agents = form.cleaned_data['agents']
        campaign.agent.set(agents)
        print("hiooo")
        for agent in agents:
            #send mail
            #Send email to the user using smtp
            subject = 'New Campaign assigned to you.'
            body = 'A new campaign assigned to you by the admin, please visit the www.crm.addox.in to check it.'
            from_email = 'developer.addox@gmail.com'
            to_email = [agent.user.email]
            email = EmailMessage(subject, body, from_email, to_email)
            email.send()

        
        return super(CampaignCreateView, self).form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class CampaignUpdateView(OrganiserAndLoginRequiredMixin, generic.UpdateView):
    template_name = "campaigns/campaign_update.html"
    form_class = CampaignModelForm

    def get_success_url(self):
        return reverse("campaigns:campaign-list")

    def get_queryset(self):
        organisation = self.request.user.userprofile
        return Campaign.objects.filter(organisation=organisation)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs



class CampaignDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = 'campaigns/campaign_detail.html'
    model = Campaign
    context_object_name = 'campaign'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        campaign = context['campaign']
        leads = campaign.leads.all()

        lead_followups = {}
        for lead in leads:
            followups = lead.followups.all()
            if followups.exists():
                lead_followups[lead.id] = followups.latest('date_added')
            else:
                lead_followups[lead.id] = None

        context['leads'] = leads
        context['lead_followups'] = lead_followups

        return context



class CampaignDeleteView(OrganiserAndLoginRequiredMixin, generic.DeleteView):
    template_name = "campaigns/campaign_delete.html"
    context_object_name = "campaign"

    def get_success_url(self):
        return reverse("campaigns:campaign-list")

    def get_queryset(self):
        organisation = self.request.user.userprofile
        return Campaign.objects.filter(organisation = organisation)   


class CampaignAddAgentView(OrganiserAndLoginRequiredMixin, generic.FormView):
    template_name = "campaigns/campaign_add_agent.html"
    form_class = CampaignAddAgentModelForm

    
    def dispatch(self, request, *args, **kwargs):
        self.campaign_id = kwargs['pk']
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs['campaign_id'] = self.campaign_id
        return kwargs
    def get_success_url(self):
        return reverse("campaign:campaign-detail", kwargs={"pk": self.campaign_id})

    def form_valid(self, form):
        campaign = Campaign.objects.get(id=self.campaign_id)
        agents = form.cleaned_data['agent']
        
        for agent in agents:
            campaign.agent.add(agent)
            subject = 'New Campaign assigned to you.'
            body = 'A new campaign assigned to you by the admin, please visit the www.crm.addox.in to check it.'
            from_email = 'developer.addox@gmail.com'
            to_email = [agent.user.email]
            email = EmailMessage(subject, body, from_email, to_email)
            email.send()
        messages.success(self.request, "Agents added successfully.")
        return super().form_valid(form)

class AssignAgentView(OrganiserAndLoginRequiredMixin, generic.FormView):
    template_name = "campaigns/assign_agent.html"
    form_class = AssignAgentForm


    
    def get_form_kwargs(self,**kwargs):
        kwargs = super(AssignAgentView, self).get_form_kwargs(**kwargs)
        kwargs.update( {
            "request":self.request
        })
        return kwargs

        
    def get_success_url(self):
        return reverse("campaign:campaign-list")
    
    def form_valid(self, form):
        agent=form.cleaned_data["agent"]
        campaign = Campaign.objects.get(id=self.kwargs["pk"])
        print(campaign)
        campaign.agent = agent
        campaign.save()
        return super(AssignAgentView, self).form_valid(form)




# send mail 
# views.py

from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django.template.loader import get_template
from django.urls import reverse_lazy
from django.views.generic import FormView

from .forms import ContactForm

class ContactView(FormView):
    template_name = 'contactus.html'
    form_class = ContactForm
    success_url = reverse_lazy('contactus-page')

    def form_valid(self, form):
        name = form.cleaned_data['name']
        email = form.cleaned_data['email']
        phone = form.cleaned_data['phone']
        subject = form.cleaned_data['subject']
        message = form.cleaned_data['message']

        # Build the message
        template = get_template('email/contact.txt')
        context = {
            'name': name,
            'email': email,
            'phone': phone,
            'subject': subject,
            'message': message,
        }
        content = f"Name: {name}\nPhone: {phone}\nEmail: {email}\nSubject:{subject} \nMessage:{message}"
        print("send mail")
        # Send the email
        email = EmailMessage(
            subject=f'Contact form submission from KYBIC CRM',
            body=content,
            from_email='developer.addox@gmail.com', # replace with your email address
            to=['roufkpkp@gmail.com'], # replace with the recipient email address
            reply_to=[email],
            headers={'From': email}
        )
        email.send()

        return super().form_valid(form)
