from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^shop$', views.shop, name='shop'),
    url(r'^about$', views.about, name='about'),
    url(r'^contact$', views.contact, name='contact'),
    url(r'^login$',views.login, name='login'),
    url(r'^signup$',views.register,name='signup'),
    url(r'^logout$',views.logout,name='logout'),
    url(r'^adminpage$',views.admin,name='adminPage'),
    url(r'^prodmanagement$',views.productManagement,name='prod'),
    url(r'^prodmanagement/edit/(?P<id>[0-9]+)$',views.productManagementEdit,name='prodEdit')
]