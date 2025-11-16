from django import forms
from .models import Order, Review


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["address", "phone", "payment_method"]


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["rating", "text"]
        widgets = {
            "rating": forms.NumberInput(attrs={"min": 1, "max": 5}),
            "text": forms.Textarea(attrs={"rows": 3}),
        }
