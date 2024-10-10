from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginPage , name = 'login'),
    path('logout/', views.logoutUser , name = 'logout'),
    path('register/', views.registrationPage , name = 'register'),
    path('edit-profile/', views.update_user , name = 'edit-user'),

    path('', views.home, name='home'),
    path("room/<str:pk>/",views.room, name='room'),
    path("create_room/", views.create_room, name='create-room'),
    path("update_room/<str:pk>/", views.update_room, name='update-room'),
    path("delete_room/<str:pk>/", views.delete_room, name='delete-room'),
    path("delete_message/<str:pk>/", views.delete_message, name='delete-message'),


    path("user-profile/<str:pk>/", views.get_profile, name='user-profile'),
    path("topics-page/", views.topics_page, name='topics-page'),
    path("activity-page/", views.activity_page, name='activity-page'),
]