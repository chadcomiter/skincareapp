"""skinsavev2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from main import views
from main.views import ProductDetailView, ProductUpdateView, ProductDeleteView, IngredientDeleteView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='homepage'),
    path('register/', views.register, name='register'),
    path('logout', views.logout_request, name='logout'),
    path('login', views.login_request, name='login'),
    path('product_list/', views.product_list, name='product_list'),
    path('product_list/<pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('product_list/<pk>/update', ProductUpdateView.as_view(), name='product_update'),
    path('product_list/<pk>/delete', ProductDeleteView.as_view(), name='product_delete'),
    path('create_product/', views.create_product, name='create_product'),
    path('create_ingredient/', views.create_ingredient, name='create_ingredient'),
    path('<pk>/delete', IngredientDeleteView.as_view(), name='ingredient_delete'),
    path('classifier/', views.classifier, name='classifier'),
    path('support/', views.support, name='support'),
]
