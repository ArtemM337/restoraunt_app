from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView
from django.views import View
from django.urls import reverse_lazy
from .models import Dish, Review, Order, OrderItem
from .forms import OrderForm, ReviewForm
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.views import View

from .forms import RegisterForm, LoginForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import RegisterForm, LoginForm, OrderForm, ReviewForm, SearchForm







class OrderHistoryView(LoginRequiredMixin, ListView):
    model = Order
    template_name = "order/history.html"
    context_object_name = "orders"

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by("-created_at")


class HomeView(ListView):
    model = Dish
    template_name = "home.html"
    context_object_name = "dishes"

    def get_queryset(self):
        return Dish.objects.filter(is_available=True).order_by("-created_at")[:8]



class MenuView(ListView):
    model = Dish
    template_name = "menu/menu.html"
    context_object_name = "dishes"

    def get_queryset(self):
        queryset = Dish.objects.all()

        query = self.request.GET.get("query", "")
        if query:
            queryset = queryset.filter(name__icontains=query)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_form"] = SearchForm(self.request.GET or None)
        return context



class DishDetailView(DetailView):
    model = Dish
    template_name = "menu/dish_detail.html"
    context_object_name = "dish"



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
        order.user = self.request.user if self.request.user.is_authenticated else None

        save_cart(self.request.session, {})
        return super().form_valid(form)


def order_success(request):
    return render(request, "order/success.html")


class RegisterView(View):
    template_name = "auth/register.html"

    def get(self, request):
        form = RegisterForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
        return render(request, self.template_name, {"form": form})


class CustomLoginView(LoginView):
    template_name = "auth/login.html"
    authentication_form = LoginForm

def search_dishes(request):
    query = request.GET.get("q", "")
    dishes = Dish.objects.filter(name__icontains=query)

    return render(request, "menu/search_results.html", {
        "query": query,
        "dishes": dishes
    })


class MenuByCategoryView(ListView):
    template_name = "menu/menu_category.html"
    context_object_name = "dishes"

    def get_queryset(self):
        category_id = self.kwargs["category_id"]
        return Dish.objects.filter(category_id=category_id)
