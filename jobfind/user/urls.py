from django.urls import path, include
from . import views

urlpatterns = [
    path('signup/',views.signup,name='signup'),
    path('login/',views.userlogin,name='login'),
    path('',views.home_view,name='home'),
    path('admin-login-page/',views.viewadminlogin,name='admin_login_page'),
    path('admin-dash',views.admindash,name='admin_dash'),
    path('adlogin/',views.admin_login,name='ad_login')
]
