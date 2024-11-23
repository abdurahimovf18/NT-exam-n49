from django.urls import path
from . import views


app_name = "products"


urlpatterns = [
    path("cart/", views.CartPageView.as_view(), name="cart"),
    # path("add_to_cart/", views.AddToCartView.as_view(), name="add_to_cart"),
    path("change_cart_quantity/", views.change_cart_quantity, name="change_cart_quantity"),
    path("set_cart_quantity", views.set_cart_quantity, name="set_cart_quantity"),
    path("categories/", views.CategoriesPageView.as_view(), name="categories"),
    path("", views.ProductsPageView.as_view(), name="products"),
    path("<int:pk>/", views.ProductDetailPageView.as_view(), name="product_detail"),
]
