from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ItemViewSet, LLMViewSet

router = DefaultRouter()
router.register(r'items', ItemViewSet)
router.register(r'llm', LLMViewSet, basename='llm')

urlpatterns = [
    path('', include(router.urls)),
] 