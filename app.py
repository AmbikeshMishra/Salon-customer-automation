from flask import Flask, flash, render_template, request, redirect, url_for, session, jsonify
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

import qrcode
import io
import base64



app = Flask(__name__)
app.secret_key = "supersecret"  # required for session management

# Google Sheets setup
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)
sheet = client.open("BarberShopLog").sheet1


@app.route("/register", methods=["POST"])
def register():
    name = request.form.get("name")
    phone = request.form.get("phone")
    scheme = request.form.get("scheme", "Default")

    if not name or not phone:
        flash("❌ Name and phone are required")
        return redirect(url_for("show_registration"))

    # Access Customers sheet
    customers_sheet = client.open("BarberShopLog").worksheet("Customers")
    records = customers_sheet.get_all_records()

    # Check if phone already exists
    existing = [r for r in records if str(r["Phone"]) == str(phone)]
    if existing:
        latest = existing[-1]
        customer = {
            "CustomerID": latest["CustomerID"],
            "Name": latest["Name"],
            "Phone": latest["Phone"],
            "SchemeName": latest.get("SchemeName", "Default")
        }
        session["customer"] = customer

        # Generate QR for existing customer
        qr_data = {
            "CustomerID": customer["CustomerID"],
            "Name": customer["Name"],
            "Phone": customer["Phone"],
            "SchemeName": customer["SchemeName"]
        }
        qr_img = qrcode.make(qr_data)
        buf = io.BytesIO()
        qr_img.save(buf, format="PNG")
        qr_base64 = base64.b64encode(buf.getvalue()).decode("utf-8")

        flash(f"ℹ️ Customer already registered: {customer['Name']} ({customer['Phone']})")
        return render_template("registration_success.html", customer=customer, qr_code=qr_base64)

    # Generate new CustomerID
    customer_id = f"C{datetime.now().strftime('%Y%m%d%H%M%S')}_{phone}"

    # Append new row to Customers sheet
    customers_sheet.append_row([
        phone, customer_id, name, scheme,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Yes"
    ])

    # Store in session
    customer = {
        "CustomerID": customer_id,
        "Name": name,
        "Phone": phone,
        "SchemeName": scheme
    }
    session["customer"] = customer

    # Generate QR for new customer
    qr_data = {
        "CustomerID": customer_id,
        "Name": name,
        "Phone": phone,
        "SchemeName": scheme
    }
    qr_img = qrcode.make(qr_data)
    buf = io.BytesIO()
    qr_img.save(buf, format="PNG")
    qr_base64 = base64.b64encode(buf.getvalue()).decode("utf-8")

    flash(f"✅ Registered {name} ({phone}) with ID {customer_id}")
    return render_template("registration_success.html", customer=customer, qr_code=qr_base64)

@app.route("/customer_transactions", methods=["GET"])
def customer_transactions():
    customer = session.get("customer")
    if not customer:
        return jsonify({"status": "error", "message": "❌ No customer selected"})

    records = sheet.get_all_records()
    # Filter by phone number
    matches = [r for r in records if str(r["Phone"]) == str(customer["Phone"])]

    # Sort by timestamp if available (optional)
    matches = sorted(matches, key=lambda r: r.get("Timestamp", ""), reverse=True)

    # Get last 20 transactions
    last_transactions = matches[-20:] if len(matches) > 20 else matches

    return jsonify({
        "status": "success",
        "transactions": last_transactions
    })



@app.route("/register/new")
def show_registration():
    return render_template("registration.html")


# Service catalog
services = {
    "1": ("Haircut", 500),
    "2": ("Shaving", 200),
    "3": ("Facial", 800),
    "4": ("Hair Colour", 1000),
    "5": ("Massage", 600)
}


# Example service catalog (code -> {name, price})
SERVICE_CATALOG = {
    "1": {"name": "Haircut", "price": 500},
    "2": {"name": "Shaving", "price": 200},
    "3": {"name": "Facial", "price": 800},
    "4": {"name": "Hair Colour", "price": 1000},
    # ...
}

# Example scheme discounts (scheme -> rate)
SCHEME_DISCOUNTS = {
    "Default": 0.5,  # 50% billed
    "Gold": 0.6,
    "Silver": 0.7,
    # ...
}

def get_service_by_code(code: str):
    return SERVICE_CATALOG.get(str(code), {"name": "Unknown", "price": 0})

