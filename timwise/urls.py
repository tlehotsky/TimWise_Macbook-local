# timwise django app
# timwise.urls.py

# #from django.urls import path, include
##############*******************commenting out all per ChatGPT.....
# from django.urls import path, include
# from .views import UploadHighlights, FileUploadView, EditAuthorView, EditBookView, EditHighlightView, EditUserSettingsView, custom_logout
# from django.views.generic import TemplateView
# from django.http import HttpResponse
# import logging
# from django.conf import settings 
# from . import views  # new from AI, Import the views module from the current app
# from django.contrib.auth import views as auth_views
# from django.contrib.auth.views import LogoutView
# from timwise.views import *
# from django.shortcuts import redirect


# def redirect_logout(request):
#     return redirect('logout')

# urlpatterns = [
#     path('', views.home, name='home'),
#     path('logout/', LogoutView.as_view(template_name='logout.html'), name='logout'),
#     path('accounts/logout/', redirect_logout, name='accounts-logout'),  # Redirect accounts/logout to logout
#     path('accounts/', include('django.contrib.auth.urls')),  # Keep other auth URLs
#     # Add your other URL patterns here
#     # path('logout/', views.custom_logout, name='logout'),
#     path('upload/', FileUploadView.as_view(), name='upload'),
#     path('success/<str:filename>/<str:msg>/', TemplateView.as_view(template_name='success.html'), name='success'),
#     path('home/', views.home, name='home'),
#     path('edit-author/<int:id>/', EditAuthorView.as_view(), name='edit-author'),
#     path('edit-book/<int:id>/', EditBookView.as_view(), name='edit-book'),
#     path('mybooks/', views.mybooks, name='mybooks'),
#     path('myauthors/', views.myauthors, name='myauthors'),
#     path('why/', views.why, name='why'),
#     path('settings/', EditUserSettingsView.as_view(), name='settings'),
#     path('myhighlights/', views.myhighlights, name='myhighlights'),
#     path('signup/', views.signup, name='signup'),
#     path('instructions/', views.instructions, name='instructions'),
#     path('accounts/', include('django.contrib.auth.urls')),
#     path('edit_highlight/<int:pk>/', EditHighlightView.as_view(), name='edit_highlight'),
# ]
##############*******************commenting out all per ChatGPT.....


from django.urls import path, include
from .views import UploadHighlights, FileUploadView, EditAuthorView, EditBookView, EditHighlightView, EditUserSettingsView #, custom_logout
from django.views.generic import TemplateView
from django.conf import settings 
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.home, name='home'),
    path('logmeout/', views.logmeout, name='logmeout'),
    # path('logout/', custom_logout, name='logout'),
    path('accounts/', include('django.contrib.auth.urls')),    # Add your other URL patterns here
    path('upload/', FileUploadView.as_view(), name='upload'),
    path('success/<str:filename>/<str:msg>/', TemplateView.as_view(template_name='success.html'), name='success'),
    path('home/', views.home, name='home'),
    path('edit-author/<int:id>/', EditAuthorView.as_view(), name='edit-author'),
    path('edit-book/<int:id>/', EditBookView.as_view(), name='edit-book'),
    path('mybooks/', views.mybooks, name='mybooks'),
    path('myauthors/', views.myauthors, name='myauthors'),
    path('why/', views.why, name='why'),
    path('settings/', EditUserSettingsView.as_view(), name='settings'),
    path('myhighlights/', views.myhighlights, name='myhighlights'),
    path('signup/', views.signup, name='signup'),
    path('instructions/', views.instructions, name='instructions'),
    path('edit_highlight/<int:pk>/', EditHighlightView.as_view(), name='edit_highlight'),
]




# if settings.DEBUG:
#     import debug_toolbar
#     urlpatterns = [
#         path('__debug__/', include(debug_toolbar.urls)),
#     ] + urlpatterns

