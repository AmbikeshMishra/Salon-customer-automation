import qrcode
import uuid
import json   # <-- add this

def generate_qr(customer_name, phone, scheme_name="Default", scheme_active=True):
    # Create a unique ID for the customer
    customer_id = str(uuid.uuid4())[:8]  # short unique ID

    # Data encoded in QR (must be valid JSON string)
    qr_data = {
        "CustomerID": customer_id,
        "Name": customer_name,
        "Phone": phone,
        "SchemeName": scheme_name,
        "SchemeActive": scheme_active
    }

    # ✅ Use json.dumps to ensure proper JSON format
    qr = qrcode.make(json.dumps(qr_data))

    filename = f"{customer_name}_QR.png"
    qr.save(filename)

    print(f"✅ QR code generated: {filename}")
    print(f"Customer ID: {customer_id}")
    return qr_data

# Example usage
if __name__ == "__main__":
    generate_qr("Ambikesh Mishra", "8700610641")