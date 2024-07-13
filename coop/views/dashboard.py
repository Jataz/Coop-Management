from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

@login_required(login_url="/login")
def index(request):

    return render(request, 'pages/dashboard/index.html')