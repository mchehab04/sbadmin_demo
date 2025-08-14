from django.urls import path
from .views import QuotationCreateView
from django.views.generic import TemplateView

app_name = "quotes"

urlpatterns = [
    path("new/", QuotationCreateView.as_view(), name="create"),
    path("list/", TemplateView.as_view(template_name="quotes/quotations_list.html"), name="list"),
    path("edit/", TemplateView.as_view(template_name="quotes/quotations_edit.html"), name="edit"),
]
# This file defines the URL patterns for the quotes app, including a view for creating new quotations and templates for listing and editing quotations.
# The `QuotationCreateView` handles the form submission and PDF generation for new quotations.