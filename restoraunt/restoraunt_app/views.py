from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView
from django.views import View
from django.urls import reverse_lazy
from .models import Dish, Review, Order, OrderItem
from .forms import OrderForm, ReviewForm


# -----------------------------
# HOME
# -----------------------------
class HomeView(ListView):
    model = Dish
    template_name = "home.html"
    context_object_name = "dishes"

    def get_queryset(self):
        return Dish.objects.filter(is_available=True).order_by("-created_at")[:8]


# -----------------------------
# MENU
# -----------------------------
class MenuView(ListView):
    model = Dish
    template_name = "menu/menu.html"
    context_object_name = "dishes"


class DishDetailView(DetailView):
    model = Dish
    template_name = "menu/dish_detail.html"
    context_object_name = "dish"


# -----------------------------
# SESSION CART
# -----------------------------
def get_cart(session):
    return session.get("cart", {})


def save_cart(session, cart):
    session["cart"] = cart
    session.modified = True


class CartView(View):
    template_name = "cart/cart.html"

    def get(self, request):
        cart = get_cart(request.session)
        items = []
        total = 0

        for dish_id, quantity in cart.items():
            dish = Dish.objects.get(id=dish_id)
            total += dish.price * quantity
            items.append({"dish": dish, "quantity": quantity, "total": dish.price * quantity})

        return render(request, self.template_name, {"items": items, "total": total})


class AddToCartView(View):
    def post(self, request, dish_id):
        cart = get_cart(request.session)
        cart[str(dish_id)] = cart.get(str(dish_id), 0) + 1
        save_cart(request.session, cart)
        return redirect("cart")


class RemoveFromCartView(View):
    def post(self, request, item_id):
        cart = get_cart(request.session)
        cart.pop(str(item_id), None)
        save_cart(request.session, cart)
        return redirect("cart")


# -----------------------------
# CHECKOUT
# -----------------------------
class CheckoutView(CreateView):
    model = Order
    form_class = OrderForm
    template_name = "order/checkout.html"
    success_url = reverse_lazy("order_success")

    def form_valid(self, form):
        cart = get_cart(self.request.session)

        order = form.save(commit=False)
        total = 0
        for dish_id, quantity in cart.items():
            dish = Dish.objects.get(id=dish_id)
            total += dish.price * quantity
        order.total_price = total
        order.save()

        for dish_id, quantity in cart.items():
            dish = Dish.objects.get(id=dish_id)
            OrderItem.objects.create(
                order=order,
                dish=dish,
                quantity=quantity,
                price_at_time=dish.price
            )

        save_cart(self.request.session, {})
        return super().form_valid(form)


def order_success(request):
    return render(request, "order/success.html")
