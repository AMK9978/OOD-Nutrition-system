from django.urls import path

from nutrition.views import FoodReserveViewSet, FoodViewSet, UserViewSet

food_list = FoodViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
food_detail = FoodViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})
foodReserve_list = FoodReserveViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
foodReserve_detail = FoodReserveViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})
user_list = UserViewSet.as_view({
    'get': 'list',
})
user_detail = UserViewSet.as_view({
    'get': 'retrieve'
})

urlpatterns = [
    path('user/', user_list, name='user-list'),
    path('user/<int:pk>/', user_detail, name='user-detail'),
    path('food/', food_list, name='food-list'),
    path('food/<int:pk>/', food_detail, name='food-detail'),
    path('food-reserve/', foodReserve_list, name='foodReserve-list'),
    path('food-reserve/<int:pk>/', foodReserve_detail, name='foodReserve-detail'),
]
