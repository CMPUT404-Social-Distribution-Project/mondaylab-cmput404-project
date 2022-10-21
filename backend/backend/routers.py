from rest_framework.routers import SimpleRouter
from author.views import UserViewSet
from auth.views import LoginViewSet, RegistrationViewSet, RefreshViewSet


routes = SimpleRouter()

# AUTHENTICATION
routes.register(r'auth/login', LoginViewSet, basename='auth-login')
routes.register(r'auth/register', RegistrationViewSet, basename='auth-register')
routes.register(r'auth/refresh', RefreshViewSet, basename='auth-refresh')

# AUTHORS
routes.register(r'authors', UserViewSet, basename='authors')


urlpatterns = [
    *routes.urls
]
