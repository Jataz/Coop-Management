from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.index, name='dashboard'),
    
    #Loan urls
    path('loan-transactions/', views.loan_transactions, name='loan-transactions'),
    path('loan-application/', views.loan_application, name='loan-application'),
    path('loan-apply/', views.loan_apply, name='loan-apply'),
    path('loan-payment/', views.loan_payment, name='loan-payment'),
    path('loan-confirm/', views.confirm_loan, name='loan-confirm'),
    path('loan-details/<int:pk>/', views.loan_details, name='loan-details'),
    path('loan-repay/<int:pk>/', views.repay_loan, name='loan-repay'),

    #Subscription Urls
    path('subscriptions-payment', views.subscriptions_payment, name='subscriptions-payment'),
    path('subscriptions-transactions', views.subscriptions_transactions, name='subscriptions-transactions'),

    #Share Capital
    path('share-capital-payment', views.share_payment, name='share-capital-payment'),
    path('share-capital-transactions', views.share_transactions, name='share-capital-transactions'),
    
    #Profile
    path('user-profile', views.user_profile, name='user-profile'),
    path('edit-profile',views.edit_profile, name='edit-profile'),
    path('change-password', views.change_password, name='change-password'),
    
    #User Registration
    path("register/", views.signup, name="register"),
    path("verify-email/<slug:username>", views.verify_email, name="verify-email"),
    path("resend-otp/", views.resend_otp, name="resend-otp"),
    path("login/", views.signin, name="login"),
    path('logout/', views.user_logout_view, name='logout'),
]