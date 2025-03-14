import frappe
import requests
import json

# Shiprocket Credentials
SHIPROCKET_EMAIL = "info@faircodelab.com"
SHIPROCKET_PASSWORD = "Faircodelab@2025"

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

# Create an Order in Shiprocket
@frappe.whitelist()
def create_shiprocket_order(sales_order):
    doc = frappe.get_doc("Sales Order", sales_order)
    token = get_shiprocket_token()
    url = f"{SHIPROCKET_API_BASE}/orders/create/"

    order_data = {
        "order_id": doc.name,
        "order_date": doc.transaction_date.strftime("%Y-%m-%d"),
        "billing_customer_name": doc.customer,
        "billing_address": doc.address_display,
        "billing_city": doc.city,
        "billing_pincode": doc.pincode,
        "billing_state": doc.state,
        "billing_country": "India",
        "order_items": [    
            {
                "name": item.item_name,
                "sku": item.item_code,
                "units": item.qty,
                "selling_price": item.rate
            } for item in doc.items
        ],
        "payment_method": "Prepaid" if doc.is_paid else "COD",
        "sub_total": doc.total,
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    response = requests.post(url, json=order_data, headers=headers)

    if response.status_code == 200:
        order_response = response.json()
        frappe.msgprint("Order successfully sent to Shiprocket!")
        return order_response  # Returns the Shiprocket order details
    else:
        frappe.throw(f"Shiprocket Order Creation Failed: {response.text}")

# Cancel an Order in Shiprocket
@frappe.whitelist()
def cancel_shiprocket_order(order_id):
    token = get_shiprocket_token()
    url = f"{SHIPROCKET_API_BASE}/orders/cancel"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    
    payload = {"ids": [order_id]}  # Shiprocket expects a list of order IDs

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        frappe.msgprint(f"Order {order_id} cancelled successfully in Shiprocket.")
    else:
        frappe.throw(f"Failed to cancel order {order_id}. Response: {response.text}")

# Get Tracking Details
@frappe.whitelist()
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
def generate_shiprocket_label(order_id):
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
