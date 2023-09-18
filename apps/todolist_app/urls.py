from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.user_signup, name='user_signup' ),
    path('accounts/login/', views.user_login, name='user_login'), # must include accounts because @login_required in Django looks for this path
    path('logout/', views.user_logout, name='user_logout'),

    path('delete/<list_id>', views.delete, name="delete"),
    path('check_off/<list_id>', views.check_off, name='check_off'),
    path('uncheck/<list_id>', views.uncheck, name='uncheck'),
    path('edit/<list_id>', views.edit, name="edit"),
]
