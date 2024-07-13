from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.index, name='dashboard'),
    
    path('loan-transactions/', views.loan_transactions, name='loan-transactions'),
    path('loan-application/', views.loan_application, name='loan-application'),
    path('loan-apply/', views.loan_apply, name='loan-apply'),
    path('loan-payment/', views.loan_payment, name='loan-payment'),
    path('loan-confirm/', views.confirm_loan, name='loan-confirm'),
    path('loan-status/<int:pk>/', views.loan_status, name='loan-status'),
    path('loan-repay/<int:pk>/', views.repay_loan, name='loan-repay'),

    
    path('subscriptions-payment', views.subscriptions_transactions, name='subscriptions-payment'),
    path('subscriptions-transactions', views.subscriptions_transactions, name='subscriptions-transactions'),
    #path('login/', views.UserLoginView.as_view(), name='login'),
    #path('register/', views.UserRegisterView.as_view(), name='register'),

    
    
    path("register/", views.signup, name="register"),
    path("verify-email/<slug:username>", views.verify_email, name="verify-email"),
    path("resend-otp/", views.resend_otp, name="resend-otp"),
    path("login/", views.signin, name="login"),
    path('logout/', views.user_logout_view, name='logout'),
]