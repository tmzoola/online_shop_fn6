from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('login/', views.login_page, name='login_page'),
    path('logout/', views.logout_page, name='logout'),
    path('product/<int:pk>', views.product, name='product'),
    path('category/<int:pk>', views.category, name='category'),
]