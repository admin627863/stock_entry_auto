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
        
        url = "https://scm.torqus.com/intg/report/sales?day_status=2022-02-10&siteId=88588" 

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
            stagging.charge = state['packing_charge']['charge'] or ''
            stagging.cgst = state['packing_charge']['cgst'] or ''
            stagging.sgst = state['packing_charge']['sgst'] or ''
            stagging.service_charge = state['service_charge']['charge'] or ''
            stagging.service_cgst = state['service_charge']['cgst'] or ''
            stagging.service_sgst = state['service_charge']['sgst'] or ''
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
            sales_invoice.update_stock = True
            sales_invoice.deal_number = '100'
            sales_invoice.warranty_claim = 'SER-WRN-2022-00001'
            for si in st.get('items'):
                sales_invoice.append("items",{
                    'item_code':si.item_code,
                    'qty':si.qty,
                    'rate':si.rate,
                    'uom':'Box'
                })
                frappe.delete_doc('Staging Table', st.order_id)
                sales_invoice.save()
            
        # response_API = requests.get('https://reqres.in/api/products/3')
        # data = response_API.text
        # parse_json = json.loads(data)
        # active_case = parse_json['data']
        # response_API = requests.get('https://reqres.in/api/products/3')
        # data = response_API.text

        # data1 = json.loads(data)

        # for person in data1['data']:
        #     # value = active_case[i]
        #     test = frappe.new_doc('Test Doc')
        #     test.value = person
        #     test.save()
        #     frappe.msgprint(person)
        frappe.msgprint("Sales Invoice Created")
          
      # jsonString = '{"key1":"value1","key2":"value2","key3":"value3"}'
      # jsonObject = json.loads(jsonString)
      # for key in jsonObject:
      #   value = jsonObject[key]
      #   frappe.msgprint("The key and value are ({}) = ({})".format(key, value))

      # response_API = requests.get('https://api.covid19india.org/state_district_wise.json')
      # #print(response_API.status_code)
      # data = response_API.text
      # parse_json = json.loads(data)
      # active_case = parse_json['Andaman and Nicobar Islands']['districtData']['South Andaman']  
      
      # for i in active_case:
      #    value = active_case[i]
      #    frappe.msgprint("{}".format(value))