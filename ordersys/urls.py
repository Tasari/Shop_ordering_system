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
    path('managers/', views.ManagerMenuView.as_view(), name='manager_tab'),
    path('manage_orders/', views.ManageOrdersView.as_view(), name='manage_orders'),
    path('manage_order/<int:pk>', views.OrderDetailsView.as_view(), name='order_details'),
    path('manage_order/<int:pk>/edit', views.OrderUpdateView.as_view(), name='edit_order' ),
    path('manage_employees/', views.ManageEmployeesView.as_view(), name='manage_employees'),
    path('manage_employee/<int:pk>', views.EmployeeDetailsView.as_view(), name='employee_details'),
    path('manage_employee/<int:pk>/edit', views.EmployeeUpdateView.as_view(), name='edit_employee' ),
    path('manage_stock/', views.ManageStockView.as_view(), name="manage_stock"),
    path('manage_ingredient/<int:pk>', views.IngredientDetailsView.as_view(), name='ingredient_details'),
    path('manage_ingredient/<int:pk>/edit', views.IngredientUpdateView.as_view(), name='edit_ingredient' ),
    path('manage_ingredient/<int:pk>/restock', views.IngredientRestockView.as_view(), name='restock_ingredient'),
    path('archive/manage_today_orders/', views.OrderTodayView.as_view(), name="manage_today_orders"),
    path('archive/manage_archive/', views.ArchiveChoiceView.as_view(), name='archives'),
    path('archive/<int:year>/<int:month>/<int:day>/', views.OrderDayArchiveView.as_view(month_format='%m'), name="archive_day"),
    path('archive/week/<int:year>/<int:week>/', views.OrderWeekArchiveView.as_view(), name="archive_week"),
    path('archive/<int:year>/<int:month>/', views.OrderMonthArchiveView.as_view(month_format='%m'), name="archive_month"),
    path('archive/<int:year>/', views.OrderYearArchiveView.as_view(), name="archive_year"),
    path('report/manage_today_reports/', views.TransactionTodayView.as_view(), name="manage_today_reports"),
    path('report/manage_reports/', views.TransactionChoiceView.as_view(), name='reports'),
    path('report/<int:year>/<int:month>/<int:day>/', views.TransactionDayArchiveView.as_view(month_format='%m'), name="report_day"),
    path('report/week/<int:year>/<int:week>/', views.TransactionWeekArchiveView.as_view(), name="report_week"),
    path('report/<int:year>/<int:month>/', views.TransactionMonthArchiveView.as_view(month_format='%m'), name="report_month"),
    path('report/<int:year>/', views.TransactionYearArchiveView.as_view(), name="report_year"),
]
