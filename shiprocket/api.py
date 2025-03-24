import frappe
import requests
import json
from datetime import datetime

# Shiprocket Credentials
SHIPROCKET_EMAIL = "abdullamirshadcl@gmail.com"
SHIPROCKET_PASSWORD = "Mirshad@123"

SHIPROCKET_API_BASE = "https://apiv2.shiprocket.in/v1/external"

# Authenticate with Shiprocket
def get_shiprocket_token():
    url = f"{SHIPROCKET_API_BASE}/auth/login"
    payload = json.dumps({"email": SHIPROCKET_EMAIL, "password": SHIPROCKET_PASSWORD})
    headers = {"Content-Type": "application/json"}

    response = requests.post(url, data=payload, headers=headers)

    if response.status_code == 200:
        return response.json().get("token")
    else:
        frappe.throw(f"Shiprocket Authentication Failed: {response.text}")

# @frappe.whitelist()
# def create_shiprocket_order(doc=None, method=None):
#     if not doc:
#         frappe.throw("Sales Order document is required.")

#     token = get_shiprocket_token()
#     order_date = datetime.strptime(doc.transaction_date, "%Y-%m-%d") if isinstance(doc.transaction_date, str) else doc.transaction_date
#     billing_address_name = doc.customer_address or frappe.get_value("Address", {"links": {"link_doctype": "Customer", "link_name": doc.customer}}, "name")

#     if not billing_address_name:
#         frappe.throw(f"Billing address not found for customer {doc.customer}")

#     billing_address_doc = frappe.get_doc("Address", billing_address_name)
#     customer_name = frappe.get_value("Customer", doc.customer, "customer_name")
#     name_parts = customer_name.strip().split(" ", 1)
#     billing_customer_name = name_parts[0]
#     billing_last_name = name_parts[1] if len(name_parts) > 1 else ""

#     order_items = [{
#         "name": item.item_name,
#         "sku": item.item_code,
#         "units": item.qty,
#         "selling_price": item.rate
#     } for item in doc.items]

#     if not order_items:
#         frappe.throw("No items found in the order.")

#     order_data = {
#         "order_id": doc.name,
#         "order_date": order_date.strftime("%Y-%m-%d"),
#         "channel_id": "",
#         "billing_customer_name": billing_customer_name,
#         "billing_last_name": billing_last_name,
#         "billing_phone": billing_address_doc.phone,
#         "billing_address": billing_address_doc.address_line1[:80],
#         "billing_city": billing_address_doc.city,
#         "billing_pincode": billing_address_doc.pincode,
#         "billing_state": billing_address_doc.state,
#         "billing_country": "India",
#         "shipping_is_billing": 1,
#         "order_items": order_items,
#         "payment_method": "Prepaid",
#         "sub_total": doc.total,
#         "length": 10,
#         "breadth": 10,
#         "height": 10,
#         "weight": 1
#     }

#     url = "https://apiv2.shiprocket.in/v1/external/orders/create/adhoc"
#     headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}
#     response = requests.post(url, json=order_data, headers=headers)

#     if response.status_code == 200:
#         shiprocket_response = response.json()
#         shiprocket_order_id = shiprocket_response.get("order_id")  # Extract Shiprocket Order ID
        
#         if shiprocket_order_id:
#             # Store Shiprocket order ID in Sales Order
#             doc.db_set("custom_shiprocket_order_id", shiprocket_order_id)
#             frappe.msgprint(f"Order created in Shiprocket. Order ID: {shiprocket_order_id}")
#         else:
#             frappe.throw("Failed to retrieve Shiprocket Order ID.")
#     else:
#         frappe.throw(f"Shiprocket Order creation failed. Response: {response.text}")
# @frappe.whitelist()
# def create_shiprocket_order(doc=None, method=None):
#     if not doc:
#         frappe.throw("Payment Entry document is required.")

#     # Fetch Sales Order linked to the Payment Entry
#     sales_order_name = None
#     for ref in doc.references:
#         if ref.reference_doctype == "Sales Order":
#             sales_order_name = ref.reference_name
#             break

#     if not sales_order_name:
#         frappe.throw("No linked Sales Order found in Payment Entry.")

#     sales_order = frappe.get_doc("Sales Order", sales_order_name)  # Fetch the Sales Order

