from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.homepage, name='home'),
    path('accountSettings/', views.accountSettings, name='accountSettings'),
    path('posts/', views.post, name='post'),
    path('personal_post/<id>', views.personalposts, name = 'personal_post'),
    path('delete_post/<id>',views.post_delete,name="post_delete"),
    path('room/',views.room , name='room'),
    path("chat/<str:room_name>/", views.chat, name="room"),

]