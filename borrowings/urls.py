from django.urls import path
from rest_framework.routers import SimpleRouter

from borrowings.views import BorrowingViewSet, CreateBorrowAPIView

router = SimpleRouter()

router.register('borrowings', BorrowingViewSet, basename='borrowings')

urlpatterns = [
    path('books/<int:pk>/borrow/', CreateBorrowAPIView.as_view(), name='borrowings-borrow')
]

urlpatterns += router.urls
