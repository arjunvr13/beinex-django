from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('user.urls')),
    path('',include('transaction.urls')),
    path('',include('deposit.urls')),
    path('',include('loan.urls'))
]
