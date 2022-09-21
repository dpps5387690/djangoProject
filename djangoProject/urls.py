"""djangoProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from djangotest import views
from django.conf.urls import url
from django.contrib import admin
from django.urls import path

urlpatterns = [
    # path('admin/', admin.site.urls),
    # path('index_Test/', views.index_Test),
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index_Test, name='index_Test'),
    url(r'^get_table/$', views.get_table, name='get_table'),
    url(r'^get_table_data/$', views.get_table_data, name='get_table_data'),
    url(r'^search_data_row/$', views.search_data_row, name='search_data_row'),
    url(r'^get_now_Status/$', views.get_now_Status, name='get_now_Status'),
    url(r'^multi_Files_Upload/$', views.multi_Files_Upload, name='multi_Files_Upload'),
]
