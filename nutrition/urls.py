from django.urls import path

from nutrition.views import FoodReserveViewSet, FoodViewSet, UserViewSet, Charge, Login

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
    'post': 'create',
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
charge_detail = Charge.as_view({
    'post': 'retrieve'
})

login = Login.as_view({
    'post': 'retrieve'
})

urlpatterns = [
    path('login/', login),
    path('charge/', charge_detail),
    path('user/', user_list, name='user-list'),
    path('user/<int:pk>/', user_detail, name='user-detail'),
    path('food/', food_list, name='food-list'),
    path('food/<int:pk>/', food_detail, name='food-detail'),
    path('food-reserve/', foodReserve_list, name='foodReserve-list'),
    path('food-reserve/<int:pk>/', foodReserve_detail, name='foodReserve-detail'),
]
