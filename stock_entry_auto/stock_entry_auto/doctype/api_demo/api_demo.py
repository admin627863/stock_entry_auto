# Copyright (c) 2022, Matiyas Solution  and contributors
# For license information, please see license.txt

# import frappe
import frappe
import requests
import requests
import json
from datetime import date, datetime, timedelta
from requests.structures import CaseInsensitiveDict
from frappe.model.document import Document
class Apidemo(Document):
    
     def after_insert(self):
         
        dt = self.date
        if dt < str(datetime.now()):
            url = "https://scm.torqus.com/intg/report/sales?day_status=%s&siteId=88588" % (dt)
            headers = CaseInsensitiveDict()
            headers["Authorization"] = "Bearer eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJibGFja3BlYXJsIn0.vrmO4UFk3Bs7qWRXSjZuJdEc9R_qt-Df4aVgm1BCgXoLxOykswsWD_C4E1tjD87-_VpigvtAOJNNKksQkRUoKw"
            headers["Cookie"] = "ACCESS_IDENTIFIER=eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJhZGVsQGNhcmF2YW5hLmFlIiwicm9sZXMiOlsiRGVmYXVsdCJdLCJleHAiOjE2MzcyNjY5MDIsImlhdCI6MTYzNzIyMjkwMn0.a_PkE1HLFvFdIvp5QQQV_N0vbuqjv8U1yvjEpScmknBL-Lpj6BLPbTPkU2q-rN9GzAGFUGkp8UgUuslNvIICzA"


            resp = requests.get(url, headers=headers)

            test = resp.json()

            for state in test['orders']:
                stagging = frappe.new_doc("Staging Table")
                stagging.order_id = state['order_id']
                stagging.posting_date = state['order_time']
                stagging.invoice_amount = state['invoice_amt'] or ''
                stagging.tax_amount = state['tax_amt'] or ''
                stagging.discount_amount = state['discount_amt'] or ''
                stagging.customer = state['customer']["name"]
                stagging.mobile_number = state['customer']['mobile_number'] or ''
                stagging.email  = state['customer']['email'] or ''
                if state['packing_charge'] is not None: 
                    stagging.charge = state['packing_charge']['charge']
                    stagging.cgst = state['packing_charge']['cgst']
                    stagging.sgst = state['packing_charge']['sgst']
                if state['service_charge'] is not None:
                    stagging.service_charge = state['service_charge']['charge']
                    stagging.service_cgst = state['service_charge']['cgst']
                    stagging.service_sgst = state['service_charge']['sgst']
                customer_list = frappe.get_list('Customer', fields=['customer_name'])
        
                check = {'customer_name': stagging.customer}
                if check not in customer_list:
                    customer = frappe.get_doc({
                        "doctype": "Customer",
                        "customer_name": stagging.customer,
                        "customer_group": 'Individual',
                        "territory":'India'
                    })
                    customer.insert()
                for st in state['order_payments']:
                #  stagging.payment_name = st['payment_name']
                    if st['tender_amt'] > 0:
                            stagging.append("payment_detail",{
                                                        'payment_name':st['payment_name'],
                                                        'tender_amt':st['tender_amt'],
                                                        'op_crncy':st['op_crncy'],
                                                        'payment_status':st['payment_status']
                                                    })
                # if state['order_items'] is not None:
                for ct in state['order_items']:
                        item_list = frappe.get_list('Item', fields=['item_code'])
            
                        check = {'item_code': ct['item_code']}
                        if check not in item_list:
                            item = frappe.get_doc({
                                "doctype": "Item",
                                "item_code": ct['item_code'],
                                "item_group": 'By-product'
                            })
                            item.insert()
                    #  stagging.payment_name = st['payment_name']
                        stagging.append("items",{
                                                    'item_code':ct['item_code'],
                                                    'qty':ct['item_qty'],
                                                    'rate':ct['item_price']
                                                })   
                        stagging.save()
                # else:
                #     stagging.append("items",{
                #                                     'item_code':'Dummy Item',
                #                                     'qty':'1',
                #                                     'rate':'1'
                #                                 })   
                #     stagging.submit()
                
                
            stag = frappe.db.get_list(
                'Staging Table',
                fields=("order_id"),
                filters={
                    "docstatus": 0,
                },
            ) 
            for s in stag:
                st = frappe.get_doc('Staging Table', s.order_id)
                sales_invoice = frappe.new_doc('Sales Invoice')
                sales_invoice.customer = st.customer
                sales_invoice.due_date = datetime.now()
                sales_invoice.posting_date_and_time = st.posting_date
                sales_invoice.inresto_order_id_ = st.order_id
                # sales_invoice.update_stock = True
                sales_invoice.append("taxes",{
                    'charge_type':'Actual',
                    'account_head':'Packing Charge - MS',
                    'description':'Packing Charge - MS',
                    'rate':st.charge,
                    'tax_amount':st.charge
                })
                sales_invoice.append("taxes",{
                    'charge_type':'Actual',
                    'account_head':'Packing Sgst - MS',
                    'description':'Packing Sgst - MS',
                    'rate':st.sgst,
                    'tax_amount':st.sgst
                })
                sales_invoice.append("taxes",{
                    'charge_type':'Actual',
                    'account_head':'Packing Cgst - MS',
                    'description':'Packing Cgst - MS',
                    'rate':st.cgst,
                    'tax_amount':st.cgst
                })
                sales_invoice.append("taxes",{
                    'charge_type':'Actual',
                    'account_head':'Service Charge - MS',
                    'description':'Service Charge - MS',
                    'rate':st.service_charge,
                    'tax_amount':st.service_charge
                })
                sales_invoice.append("taxes",{
                    'charge_type':'Actual',
                    'account_head':'Service Sgst - MS',
                    'description':'Service Sgst - MS',
                    'rate':st.service_sgst,
                    'tax_amount':st.service_sgst
                })
                sales_invoice.append("taxes",{
                    'charge_type':'Actual',
                    'account_head':'Service Cgst - MS',
                    'description':'Service Cgst - MS',
                    'rate':st.service_cgst,
                    'tax_amount':st.service_cgst
                })
                
                # if st.get('items') is not None:
                for si in st.get('items'):
                        sales_invoice.append("items",{
                            'item_code':si.item_code,
                            'qty':si.qty,
                            'rate':si.rate,
                            'uom':'Box'
                        })
                for pi in st.get("payment_detail"):
                        mode_payment_list = frappe.get_list('Mode of Payment', fields=['mode_of_payment'])

                        check_mode = {'mode_of_payment': pi.payment_name}
                        if check_mode not in mode_payment_list:
                                mode = frappe.get_doc({
                                    "doctype": "Mode of Payment",
                                    "mode_of_payment": pi.payment_name,
                                    "type": "Cash"         
                                })
                                mode.insert()
                        sales_invoice.payment_mode = pi.payment_name
                
                
                        frappe.delete_doc('Staging Table', st.order_id)
                        sales_invoice.submit()   
            
            frappe.msgprint("Sales Invoice Created")
            
        else:
                frappe.msgprint("Do not Enter Date After Today")
        
          
      