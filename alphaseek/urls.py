"""alphaseek URL Configuration

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
from api import views
from django.conf.urls import include, url

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'crud_exchange/', views.crud_exchange, name='crud_exchange'),
    url(r'crud_company/', views.crud_company, name='crud_company'),
    url(r'crud_company_prices/', views.crud_company_prices, name='crud_company_prices'),
    url(r'crud_index_prices/', views.crud_index_prices, name='crud_index_prices'),
    url(r'crud_index/', views.crud_index, name='crud_index'),
    url(r'read_strategies/', views.read_strategies, name='read_strategies'),
    url(r'read_strategy_returns/', views.read_strategy_returns, name='read_strategy_returns'),
    url(r'read_strategy_compare/', views.read_strategy_returns_multi, name='read_strategy_returns_multi'),
]

