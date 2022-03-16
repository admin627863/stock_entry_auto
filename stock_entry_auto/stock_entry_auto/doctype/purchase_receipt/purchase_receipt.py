import frappe
import requests
import json

@frappe.whitelist()
def on_purchase_receipt_after_submit(doc, handler=""):
            frappe.db.sql("""update `tabPurchase Receipt` set status = 'Material Arrived at Labgate/yadro' where name = %s""",(doc.name))
            frappe.db.commit()
            doc.save()
