from api.views import StockPricesViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"stock_prices", StockPricesViewSet, basename="stock_prices")
urlpatterns = router.urls
