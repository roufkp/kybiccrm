from django.urls import path
from .views import CampaignListView,CampaignCreateView,CampaignDetailView,CampaignUpdateView,CampaignDeleteView,AssignAgentView,CampaignAddAgentView


app_name = 'campaign'

urlpatterns = [
    path('',CampaignListView.as_view(), name='campaign-list'),
    path('<int:pk>/' , CampaignDetailView.as_view(),name='campaign-detail'),
    path('<int:pk>/update/',CampaignUpdateView.as_view(), name='campaign-update'),
    path('<int:pk>/delete/',CampaignDeleteView.as_view(), name='campaign-delete'),
    path('create/',CampaignCreateView.as_view(), name='campaign-create'),
    path('<int:pk>/assign-agent/', AssignAgentView.as_view(),name="assign-agent"),
    path("campaign/<int:pk>/add-agent/", CampaignAddAgentView.as_view(), name="campaign-add-agent"),
    




]