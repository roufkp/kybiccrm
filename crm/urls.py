from django.conf import settings
from django.conf.urls.static import static 
from django.contrib import admin
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView

    )
from django.urls import path, include
from leads.views import (
    landing_page,pricing_page,
    services_page,aboutus_page,
    contactus_page,
    LandingPageView,
    SignupView,
    dashboard,
    DashboardView,DownloadLeadsView,UploadCSVView,MatchFieldsView,ProcessDataView,
    # CreateNotificationView, MarkAsReadView, ClearNotificationsView,create_lead_notification
 )
from campaign.views import ContactView
from fb_app.views import fb_callback
# from whatsapp.views import whatsapp_callback





urlpatterns = [
    path('admin/', admin.site.urls),
    path('',landing_page , name="landing-page"),
    path('fb_callback/',fb_callback , name="fb_callback"),
    # path('whatsapp_callback/',whatsapp_callback , name="whatsapp_callback")
    # path('pricing/',pricing_page , name="pricing-page"),
    path('services/',services_page , name="services-page"),
    path('aboutus/',aboutus_page , name="aboutus-page"),
    # path('contactus/',contactus_page , name="contactus-page"),
    path('contactus/',ContactView.as_view() , name="contactus-page"),
    path('dashboard/',DashboardView.as_view() , name="dashboard"),
    # path('',LandingPageView.as_view() , name="landing-page"),
    path('leads/', include('leads.urls',namespace="leads")),
    path('agents/', include('agents.urls',namespace="agents")),
    path('membership/', include('membership.urls',namespace="membership")),
    path('campaigns/', include('campaign.urls',namespace="campaigns")),
    path('signup/',SignupView.as_view(),name='signup'),
    path('reset-password/', PasswordResetView.as_view(),name="reset-password"),
    path('password-reset-done/', PasswordResetDoneView.as_view(),name="password_reset_done"),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(),name="password_reset_comfirm"),
    path('password-reset-complete/', PasswordResetCompleteView.as_view(),name="password_reset_complete"),
    path('login/',LoginView.as_view(),name='login'),
    path('logout/',LogoutView.as_view(),name='logout'),
    # path('contact/',ContactUsView.as_view(), name='contact')
    path('download/', DownloadLeadsView.as_view(), name='download_leads'),
    # path('upload/', UploadCSVView.as_view(), name='upload'),
    path('upload/', UploadCSVView.as_view(), name='upload'),
    path('match-fields/', MatchFieldsView.as_view(), name='match-fields'),
    path('process-data/', ProcessDataView.as_view(), name='process-data'),
    # path('notifications/create/', CreateNotificationView.as_view(), name='create_notification'),
    # path('notifications/create/', create_lead_notification, name='create_notification'),
    # path('notifications/mark-as-read/<int:notification_id>/', MarkAsReadView.as_view(), name='mark_as_read'),
    # path('notifications/clear/', ClearNotificationsView.as_view(), name='clear_notifications'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

#considering production
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)