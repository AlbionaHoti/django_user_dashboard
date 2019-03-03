from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^create/$', views.create, name="create"),
    url(r'^create_user/$', views.create_user, name="create_user"),
    url(r'^dashboard/$', views.dashboard, name="dashboard"),
    url(r'^logout/$', views.logout, name="logout"),
    url(r'^login/$', views.login, name="login"),
    url(r'^signin/$', views.signin, name="signin"),
    url(r'^register/$', views.register, name="register"),    
    url(r'^new/$', views.new, name="new"),    
    url(r'^remove/(?P<user_id>\d+)/$', views.remove, name="remove"),    
    url(r'^edit/(?P<user_id>\d+)/$', views.edit, name="edit"),
    url(r'^edit_personal_info/(?P<user_id>\d+)/$', views.edit_personal_info, name="edit_personal_info"),    
    url(r'^edit_passwords/(?P<user_id>\d+)/$', views.edit_passwords, name="edit_passwords"),
    url(r'^edit_description/(?P<user_id>\d+)/$', views.edit_description, name="edit_description"),
    url(r'^wall/$', views.wall, name="wall"),
    url(r'^message/$', views.message, name="message"),
    url(r'^(?P<message_id>\d+)/comment$', views.comment, name="comment"),
    url(r'^(?P<comment_id>\d+)/delete_comment$', views.delete_comment, name="delete_comment")
]