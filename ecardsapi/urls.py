"""ecardsapi URL Configuration

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
from django.conf import settings
from django.urls import include, path
from api import views as api_views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('cards', api_views.CardViewSet, basename="card")
router.register('users', api_views.UserViewSet, basename="card")
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include ('djoser.urls')),
    path('api/', include(router.urls)),
    path('api/auth/', include('djoser.urls.authtoken')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/user_cards/<str:username>/', api_views.UserCardsView.as_view(), name='api_user_cards'),
    path('api/following/', api_views.FollowingView.as_view(), name='api_following'),
    path('api/remove_follow/<str:username>/', api_views.RemoveFollowView.as_view(), name="remove_followed_user"),
    

]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),

        # For django versions before 2.0:
        # url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
