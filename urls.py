from django.conf.urls import patterns, url
from sesar_mobile import views

urlpatterns = patterns('',
    # url(r'^thingie/', include(api.urls)),
    url(r'^ingest/$', views.RecordIngestView.as_view(), name="sesarmobileingest"),
    url(r'^index/$', views.IndexView.as_view(), name='sesarmobileindex'),
    url(r'^register/$', views.RegistrationView.as_view(), name='sesarmobileregister'),
    url(r'^logout/$', views.LogoutView.as_view(), name='sesarmobilelogout'),
    url(r'^$', views.LoginView.as_view(), name='sesarmobilelogin'),

)
