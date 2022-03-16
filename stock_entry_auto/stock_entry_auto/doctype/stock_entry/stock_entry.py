import frappe
import requests
import json

@frappe.whitelist()
def on_stock_entry_after_submit(doc, handler=""):
    expense = frappe.db.get_value('Company',{'name':doc.company},['default_expense_account'])
    material = frappe.db.get_value('Warehouse',{'name':doc.to_warehouse},['is_consumption_required'])
    if material == True:
        if doc.stock_entry_type == 'Material Transfer':        
            new_st = frappe.new_doc('Stock Entry')
            for i in doc.items:
                new_st.append("items",{
                                    'item_code':i.item_code,
                                    'item_name':i.item_name,
                                    'qty':i.qty,
                                    'batch_no':i.batch_no or '',
                                    'amount':i.amount,
                                    'uom':i.uom,
                                    'expense_account':expense,
                                    'cost_center':i.cost_center
                                })
                
                
            new_st.stock_entry_type = 'Material Issue'
            new_st.from_warehouse = doc.to_warehouse  
            new_st.warranty_claim = doc.warranty_claim
            new_st.flags.ignore_permissions  = True
            new_st.submit()
        
