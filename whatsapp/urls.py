from django.urls  import path
from .views import (
    LeadListView
    
    )
# from campaign.views import AssignAgentView


app_name = "whatsapp"

urlpatterns = [
    path('',LeadListView.as_view(),name="lead-list"),
    
]