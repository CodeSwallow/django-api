from django.urls import path, include
from rest_framework.routers import DefaultRouter

from activities.views import ActivityListViewSet, ActivityItemViewSet


router = DefaultRouter()
router.register(r'lists', ActivityListViewSet, basename='list')
router.register(r'items', ActivityItemViewSet, basename='item')


urlpatterns = [
    path('', include(router.urls))
]
