from io import BytesIO
from django.views import View
from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.staticfiles import finders

from xhtml2pdf import pisa
from .forms import QuotationForm, ItemFormSet

def link_callback(uri, rel):
    # Allow xhtml2pdf to resolve /static/... into real files
    if uri.startswith(settings.STATIC_URL):
        relative_path = uri[len(settings.STATIC_URL):]
        absolute_path = finders.find(relative_path)
        if absolute_path:
            if isinstance(absolute_path, (list, tuple)):
                absolute_path = absolute_path[0]
            return absolute_path
    return uri  # fallback

class QuotationCreateView(View):
    template_name = "quotes/quotation_form.html"

    def get(self, request):
        return render(request, self.template_name, {
            "form": QuotationForm(),
            "formset": ItemFormSet()
        })

    def post(self, request):
        form = QuotationForm(request.POST)
        formset = ItemFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            quotation = form.save()
            formset.instance = quotation
            formset.save()

            # Render HTML to PDF
            html = render_to_string("quotes/quotation_pdf.html", {"q": quotation})
            pdf_buffer = BytesIO()
            pisa.CreatePDF(html, dest=pdf_buffer, link_callback=link_callback)
            resp = HttpResponse(pdf_buffer.getvalue(), content_type="application/pdf")
            resp["Content-Disposition"] = f'attachment; filename="quotation_{quotation.pk}.pdf"'
            return resp

        # invalid -> re-render with errors
        return render(request, self.template_name, {"form": form, "formset": formset})
