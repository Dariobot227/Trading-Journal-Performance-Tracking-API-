
from django.contrib import admin
from django.urls import path,include
from rest_framework.routers import DefaultRouter
from journal.views import TradeViewSet, StrategyViewSet,ProfileViewSet,Homepage
from rest_framework.authtoken.views import obtain_auth_token

router = DefaultRouter()
router.register(r"trades", TradeViewSet, basename='trades')
router.register(r"strategies", StrategyViewSet, basename='strategies')  
router.register(r"profile", ProfileViewSet, basename="profile")

urlpatterns = [
    path('', Homepage.as_view(), name='home'),
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/auth/', include('journal.urls')),
    path('api/login/', obtain_auth_token),
]
