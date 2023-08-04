import random
from django.shortcuts import render
from django.core.mail import send_mail
from django.views import generic
from django.shortcuts import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from leads.models import Agent
from .forms import AgentModelForm
from .mixins import OrganiserAndLoginRequiredMixin
from leads.models import Campaign
from django.http import Http404
from django.core.mail import EmailMessage
from django.views import generic
# from .models import Agent, Campaign

class AgentListView(OrganiserAndLoginRequiredMixin, generic.ListView):
    template_name = "agents/agent_list.html"

    def get_queryset(self):
        organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation=organisation)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        organisation = self.request.user.userprofile
        agents = Agent.objects.filter(organisation=organisation)
        agent_campaigns = {}

        for agent in agents:
            # Get the campaigns associated with the current agent
            campaigns = Campaign.objects.filter(agent=agent)
            agent_campaigns[agent] = campaigns

        context['agent_campaigns'] = agent_campaigns
        return context





class AgentCreateView(OrganiserAndLoginRequiredMixin, generic.CreateView):
    template_name = "agents/agent_create.html"
    form_class = AgentModelForm
    
    # print("Success! Agent created and email sent.")


    def get_success_url(self):
        return reverse("agents:agent-list")

    def form_valid(self,form):
        user = form.save(commit=False)
        user.is_agent = True
        user.is_organiser = False
        user.set_password(f"{random.randint(0,10000000)}")
        user.save()
        Agent.objects.create(
            user=user,
            organisation = self.request.user.userprofile
        )
                # Send email to the user using smtp
        subject = 'You are added to Kybic CRM'
        body = 'You are added to kybic CRM as a staff'
        from_email = 'developer.addox@gmail.com'
        to_email = [user.email]
        email = EmailMessage(subject, body, from_email, to_email)
        email.send()

        # agent.organisation = self.request.user.userprofile
        # agent.save()
        # print("Success! Agent created and email sent.")
        return super(AgentCreateView,self).form_valid(form)






# class AgentDetailView(OrganiserAndLoginRequiredMixin, generic.DetailView):
#     template_name = "agents/agent_detail.html"
#     context_object_name = "agent"

#     def get_queryset(self):
#         organisation = self.request.user.userprofile
#         return Agent.objects.filter(organisation = organisation)

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         agent = self.get_object()
#         campaigns = Campaign.objects.filter(agent=agent)
#         context['campaigns'] = campaigns
#         return context

class AgentDetailView(OrganiserAndLoginRequiredMixin, generic.DetailView):
    template_name = "agents/agent_detail.html"
    context_object_name = "agent"

    def get_queryset(self):
        organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation=organisation)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        agent = self.get_object()
        campaigns = Campaign.objects.filter(agent=agent)
        context['campaigns'] = campaigns
        return context


class AgentUpdateView(OrganiserAndLoginRequiredMixin, generic.UpdateView):
    template_name = "agents/agent_update.html"
    form_class = AgentModelForm

    def get_success_url(self):
        return reverse("agents:agent-list")

    def get_queryset(self):
        organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation = organisation)

    def get_object(self, queryset=None):
        # Get the specific Agent object you want to update
        obj = super().get_object(queryset=queryset)
        return obj
    # def get_form_kwargs(self):
    #     kwargs = super().get_form_kwargs()
    #     kwargs['user'] = self.request.user
    #     return kwargs   



class AgentDeleteView(OrganiserAndLoginRequiredMixin, generic.DeleteView):
    template_name = "agents/agent_delete.html"
    context_object_name = "agent"

    def get_success_url(self):
        return reverse("agents:agent-list")

    def get_queryset(self):
        organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation = organisation)   
