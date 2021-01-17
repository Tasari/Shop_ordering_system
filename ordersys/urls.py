from django.urls import path

from . import views

app_name = 'ordersys'

urlpatterns = [
    path('orders/', views.OrdersView.as_view(), name='index'),
    path('orders/pending/', views.PendingOrdersView.as_view(), name='pending'),
    path('orders/<int:pk>/start_preparing/', views.start_preparing_order, name='start_preparing'),
    path('orders/<int:pk>/finish_preparing/', views.finish_preparing_order, name='finish_preparing'),
    path('orders/<int:pk>/collect_order/', views.collected_order, name='collect_preparing'),
    path('orders/prepare/', views.PrepareOrdersView.as_view(), name='prepare'),
    path('orders/collect/', views.CollectOrdersView.as_view(), name='collect'),
    path('orders/done/', views.DoneOrdersView.as_view(), name='done'),
    path('orders/failed/', views.FailedOrdersView.as_view(), name='failed'),
    path('orders/customers/', views.CustomersOrdersView.as_view(), name='customers'),
    path('orders/create/', views.CreateOrderView.as_view(), name='create'),
    path('login/', views.LogView.as_view(), name='login'),
    path('managers/', views.ManagerMenuView.as_view(), name='manager_tab')

]
