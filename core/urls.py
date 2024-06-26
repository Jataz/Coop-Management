
from django.contrib import admin
from django.views.generic import RedirectView
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('coop.urls')),
    path('', RedirectView.as_view(url='/login/')),
]
