import frappe
from frappe.utils import cstr, unique
from frappe.desk.search import search_widget

@frappe.whitelist()
def search_link(doctype, txt, query=None, filters=None, page_length=20, searchfield=None, reference_doctype=None, ignore_user_permissions=False):
    search_widget(doctype, txt.strip(), query, searchfield=searchfield, page_length=page_length, filters=filters, reference_doctype=reference_doctype, ignore_user_permissions=ignore_user_permissions)
    frappe.response['results'] = build_for_autosuggest(frappe.response["values"])
    del frappe.response["values"]

def build_for_autosuggest(res):
    results = []
    for r in res:
        out = {
            "value": r[0],
            "description": ", ".join(unique(cstr(d) for d in r if d)[1:]),
            "actual_qty":get_actual_qty(r[0]) # get_actual_qty is self implement function
        }
        results.append(out)
    return results