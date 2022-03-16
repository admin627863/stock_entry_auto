import frappe
import frappe.utils
from frappe import _
from frappe.contacts.doctype.address.address import get_company_address
from frappe.desk.notifications import clear_doctype_notifications
from frappe.model.mapper import get_mapped_doc
from frappe.model.utils import get_fetch_values
from frappe.utils import add_days, cint, cstr, flt, get_link_to_form, getdate, nowdate, strip_html
from six import string_types
from erpnext.accounts.doctype.sales_invoice.sales_invoice import (
    unlink_inter_company_doc,
    update_linked_doc,
    validate_inter_company_party,
)
from erpnext.controllers.selling_controller import SellingController
from erpnext.manufacturing.doctype.production_plan.production_plan import (
    get_items_for_material_requests,
)
from erpnext.selling.doctype.customer.customer import check_credit_limit
from erpnext.setup.doctype.item_group.item_group import get_item_group_defaults
from erpnext.stock.doctype.item.item import get_item_defaults
from erpnext.stock.stock_balance import get_reserved_qty, update_bin_qty


@frappe.whitelist()
def make_sales_invoice(source_name, target_doc=None, ignore_permissions=False):
    def postprocess(source, target):
        set_missing_values(source, target)
        # Get the advance paid Journal Entries in Sales Invoice Advance
        if target.get("allocate_advances_automatically"):
            target.set_advances()

    def set_missing_values(source, target):
        target.ignore_pricing_rule = 1
        target.flags.ignore_permissions = True
        target.run_method("set_missing_values")
        target.run_method("set_po_nos")
        target.run_method("calculate_taxes_and_totals")
        target.customer = source.customer_name
        target.due_date = source.valid_till
        # if source.company_address:
        # 	target.update({'company_address': source.company_address})
        # else:
        # 	# set company address
        # 	target.update(get_company_address(target.company))

        # if target.company_address:
        # 	target.update(get_fetch_values("Sales Invoice", 'company_address', target.company_address))

        # set the redeem loyalty points if provided via shopping cart
        # if source.loyalty_points and source.order_type == "Shopping Cart":
        # 	target.redeem_loyalty_points = 1

    def update_item(source, target, source_parent):
        
        if target.item_code:
            item = get_item_defaults(target.item_code, source_parent.company)
            item_group = get_item_group_defaults(
                target.item_code, source_parent.company)
            cost_center = item.get("selling_cost_center") \
                or item_group.get("selling_cost_center")

            if cost_center:
                target.cost_center = cost_center

    doclist = get_mapped_doc("Quotation", source_name, {
        "Quotation": {
            "doctype": "Sales Invoice",
            "field_map": {
                "party_account_currency": "party_account_currency",
                "payment_terms_template": "payment_terms_template"
            },
            "field_no_map": ["payment_terms_template"],
            "validation": {
                "docstatus": ["=", 1]
            }
        },
        "Quotation Item": {
            "doctype": "Sales Invoice Item",
            "field_map": {
                "name": "so_detail",
                        "parent": "quotation",
            },
            "postprocess": update_item,
        },
    }, target_doc, postprocess, ignore_permissions=ignore_permissions)

    automatically_fetch_payment_terms = cint(frappe.db.get_single_value(
        'Accounts Settings', 'automatically_fetch_payment_terms'))
    if automatically_fetch_payment_terms:
        doclist.set_payment_schedule()

    return doclist
