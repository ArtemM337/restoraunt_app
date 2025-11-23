from django.urls import path
from .views import (
    HomeView, MenuView, DishDetailView,
    CartView, AddToCartView, RemoveFromCartView,
    CheckoutView, order_success
)
from .views import RegisterView, CustomLoginView
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path("", HomeView.as_view(), name="home"),

    path("menu/", MenuView.as_view(), name="menu"),
    path("dish/<int:pk>/", DishDetailView.as_view(), name="dish_detail"),

    path("cart/", CartView.as_view(), name="cart"),
    path("cart/add/<int:dish_id>/", AddToCartView.as_view(), name="add_to_cart"),
    path("cart/remove/<int:item_id>/", RemoveFromCartView.as_view(), name="remove_from_cart"),

    path("checkout/", CheckoutView.as_view(), name="checkout"),
    path("checkout/success/", order_success, name="order_success"),

    path("register/", RegisterView.as_view(), name="register"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(next_page="home"), name="logout"),

]
