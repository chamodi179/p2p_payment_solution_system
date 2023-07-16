from django.urls import path
from . import views

urlpatterns = [
    path('loginpage',views.loginpage,name="loginpage"),
    path('',views.signuppage,name='signuppage'),
    path('dashboard',views.dashboard,name='dashboard'),
    path('money_transfer',views.money_transfer,name='money_transfer'),
    path('logout/', views.logout_view, name='logout')
]
