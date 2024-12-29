# timwise django app
# timwise.urls.py
# Git update
# more git updates
# even more git updates

#latest git test


from django.urls import path, include
from .views import UploadHighlights, FileUploadView
from django.views.generic import TemplateView
from django.http import HttpResponse
import logging
from django.conf import settings 
from . import views  # new from AI, Import the views module from the current app

logger = logging.getLogger(__name__)

def test_logging(request):
    print("PRINT: Test view executed")
    logger.debug("DEBUG: Test view executed")
    logger.info("INFO: Test view executed")
    logger.warning("WARNING: Test view executed")
    logger.error("ERROR: Test view executed")
    return HttpResponse("Test view executed - check your console")

urlpatterns = [
    path('test-logging/', test_logging, name='test-logging'),
    path('upload/', FileUploadView.as_view(), name='upload'),
    path('success/<str:filename>/<str:msg>/', TemplateView.as_view(template_name='success.html'), name='success'),
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('why/', views.why, name='why'),
    path('settings/', views.settings, name='settings'),
    path('myhighlights/', views.myhighlights, name='myhighlights'),
    path('logout/', views.logout, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('instructions/', views.instructions, name='instructions'),
    path('accounts/', include('django.contrib.auth.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