#     token = get_shiprocket_token()
#     order_date = datetime.strptime(sales_order.transaction_date, "%Y-%m-%d") if isinstance(sales_order.transaction_date, str) else sales_order.transaction_date

#     # Get billing address
#     billing_address_name = sales_order.customer_address or frappe.get_value(
#         "Address", {"links": {"link_doctype": "Customer", "link_name": sales_order.customer}}, "name"
#     )

#     if not billing_address_name:
#         frappe.throw(f"Billing address not found for customer {sales_order.customer}")

#     billing_address_doc = frappe.get_doc("Address", billing_address_name)
#     customer_name = frappe.get_value("Customer", sales_order.customer, "customer_name")
#     name_parts = customer_name.strip().split(" ", 1)
#     billing_customer_name = name_parts[0]
#     billing_last_name = name_parts[1] if len(name_parts) > 1 else ""

#     # Fetch order items
#     order_items = [{
#         "name": item.item_name,
#         "sku": item.item_code,
#         "units": item.qty,
#         "selling_price": item.rate
#     } for item in sales_order.items]

#     if not order_items:
#         frappe.throw("No items found in the Sales Order.")

#     # Order Data for Shiprocket
#     order_data = {
#         "order_id": sales_order.name,
#         "order_date": order_date.strftime("%Y-%m-%d"),
#         "channel_id": "",
#         "billing_customer_name": billing_customer_name,
#         "billing_last_name": billing_last_name,
#         "billing_phone": billing_address_doc.phone,
#         "billing_address": billing_address_doc.address_line1[:80],
#         "billing_city": billing_address_doc.city,
#         "billing_pincode": billing_address_doc.pincode,
#         "billing_state": billing_address_doc.state,
#         "billing_country": "India",
#         "shipping_is_billing": 1,
#         "order_items": order_items,
#         "payment_method": "Prepaid",
#         "sub_total": sales_order.total,
#         "length": 10,
#         "breadth": 10,
#         "height": 10,
#         "weight": 1
#     }

#     # Call Shiprocket API
#     url = "https://apiv2.shiprocket.in/v1/external/orders/create/adhoc"
#     headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}
#     response = requests.post(url, json=order_data, headers=headers)

#     if response.status_code == 200:
#         shiprocket_response = response.json()
#         shiprocket_order_id = shiprocket_response.get("order_id")

