from tabnanny import check
import frappe
from datetime import date, datetime, timedelta
from frappe.utils import date_diff


def on_sales_invoice_payment_after_submit(doc, handler=""):
            
            payment = frappe.new_doc('Payment Entry')
            payment.posting_date = datetime.now()
            payment.payment_type = 'Receive'
            payment.party_type = 'Customer'
            payment.mode_of_payment = doc.payment_mode
            payment.party = doc.customer
            payment.paid_to = 'Cash - MS'
            payment.paid_from = 'Debtors - MS'
            payment.paid_amount = doc.grand_total
            payment.received_amount = doc.grand_total
            payment.append('references', {
                    'reference_doctype': 'Sales Invoice',
                    'reference_name': doc.name,
                    'total_amount': doc.grand_total,
                    'allocated_amount': doc.grand_total
                })
            payment.submit()