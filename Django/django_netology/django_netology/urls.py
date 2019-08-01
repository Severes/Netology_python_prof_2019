"""django_netology URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from app.views import hello_view, hello_name_view, since_view


urlpatterns = [
    path('hello/', hello_view, name='hello'),
    path('hello-name/', hello_name_view, name='hello-name'),
    path('since/<int:year>-<int:month>-<int:day>/', since_view, name='since'),
    path('admin/', admin.site.urls),
]
