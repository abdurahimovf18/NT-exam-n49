from typing import Any
from django.db.models.query import QuerySet
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, redirect

from .models import CategoryModel, ProductModel, OrderModel
from .forms import OrderForm



UserModel = get_user_model()


def get_next_page(request):
    return request.POST.get("next", None) or request.GET.get("next", None) or "/"


class CartPageView(LoginRequiredMixin, ListView):
    template_name = "cart.html"
    model = OrderModel
    context_object_name = "objects"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        
        data = {
            self.context_object_name: self.request.user.orders.all(),
            "total_price": sum((order.total_price for order in self.request.user.orders.all()))
        }

        data["total_amount"] = data["total_price"] + 10

        return data
    

@login_required
def change_cart_quantity(request):

    if request.method != "POST":
        return redirect(get_next_page(request))

    form = OrderForm(request.POST)
    
    if form.is_valid():
        data = form.cleaned_data

        product_id = data["product_id"]
        target_product = get_object_or_404(ProductModel, id=product_id)

        user = request.user

        order, _ = OrderModel.objects.get_or_create(user=user, product=target_product)
        order.quantity += data["quantity"]

        if order.quantity <= 0:
            order.delete()
        else:
            order.save()

    return redirect(get_next_page(request))


@login_required
def set_cart_quantity(request):

    if request.method != "POST":
        return redirect(get_next_page(request))

    form = OrderForm(request.POST)
    
    if form.is_valid():
        data = form.cleaned_data

        product_id = data["product_id"]
        target_product = get_object_or_404(ProductModel, id=product_id)

        user = request.user

        order, _ = OrderModel.objects.get_or_create(user=user, product=target_product)
        order.quantity = data["quantity"]

        if data["quantity"] < 1:
            order.delete()
        else:
            order.save()

    return redirect(get_next_page(request))


class CategoriesPageView(ListView):
    template_name = "categories.html"
    model = CategoryModel
    paginate_by = 6
    context_object_name = "objects"


class ProductsPageView(ListView):
    template_name = "products.html"
    model = ProductModel
    paginate_by = 6
    context_object_name = "objects"

    def get_queryset(self) -> QuerySet[Any]:
        category_name = self.request.GET.get("category", "")
        product_name = self.request.GET.get("search", "")

        if category_name:
            queryset = self.model.objects.filter(categories__name__icontains=category_name)
        else:
            queryset = self.model.objects.all()

        if product_name:
            queryset = queryset.filter(name__icontains=product_name)
        
        return queryset

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        category_name = self.request.GET.get("category", "All")
        context["category"] = category_name
        
        return context
    

class ProductDetailPageView(DetailView):
    template_name = "product_detail.html"
    model = ProductModel
    context_object_name = "product"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        data = super().get_context_data(**kwargs)

        quantity = 0

        if user := self.request.user:
            try:
                order = OrderModel.objects.get(user=user, product=data[self.context_object_name])
                quantity = order.quantity
            except:
                quantity = 0

        data["product_quantity"] = quantity

        return data
