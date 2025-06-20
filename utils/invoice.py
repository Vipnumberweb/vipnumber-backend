from weasyprint import HTML
from django.template.loader import render_to_string
from django.conf import settings
import os

def generate_invoice_pdf(sale, payment):
    context = {
        "sale": sale,
        "payment": payment,
        "customer": sale.customer,
        "numbers": sale.numbers.all(),
        "vendor_rate": sale.vendor_rate,
        "order_rate": sale.order_rate,
        "total_incl_gst": sale.total_incl_gst,
        "total_excl_gst": sale.total_excl_gst,
        "final_price": sale.final_price,
    }

    html_string = render_to_string("invoice_template.html", context)
    pdf_file = HTML(string=html_string).write_pdf()

    # Save to media/invoices/
    invoice_path = os.path.join(settings.MEDIA_ROOT, "invoices")
    os.makedirs(invoice_path, exist_ok=True)
    file_path = os.path.join(invoice_path, f"invoice_{sale.sales_id}.pdf")
    with open(file_path, "wb") as f:
        f.write(pdf_file)
    return file_path
