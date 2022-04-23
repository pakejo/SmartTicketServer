from rest_framework.routers import DefaultRouter

from . import viewsets

router = DefaultRouter()

router.register(r'events', viewsets.EventsViewsets, basename="events")

urlpatterns = router.urls