def get_discount_rate(customer: dict):
    scheme = (customer.get("SchemeName") or "Default").strip()
    return SCHEME_DISCOUNTS.get(scheme, SCHEME_DISCOUNTS["Default"])

def get_service_price_by_name(name: str) -> int:
    for s in SERVICE_CATALOG.values():
        if s["name"].lower() == name.lower():
            return s["price"]
    return 0  # fallback

def get_discount_rate_for_customer(customer: dict) -> float:
    scheme = (customer.get("SchemeName") or "Default").strip()
    return SCHEME_DISCOUNTS.get(scheme, SCHEME_DISCOUNTS["Default"])


# --- Routes ---

@app.route("/")
def index():
    if "selected_codes" not in session:
        session["selected_codes"] = []
    return render_template("index.html", services=services, selected=session["selected_codes"])

@app.route("/add/<code>")
def add_service(code):
    selected = session.get("selected_codes", [])
    selected.append(code)
    session["selected_codes"] = selected
    return redirect(url_for("index"))

@app.route("/undo")
def undo_last():
    selected = session.get("selected_codes", [])
    if selected:
        selected.pop()
    session["selected_codes"] = selected
    return redirect(url_for("index"))


@app.route("/set_customer", methods=["POST"])
def set_customer():
    data = request.get_json()
    customer = data.get("customer")

    if customer:
        session["customer"] = customer
        return jsonify({
            "status": "success",
            "message": f"✅ Customer loaded: {customer['Name']} ({customer['Phone']}) | Balance ₹{customer.get('Balance', 0)}"
        })
    else:
        return jsonify({"status": "error", "message": "❌ Invalid customer data"})

@app.route("/finalize", methods=["POST"])
def finalize():
    customer = session.get("customer")
    if not customer:
        flash("❌ No customer scanned")
        return redirect(url_for("index"))

    selected_codes = session.get("selected_codes", [])
    if not selected_codes:
        flash("❌ No services selected")
        return redirect(url_for("index"))

    records = sheet.get_all_records()
    cust_records = [r for r in records if r["CustomerID"] == customer["CustomerID"]]
    prev_balance = cust_records[-1]["BalanceAfter"] if cust_records else 0

    #discount_rate = 0.5 if prev_balance > 0 else 1.0
    discount_rate = get_discount_rate(customer)
    total_price = sum(services[c][1] for c in selected_codes)
    final_total = total_price * discount_rate
    discount_amount = total_price - final_total

    running_balance = prev_balance
    summary_rows = []

    for c in selected_codes:
        name, price = services[c]
        final = price * discount_rate
        disc = price - final
        running_balance -= final

        summary_rows.append({
            "code": c,
            "name": name,
            "original": price,
            "final": final,
            "discount": disc,
            "balance": running_balance
        })

        sheet.append_row([
            customer["CustomerID"], customer["Name"], customer["Phone"], customer.get("SchemeName", "Default"),
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"), c, name, price,
            "Yes" if discount_rate < 1 else "No",
            final, disc, final, running_balance,
            "Yes" if running_balance > 0 else "No"
        ])

    session["selected_codes"] = []
    session["finalized_summary"] = {
        "customer": customer,
        "rows": summary_rows,
        "total": total_price,
        "discount": discount_amount,
        "final": final_total,
        "balance": running_balance
    }

    flash(f"✅ Finalized {len(summary_rows)} services for {customer['Name']}")
    return redirect(url_for("index"))
from flask import request, jsonify, session

@app.route("/lookup_customer", methods=["POST"])
def lookup_customer():
    phone = request.form.get("phone")
    if not phone:
        return jsonify({
            "status": "error",
            "message": "❌ No phone number provided"
        })

    records = sheet.get_all_records()
    matches = [r for r in records if str(r["Phone"]) == str(phone)]

    if not matches:
        return jsonify({
            "status": "error",
            "message": "❌ No customer found"
        })

    latest = matches[-1]
    customer = {
        "CustomerID": latest["CustomerID"],
        "Name": latest["Name"],
        "Phone": latest["Phone"],
        "SchemeName": latest.get("SchemeName", "Default")
    }

    # ✅ Get latest balance
    balance = latest.get("BalanceAfter", 0)

    # Save customer in session
    session["customer"] = customer

    return jsonify({
        "status": "success",
        "message": f"✅ Customer loaded: {customer['Name']} ({customer['Phone']}) | Balance ₹{balance}",
        "customer": customer,
        "balance": balance
    })

