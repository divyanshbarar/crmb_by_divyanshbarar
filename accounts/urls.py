from django.urls import path
from . import views

admin.site.site_header="Customer Relationship MAnagement"
admin.site.site_title=" Welcome Divyansh"
admin.site.index_title="Backend Of CRM"

urlpatterns = [

    path('register/',views.registerPage,name='register'),
    path('login/',views.loginPage,name='login'),
    path('logout/',views.logoutUser,name='logout'),

    path('',views.home,name='home'),
    path('user/',views.userPage,name='user-page'),
    path('products/',views.products,name='products'),
    path('customer/<str:pk>/',views.customer,name='customer'),
    path('account/',views.accountSettings,name='account'),

    path('create_order/<str:pk_test>/',views.createOrder,name='create_order'),
    path('update_order/<str:pk_test>/',views.updateOrder,name='update_order'),
    path('delete_order/<str:pk_test>/',views.deleteOrder,name='delete_order'),
]
