from django.urls import path, include
from .views import MakeTransaction

urlpatterns = [
    path('make-transaction/', MakeTransaction.as_view(), name='make_transaction'),
]
