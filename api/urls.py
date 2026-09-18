from django.urls import path
from .views import RouteOptimizeView

urlpatterns = [
    path('optimize/', RouteOptimizeView.as_view(), name='optimize-route'),
]