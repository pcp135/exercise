from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'getfit.views.home'),
    url(r'^workout/(\d+)/$', 'getfit.views.workout'),
    url(r'^workout/add/$', 'getfit.views.add'),
    url(r'^workout/(\d+)/delete/$', 'getfit.views.delete'),
    url(r'^workout/(\d+)/edit/$', 'getfit.views.edit'),
		url(r'^my_admin/jsi18n', 'django.views.i18n.javascript_catalog'),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
