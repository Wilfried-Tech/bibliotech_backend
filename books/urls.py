from rest_framework.routers import SimpleRouter

from books.views import CategoryViewSet, AuthorViewSet, BookViewSet

router = SimpleRouter()

router.register('categories', CategoryViewSet, basename='categories')
router.register('authors', AuthorViewSet, basename='authors')
router.register('books', BookViewSet, basename='books')

urlpatterns = router.urls
