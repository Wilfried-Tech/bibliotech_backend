from rest_framework.routers import SimpleRouter

from users.views import UserViewSet

router = SimpleRouter()

router.register('users', UserViewSet, basename='users')

urlpatterns = router.urls
