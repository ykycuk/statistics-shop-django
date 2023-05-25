from django.urls import path
from .views import (
    register, login, AuthenticatedUser, logout, PermissionAPIView, RoleViewSet, UserGenericAPIView, ProfileInfoAPIView,
    ProfileInfoAPIView, ProfilePasswordAPIView
)

urlpatterns = [
    path('register', register),
    path('login', login),
    path('logout', logout),
    path('user', AuthenticatedUser.as_view()), #as_view() because it is a class not a function
    path('permissions', PermissionAPIView.as_view()), #as_view() because it is a class not a function
    path('roles', RoleViewSet.as_view({
        'get': 'list',
        'post': 'create'
    })),
    path('roles/<str:pk>', RoleViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy'
    })),
    path('users/info', ProfileInfoAPIView.as_view()),
    path('users/password', ProfilePasswordAPIView.as_view()),
    path('users', UserGenericAPIView.as_view()),
    path('users/<str:pk>', UserGenericAPIView.as_view())
]
