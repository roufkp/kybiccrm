from django.urls  import path
from .views import (
    lead_list,lead_detail,lead_update,lead_delete,
    LeadListView,LeadDetailView,LeadCreateView,LeadUpdateView,LeadDeleteView,CategoryListView,
    # CategoryDetailView,CategoryCreateView,CategoryUpdateView,CategoryDeleteView,
    LeadCategoryUpdateView,
    FollowUpCreateView,FollowUpUpdateView, FollowUpDeleteView,FollowUpListView,DownloadLeadsView,
    # WhatsappMessagingView,
    lead_form_submissions,
    )
from django.conf.urls import handler404,handler400,handler403,handler500
from leads.views import error_404,error_400,error_403,error_500,error_401,error_405
# from campaign.views import AssignAgentView

handler404 = error_404
handler400 = error_400
handler403 = error_403
handler401 = error_401
handler405 = error_405
handler500 = error_500


app_name = "leads"

urlpatterns = [
    path('',LeadListView.as_view(),name="lead-list"),
    path('facebook/',lead_form_submissions,name="facebook-lead-list"),
    # path('<int:campaign_id>/<int:pk>/',LeadDetailView.as_view(),name="lead-detail"),
    path('<int:campaign_id>/<int:pk>/', LeadDetailView.as_view(), name="lead-detail"),
    path('<int:campaign_id>/<int:pk>/update/', LeadUpdateView.as_view(),name="lead-update"),
    path('<int:campaign_id>/<int:pk>/delete/', LeadDeleteView.as_view(),name="lead-delete"),
    # path('<int:pk>/assign-agent/', AssignAgentView.as_view(),name="assign-agent"),
    path('<int:campaign_id>/<int:pk>/category/', LeadCategoryUpdateView.as_view(),name="lead-category-update"),
    path('leads/followups/', FollowUpListView.as_view(), name='followup-list'), 
    # path('<int:campaign_id>/followups/', FollowUpView.as_view(), name='followup-leads'),
    path('<int:campaign_id>/<int:pk>/followups/create/', FollowUpCreateView.as_view(), name='lead-followup-create'),    
    path('followups/<int:campaign_id>/<int:pk>/update/', FollowUpUpdateView.as_view(), name='lead-followup-update'),
    path('followups/<int:pk>/delete/', FollowUpDeleteView.as_view(), name='lead-followup-delete'),
    path('<int:pk>/create/', LeadCreateView.as_view(),name="lead-create"),
    # path('<int:pk>/whatsapp/', WhatsappMessagingView.as_view(), name='lead-whatsapp'),
    # path('create-category/', CategoryCreateView.as_view(),name="category-create"),
    path('categories/' , CategoryListView.as_view(), name="category-list"),
    # path('categories/<int:pk>/update/' ,CategoryUpdateView.as_view(), name="category-update"),
    # path('categories/<int:pk>/delete/', CategoryDeleteView.as_view(),name="category-delete"),
    # path('categories/' , CategoryDetailView.as_view(), name="category-detail"),
    # path('upload/', UploadFileView.as_view(), name='upload'),


]