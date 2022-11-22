from django.urls import path
from . import views

urlpatterns = [
    path('',views.adminlogin,name='adminlogin'),
    path('/admindashboard',views.admindashboard,name='admindashboard'),
    path('/adminuser',views.adminuser,name='adminuser'),
    path('/adminblock/<int:id>/',views.adminblock,name='adminblock'),
    path('/adminlogout',views.adminlogout,name='adminlogout'),
    path('/admincategory',views.admincategory,name='admincategory'),
    path('/adminproduct',views.adminproduct,name='adminproduct'),
    path('/admin_addproduct',views.admin_addproduct,name='admin_addproduct'),
    path('/edit_product/<int:id>/',views.edit_product,name='edit_product'),
    path('/delete_product/<int:id>/',views.delete_product,name='delete_product'),
    path('/edit_category/<int:id>/',views.edit_category,name='edit_category'),
    path('/delete_category/<int:id>/',views.delete_category,name='delete_category'),
    path('/order_list',views.order_list,name='order_list'),
    path('/status_update',views.status_update,name='status_update'),
    path('/coupon',views.coupon,name='coupon'),
    path('/edit_coupon/<int:id>/',views.edit_coupon,name='edit_coupon'),
    path('/delete_coupon/<int:id>/',views.delete_coupon,name='delete_coupon'),

]