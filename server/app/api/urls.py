from django.urls import path
from .views import get_stocks,create_stock,update_stock,delete_stock, get_prediction

urlpatterns = [
    path('stocks/', get_stocks, name='get_stocks'),
    path('stocks/create/', create_stock, name='create_stock'),
    path('stocks/delete/<int:pk>', delete_stock, name='delete_stock'),
    path('stocks/update/<int:pk>', update_stock, name='update_stock'),
    path('stocks/predict/', get_prediction, name='predict_stock')
]
