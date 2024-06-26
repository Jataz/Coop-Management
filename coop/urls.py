from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.index, name='dashboard'),
    #path('login/', views.UserLoginView.as_view(), name='login'),
    #path('register/', views.UserRegisterView.as_view(), name='register'),

    
    
    path("register/", views.signup, name="register"),
    path("verify-email/<slug:username>", views.verify_email, name="verify-email"),
    path("resend-otp/", views.resend_otp, name="resend-otp"),
    path("login/", views.signin, name="login"),
    path('logout/', views.user_logout_view, name='logout'),
]