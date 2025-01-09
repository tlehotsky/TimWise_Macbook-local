"""django_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path, include
from debug_toolbar.toolbar import debug_toolbar_urls
from . import views
from django.conf import settings
from django.shortcuts import redirect
# from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('', lambda request: redirect('http://134.209.220.170/instructions/home/', permanent=True)),  # Redirect home page
    path('accounts/', include('django.contrib.auth.urls')),
    # path('logout/', LogoutView.as_view(template_name='logout.html'), name='logout'),

    path('admin/', admin.site.urls),
    path("timwise/", include("timwise.urls")),
    path('', include('timwise.urls')),  # chat gpt new

] 

# if settings.DEBUG:
#     import debug_toolbar
#     urlpatterns += [
#         path('__debug__/', include(debug_toolbar.urls)),
#     ]


