from flask import Flask, render_template, request, jsonify
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

app = Flask(__name__)

# Google Sheets setup
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)
sheet = client.open("BarberShopLog").sheet1

services = {
    "1": ("Haircut", 500),
    "2": ("Shaving", 200),
    "3": ("Facial", 800),
    "4": ("Hair Colour", 1000),
    "5": ("Massage", 600)
}

@app.route("/")
def index():
    return render_template("index.html", services=services)

@app.route("/submit", methods=["POST"])
def submit():
    #data = request.json
    data = request.form.to_dict()
    customer = data["customer"]
    action = data["action"]
    code = data.get("code")
    correct_code = data.get("correct_code")
    amount = float(data.get("amount", 0))

    # Get latest balance
    records = sheet.get_all_records()
    cust_records = [r for r in records if r["CustomerID"] == customer["CustomerID"]]
    prev_balance = cust_records[-1]["BalanceAfter"] if cust_records else 0

    rows = []
    if action == "service":
        name, price = services[code]
        discount = 0.5 if prev_balance > 0 else 1.0
        final = price * discount
        new_balance = prev_balance - final
        rows.append([
            customer["CustomerID"], customer["Name"], customer["Phone"], customer.get("SchemeName", "Default"),
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"), code, name, price,
            "Yes" if discount < 1 else "No", final, 0, final, new_balance,
            "Yes" if new_balance > 0 else "No"
        ])
    elif action == "topup":
        new_balance = amount if data.get("mode") == "reset" else prev_balance + amount
        rows.append([
            customer["CustomerID"], customer["Name"], customer["Phone"], customer.get("SchemeName", "Default"),
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "T", "Top-Up", 0, "No", 0, amount, 0, new_balance,
            "Yes" if new_balance > 0 else "No"
        ])
    elif action == "delete":
        wrong = [r for r in cust_records if str(r["ServiceCode"]) == code][-1]
        refund = wrong["FinalPrice"]
        new_balance = prev_balance + refund
        rows.append([
            customer["CustomerID"], wrong["Name"], wrong["Phone"], wrong["SchemeName"],
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"), code, f"Deletion of {wrong['ServiceName']}", 0,
            "No", -refund, 0, -refund, new_balance, "Yes" if new_balance > 0 else "No"
        ])
    elif action == "correct":
        wrong = [r for r in cust_records if str(r["ServiceCode"]) == code][-1]
        refund = wrong["FinalPrice"]
        balance_after_refund = prev_balance + refund
        rows.append([
            customer["CustomerID"], wrong["Name"], wrong["Phone"], wrong["SchemeName"],
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"), code, f"Correction of {wrong['ServiceName']}", 0,
            "No", -refund, 0, -refund, balance_after_refund, "Yes" if balance_after_refund > 0 else "No"
        ])
        name, price = services[correct_code]
        discount = 0.5 if balance_after_refund > 0 else 1.0
        final = price * discount
        new_balance = balance_after_refund - final
        rows.append([
            customer["CustomerID"], wrong["Name"], wrong["Phone"], wrong["SchemeName"],
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"), correct_code, name, price,
            "Yes" if discount < 1 else "No", final, 0, final, new_balance,
            "Yes" if new_balance > 0 else "No"
        ])

    for row in rows:
        sheet.append_row(row)

    return jsonify({"status": "success", "balance": new_balance, "rows": rows})

if __name__ == "__main__":
    app.run(debug=True)