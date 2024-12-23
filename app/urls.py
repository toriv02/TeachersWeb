"""
URL configuration for app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path,include
from teachers import views
from django.conf.urls.static import static

from rest_framework.routers import DefaultRouter

from teachers.api import *

router=DefaultRouter()
router.register(r'subjects',SubjectViewSet)
router.register(r'records',RecordViewSet)
router.register(r'files',FileViewSet)
router.register(r'feedbacks',FeedbackViewSet)
router.register(r'reviews',ReviewViewSet)
router.register(r'documents', DocumentViewSet)
router.register(r'schools', SchoolViewSet)
router.register(r'user', UserViewSet)




urlpatterns = [
    path('',views.message),
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)