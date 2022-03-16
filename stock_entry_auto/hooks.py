from . import __version__ as app_version

app_name = "stock_entry_auto"
app_title = "Stock Entry Auto"
app_publisher = "Matiyas Solutions"
app_description = "stock entry"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "develop.matiyas@gmail.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/stock_entry_auto/css/stock_entry_auto.css"
# app_include_js = "/assets/stock_entry_auto/js/stock_entry_auto.js"

# include js, css files in header of web template
# web_include_css = "/assets/stock_entry_auto/css/stock_entry_auto.css"
# web_include_js = "/assets/stock_entry_auto/js/stock_entry_auto.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "stock_entry_auto/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "stock_entry_auto.install.before_install"
# after_install = "stock_entry_auto.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "stock_entry_auto.uninstall.before_uninstall"
# after_uninstall = "stock_entry_auto.uninstall.after_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "stock_entry_auto.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	"Stock Entry": {
        "on_submit": "stock_entry_auto.stock_entry_auto.doctype.stock_entry.stock_entry.on_stock_entry_after_submit",
    },
	"Purchase Receipt": {
        "on_submit": "stock_entry_auto.stock_entry_auto.doctype.purchase_receipt.purchase_receipt.on_purchase_receipt_after_submit",
    }
}

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"stock_entry_auto.tasks.all"
# 	],
# 	"daily": [
# 		"stock_entry_auto.tasks.daily"
# 	],
# 	"hourly": [
# 		"stock_entry_auto.tasks.hourly"
# 	],
# 	"weekly": [
# 		"stock_entry_auto.tasks.weekly"
# 	]
# 	"monthly": [
# 		"stock_entry_auto.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "stock_entry_auto.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "stock_entry_auto.event.get_events"
# }
# override_whitelisted_methods = {
# 	"frappe.desk.search.search_link": "stock_entry_auto.desk.search.search_link"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "stock_entry_auto.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]


# User Data Protection
# --------------------

user_data_fields = [
	{
		"doctype": "{doctype_1}",
		"filter_by": "{filter_by}",
		"redact_fields": ["{field_1}", "{field_2}"],
		"partial": 1,
	},
	{
		"doctype": "{doctype_2}",
		"filter_by": "{filter_by}",
		"partial": 1,
	},
	{
		"doctype": "{doctype_3}",
		"strict": False,
	},
	{
		"doctype": "{doctype_4}"
	}
]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"stock_entry_auto.auth.validate"
# ]

