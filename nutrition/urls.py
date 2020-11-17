from django.urls import include, path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register('programs', views.FoodProgramViewSet)

# Wire up our API using automatic URL routing.
# TODO: All routes must check sent JWT and authenticate it automatically
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('programs/', views.FoodProgramViewSet.as_view)
]
