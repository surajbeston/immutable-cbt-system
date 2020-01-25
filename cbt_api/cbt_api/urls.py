"""cbt_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from api.views import create_examiner,save_score, rank_examiners, simple_get, get_user

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', create_examiner),
    path('submit-score/', save_score),
    path('rank/', rank_examiners),
    path('', simple_get),
    path('get/', get_user)
]