#         if shiprocket_order_id:
#             # Store Shiprocket order ID in Sales Order
#             sales_order.db_set("custom_shiprocket_order_id", shiprocket_order_id)
#             frappe.msgprint(f"Order created in Shiprocket. Order ID: {shiprocket_order_id}")
#         else:
#             frappe.throw("Failed to retrieve Shiprocket Order ID.")
#     else:
#         frappe.throw(f"Shiprocket Order creation failed. Response: {response.text}")
@frappe.whitelist()
def create_shiprocket_order(doc=None, method=None):
    print("Starting Shiprocket Order Creation...")

    if not doc:
        frappe.throw("Sales Invoice document is required.")

    # Fetch linked Sales Order from Sales Invoice items
    sales_order_name = doc.items[0].sales_order if doc.items else None

    if not sales_order_name:
        frappe.throw("No linked Sales Order found in Sales Invoice.")

    print(f"Sales Order Found: {sales_order_name}")

    try:
        sales_order = frappe.get_doc("Sales Order", sales_order_name)
        print("Sales Order fetched successfully.")
    except Exception as e:
        print(f"Error fetching Sales Order: {str(e)}")
        frappe.throw(f"Error fetching Sales Order: {str(e)}")

    # Get Shiprocket Token
    token = get_shiprocket_token()
    print("Shiprocket token fetched successfully.")

    # Convert order date
    try:
        order_date = datetime.strptime(sales_order.transaction_date, "%Y-%m-%d") if isinstance(sales_order.transaction_date, str) else sales_order.transaction_date
    except Exception as e:
        print(f"Error parsing order date: {str(e)}")
        frappe.throw(f"Error parsing order date: {str(e)}")

    # Get billing address
    billing_address_name = sales_order.customer_address or frappe.get_value(
        "Address", {"links": {"link_doctype": "Customer", "link_name": sales_order.customer}}, "name"
    )

    if not billing_address_name:
        print(f"Billing address not found for customer {sales_order.customer}")
        frappe.throw(f"Billing address not found for customer {sales_order.customer}")

    try:
        billing_address_doc = frappe.get_doc("Address", billing_address_name)
        print(f"Billing address fetched: {billing_address_name}")
    except Exception as e:
        print(f"Error fetching billing address: {str(e)}")
        frappe.throw(f"Error fetching billing address: {str(e)}")

    # Extract customer name
    customer_name = frappe.get_value("Customer", sales_order.customer, "customer_name")
    name_parts = customer_name.strip().split(" ", 1)
    billing_customer_name = name_parts[0]
    billing_last_name = name_parts[1] if len(name_parts) > 1 else ""

    # Fetch order items
    order_items = [  
        {
            "name": item.item_name,
            "sku": item.item_code,
            "units": item.qty,
            "selling_price": item.rate
        }
        for item in sales_order.items
    ]

    if not order_items:
        print("No items found in the Sales Order.")
        frappe.throw("No items found in the Sales Order.")

    print(f"Order Items: {order_items}")

    # Order Data for Shiprocket
    order_data = {
        "order_id": sales_order.name,
        "order_date": order_date.strftime("%Y-%m-%d"),
        "channel_id": "",
        "billing_customer_name": billing_customer_name,
        "billing_last_name": billing_last_name,
        "billing_phone": billing_address_doc.phone,
        "billing_address": billing_address_doc.address_line1[:80],
        "billing_city": billing_address_doc.city,
        "billing_pincode": billing_address_doc.pincode,
        "billing_state": billing_address_doc.state,
        "billing_country": "India",
        "shipping_is_billing": 1,
        "order_items": order_items,
        "payment_method": "Prepaid",
        "sub_total": sales_order.total,
        "length": 10,
        "breadth": 10,
        "height": 10,
        "weight": 1
    }

    print(f"Shiprocket Order Data: {order_data}")

    # Call Shiprocket API
    url = "https://apiv2.shiprocket.in/v1/external/orders/create/adhoc"
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}

    try:
        response = requests.post(url, json=order_data, headers=headers)
        response_data = response.json()
        print(f"Shiprocket API Response: {response_data}")

        if response.status_code == 200 and response_data.get("order_id"):
            shiprocket_order_id = response_data.get("order_id")
            sales_order.db_set("custom_shiprocket_order_id", shiprocket_order_id)
            sales_order.db_set("custom_tracking_number", shiprocket_order_id)
            sales_order.db_set("custom_current_status", "Order Placed")
            frappe.msgprint(f"Order created in Shiprocket. Order ID: {shiprocket_order_id}")
            print(f"Shiprocket Order ID stored: {shiprocket_order_id}")
        else:
            print(f"Shiprocket Order creation failed. Response: {response.text}")
            frappe.throw(f"Shiprocket Order creation failed. Response: {response.text}")

    except Exception as e:
        print(f"Shiprocket API request failed: {str(e)}")
        frappe.throw(f"Shiprocket API request failed: {str(e)}")

    print("Shiprocket Order creation process completed successfully.")



# Cancel an Order in Shiprocket
@frappe.whitelist()
def cancel_shiprocket_order(doc, method):
    if not doc.custom_shiprocket_order_id:
        frappe.throw("Order ID is required for cancellation.")

    token = get_shiprocket_token()
    url = f"{SHIPROCKET_API_BASE}/orders/cancel"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    
    payload = {"ids": [doc.custom_shiprocket_order_id]}  # Shiprocket expects a list of order IDs

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        frappe.msgprint(f"Order {doc.custom_shiprocket_order_id} cancelled successfully in Shiprocket.")
    else:
        frappe.throw(f"Failed to cancel order {doc.custom_shiprocket_order_id}. Response: {response.text}")


# @frappe.whitelist()
# def update_shiprocket_order_payment(doc, method):
#     """Update Shiprocket order payment method when a Payment Entry is created"""

#     if not doc.references:
#         return  # No linked Sales Order

#     sales_order_id = doc.references[0].reference_name
#     sales_order = frappe.get_doc("Sales Order", sales_order_id)

