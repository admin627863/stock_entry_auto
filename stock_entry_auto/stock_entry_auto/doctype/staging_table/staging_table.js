// Copyright (c) 2022, Matiyas Solution  and contributors
// For license information, please see license.txt

frappe.ui.form.on('Staging Table', function(frm) {
    // refresh: function(frm) {
    frm.add_custom_button(__("update purchase rate"), function() {

        erpnext.utils.update_child_items({
            frm: frm,
            child_docname: "item",
            child_doctype: "Purchase Order Detail",
            cannot_add_row: false,
        })

    });

    // }
});