from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ItemViewSet, LLMViewSet, DocumentProcessingViewSet

router = DefaultRouter()
router.register(r'items', ItemViewSet)
router.register(r'llm', LLMViewSet, basename='llm')
router.register(r'documents', DocumentProcessingViewSet, basename='documents')

urlpatterns = [
    path('', include(router.urls)),
] 