#     if not sales_order:
#         frappe.throw("Sales Order not found for this Payment Entry.")

#     shiprocket_order_id = sales_order.get("custom_shiprocket_order_id")
#     if not shiprocket_order_id:
#         frappe.throw("No Shiprocket Order ID found. Cannot update payment method.")

#     # Ensure payment mode is Razorpay (Prepaid)
#     # if doc.mode_of_payment != "Razorpay":
#     #     return

#     # Fetch billing address
#     billing_address_name = sales_order.customer_address or frappe.get_value(
#         "Address", {"links": {"link_doctype": "Customer", "link_name": sales_order.customer}}, "name"
#     )

#     if not billing_address_name:
#         frappe.throw(f"Billing address not found for customer {sales_order.customer}")

#     billing_address_doc = frappe.get_doc("Address", billing_address_name)
#     customer_name = frappe.get_value("Customer", sales_order.customer, "customer_name")
#     name_parts = customer_name.strip().split(" ", 1)
#     billing_customer_name = name_parts[0]
#     billing_last_name = name_parts[1] if len(name_parts) > 1 else ""

#     # Prepare order items
#     order_items = [{
#         "name": item.item_name,
#         "sku": item.item_code,
#         "units": item.qty,
#         "selling_price": item.rate
#     } for item in sales_order.items]

#     if not order_items:
#         frappe.throw("No items found in the order.")

#     # Prepare payload for Shiprocket order update
#     order_data = {
#         "order_id": sales_order.name,
#         "order_date": sales_order.transaction_date.strftime("%Y-%m-%d"),
#         "channel_id": "",
#         "billing_customer_name": billing_customer_name,
#         "billing_last_name": billing_last_name,
#         "billing_phone": billing_address_doc.phone,
#         "billing_address": billing_address_doc.address_line1[:80],
#         "billing_city": billing_address_doc.city,
#         "billing_pincode": billing_address_doc.pincode,
#         "billing_state": billing_address_doc.state,
#         "billing_country": "India",
#         "shipping_is_billing": 1,
#         "order_items": order_items,
#         "payment_method": "Prepaid",  # Updating payment method to Prepaid
#         "sub_total": sales_order.total,
#         "length": 10,
#         "breadth": 10,
#         "height": 10,
#         "weight": 1
#     }

#     # API request
#     token = get_shiprocket_token()
#     url = f"{SHIPROCKET_API_BASE}/orders/update/adhoc"
#     headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    
#     response = requests.post(url, json=order_data, headers=headers)

#     if response.status_code == 200:
#         frappe.msgprint(f"Order {shiprocket_order_id} payment method updated to Prepaid in Shiprocket.")
#     else:
#         frappe.throw(f"Failed to update payment method for order {shiprocket_order_id}. Response: {response.text}")



# Get Tracking Details
@frappe.whitelist(allow_guest=True)
def get_shiprocket_tracking(order_id):
    token = get_shiprocket_token()
    url = f"{SHIPROCKET_API_BASE}/courier/track?order_id={order_id}"
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        frappe.throw(f"Tracking fetch failed: {response.text}")

# Generate Shipping Label
@frappe.whitelist()
def generate_shiprocket_label(order_id, order_data):
    token = get_shiprocket_token()
    url = f"{SHIPROCKET_API_BASE}/orders/print/labels"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    
    payload = {"ids": [order_id]}

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        label_url = response.json().get("label_url")
        frappe.msgprint(f"Shipping Label Generated: <a href='{label_url}' target='_blank'>Download Label</a>")
        return label_url
    else:
        frappe.throw(f"Failed to generate shipping label: {response.text}")


@frappe.whitelist(allow_guest=True)
def webhook_handler():
    try:
        # Read and log request headers
        headers = frappe.request.headers
        frappe.log_error(title="Shiprocket Webhook Headers", message=headers)

        # Read request data
        if frappe.request.content_type == "application/json":
            data = json.loads(frappe.request.data)
        else:
            data = frappe.form_dict

        # Log request data
        frappe.log_error(title="Shiprocket Webhook Received", message=data)

        return {"status": "success", "message": "Webhook received"}

    except Exception as e:
        frappe.log_error(title="Shiprocket Webhook Error", message=str(e))
        return {"error": str(e)}