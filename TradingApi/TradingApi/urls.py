
from django.contrib import admin
from django.urls import path,include
from rest_framework.routers import DefaultRouter
from journal.views import TradeViewSet, StrategyViewSet

router = DefaultRouter()
router.register(r"trades", TradeViewSet, basename='trades')
router.register(r"strategies", StrategyViewSet, basename='strategies')  


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/auth/', include('journal.urls')),
]