@app.route("/get_customer")
def get_customer():
    customer = session.get("customer")
    return jsonify({"customer": customer})  # keep JSON for JS auto-load

@app.route("/reset_customer", methods=["POST"])
def reset_customer():
    session.pop("customer", None)
    session.pop("finalized_summary", None)
    return jsonify({"status": "success", "message": "ℹ️ Customer reset"})

def update_summary_totals(summary):
    """Recalculate totals and balance for a finalized summary dict."""
    if not summary or "rows" not in summary:
        return summary

    total = sum(r["original"] for r in summary["rows"])
    discount = sum(r["discount"] for r in summary["rows"])
    final_total = sum(r["final"] for r in summary["rows"])
    balance = summary["rows"][-1]["balance"] if summary["rows"] else 0

    summary["total"] = total
    summary["discount"] = discount
    summary["final"] = final_total
    summary["balance"] = balance

    return summary

def build_finalize_summary():
    summary = session.get("finalized_summary")
    if not summary:
        return None
    return update_summary_totals(summary)

@app.route("/submit", methods=["POST"])
def submit():
    data = request.form.to_dict()
    action = data.get("action")
    customer = session.get("customer")

    if not customer:
        flash("❌ No customer scanned")
        return redirect(url_for("index"))

    code = data.get("code")
    correct_code = data.get("correct_code")
    amount = float(data.get("amount", 0)) if data.get("amount") else 0
    mode = data.get("mode", "add")

    records = sheet.get_all_records()
    cust_records = [r for r in records if r["CustomerID"] == customer["CustomerID"]]
    prev_balance = cust_records[-1]["BalanceAfter"] if cust_records else 0

    rows = []

    if action == "topup":
        amount = float(data.get("amount", 0)) if data.get("amount") else 0
        mode = data.get("mode", "add")

        # ✅ Calculate new balance
        new_balance = amount if mode == "reset" else prev_balance + amount

        # ✅ Build row exactly matching your sheet headers
        rows.append([
            customer["CustomerID"],                 # CustomerID
            customer["Name"],                       # Name
            customer["Phone"],                      # Phone
            customer["SchemeName"],                 # SchemeName
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),  # Date
            "T",                                    # ServiceCode
            "Top-Up",                               # ServiceName
            amount,                                 # Price
            "No",                                   # DiscountApplied
            amount,                                 # FinalPrice
            amount,                                 # Credit
            0,                                      # Debit
            new_balance,                            # BalanceAfter
            "Yes" if new_balance > 0 else "No"      # SchemeActive
        ])

        # ✅ Update session balance so UI reflects immediately
        session["customer"]["Balance"] = new_balance

        # ✅ Flash confirmation
        flash(f"💳 Balance updated by ₹{amount} for {customer['Name']}", "topup")

    elif action == "delete":
        wrong = [r for r in cust_records if str(r["ServiceCode"]) == code][-1]
        refund = wrong["FinalPrice"]
        new_balance = prev_balance + refund

        # Append deletion row to sheet
        rows.append([
            customer["CustomerID"], wrong["Name"], wrong["Phone"], wrong["SchemeName"],
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"), code,
            f"Deletion of {wrong['ServiceName']}", 0,
            "No", -refund, 0, -refund, new_balance,
            "Yes" if new_balance > 0 else "No"
        ])

        wrong_name = services.get(code, ["Unknown"])[0]
        flash(f"✅ Deleted {wrong_name} for {customer['Name']}")

        # ✅ Update session summary
        if "finalized_summary" in session:
            summary = session["finalized_summary"]
            summary["rows"] = [r for r in summary["rows"] if r["name"] != wrong_name]
            if summary["rows"]:
                summary["rows"][-1]["balance"] = new_balance
            summary = update_summary_totals(summary)
            session["finalized_summary"] = summary

 
    for row in rows:
        sheet.append_row(row)
        # ✅ Rebuild summary
        #session["finalized_summary"] = build_finalize_summary(customer["CustomerID"])
        session["finalized_summary"] = build_finalize_summary()



    return redirect(url_for("index"))

if __name__ == "__main__":
    #app.run(debug=True)
    app.run(host="0.0.0.0", port=5000, debug=True)