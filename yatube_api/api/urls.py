from django.urls import path, include
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter

from .views import PostViewSet, GroupViewSet, CommentViewSet

API_VERSION = 'v1/'

router_v1 = DefaultRouter()
router_v1.register(r'posts', PostViewSet, basename='post')
router_v1.register(r'groups', GroupViewSet, basename='group')
router_v1.register(
    r'posts/(?P<post_id>\d+)/comments', CommentViewSet, basename='comment'
)

urlpatterns = [
    path(API_VERSION, include(router_v1.urls)),
    path(
        f'{API_VERSION}api-token-auth/',
        views.obtain_auth_token,
        name='api_token_auth'
    ),
]
