from rest_framework import routers

from smarticket_api.views import *

router = routers.DefaultRouter()
router.register(r'events', EventsViewSets, basename='Events')
router.register(r'sales', SalesViewSets, basename='Sales')
router.register(r'users', UsersViewSets, basename='Users')

urlpatterns = router.urls
