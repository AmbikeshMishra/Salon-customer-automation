✂️ Barber Shop Automation App
📌 Overview
This project is a lightweight, real-world automation system designed for barber shops and salons. It streamlines customer management, service selection, billing, and transaction logging — all through a clean, fast, and staff-friendly interface. Built for hyperlocal businesses that want digital efficiency without complex software.

🚀 Features
💇 Customer Management
- Mobile number lookup – Quickly find existing customers by phone.
- New customer registration – Add fresh entries with minimal input.
- Balance tracking – Show current wallet balance and update after each transaction.
- Top-up system – Add prepaid amounts to customer accounts.
🧾 Service Selection & Billing
- Service catalog with pricing – Haircut, Shaving, Facial, Hair Colour, Massage, etc.
- Multi-service selection – Add multiple services to a single bill.
- Live billing preview – See selected services and total before finalizing.
- Finalize & log – Confirm service and update customer ledger.
- Undo last transaction – Roll back the most recent service entry.
- Fix mistakes – Delete specific services before finalizing.
📊 Transaction History
- Recent transactions viewer – Show last 10 or 20 entries with timestamps.
- Top-up and service logs – Chronological view of all customer interactions.
- Running balance updates – Real-time balance after each transaction.
📱 QR & Scanner Tools
- QR scanner integration – Identify customers or services via QR codes.
- Start scanner button – Launch camera-based scanning from the UI.
🧠 Smart UX Touches
- Minimalist layout – Designed for fast operation by staff.
- Color-coded buttons – Green for top-up, blue for finalize, red for delete, yellow for undo.
- Session summary – Total amount handled in current view.

🛠 Tech Stack
- Backend: Python (Flask)
- Frontend: HTML + Bootstrap (or Streamlit for rapid prototyping)
- Data Storage: Google Sheets or SQLite
- Integrations: QR scanner (browser-based), WhatsApp/SMS (optional)

📂 Project Structure
```barber_app/
│── src/
│   ├── app.py                 # Main app logic
│   ├── customer.py            # Customer lookup and registration
│   ├── services.py            # Service catalog and selection
│   ├── billing.py             # Top-up, finalize, undo
│   ├── transactions.py        # History and logging
│── templates/                 # HTML templates
│── static/                    # CSS, JS, icons
│── config/                    # Credentials (ignored in .gitignore)
│── assets/                    # Screenshots and demo GIFs
│── README.md
```

⚙️ Setup Instructions
1. Clone the repository
git clone https://github.com/<your-username>/barber_app.git
cd barber_app


2. Create and activate a virtual environment
- Windows (cmd):
python -m venv venv
venv\Scripts\activate
- Windows (PowerShell):
python -m venv venv
venv\Scripts\Activate.ps1
- Linux/macOS:
python3 -m venv venv
source venv/bin/activate


3. Install dependencies
pip install -r requirements.txt


4. Configure credentials (if using Google Sheets)
- Place your credential.json in the config/ folder (this folder is ignored by .gitignore).
- Set environment variable:
export GOOGLE_APPLICATION_CREDENTIALS="config/credential.json"


- (On Windows PowerShell, use setx GOOGLE_APPLICATION_CREDENTIALS "config\credential.json")
If you’re only using SQLite, no credentials are required.5. Run the apppython src/app.py
Then open http://localhost:5000 in your browser.



📸 Demo Screens
- Customer lookup and balance view
  <img width="547" height="555" alt="image" src="https://github.com/user-attachments/assets/cfba3704-5976-4968-aa9d-62a80f1cd4bf" />

- Service selection and billing preview
  <img width="1127" height="912" alt="image" src="https://github.com/user-attachments/assets/9a2ded3f-11f6-43bf-b013-2dd9f4b8f049" />


- Top-up flow
 <img width="1118" height="1025" alt="image" src="https://github.com/user-attachments/assets/4e836f9e-d0d6-4329-8ef6-7b528f993a6e" />


- Transaction history panel
<img width="1136" height="552" alt="image" src="https://github.com/user-attachments/assets/1f953c9b-85f7-478a-8b05-490fc6aee1af" />


- QR scanner interface
<img width="585" height="493" alt="image" src="https://github.com/user-attachments/assets/cff477b3-8ea9-4175-9b57-f7ecec970ad9" />


📊 Business Impact
- ⏱️ Faster checkout and reduced billing errors
- 📈 Clear revenue tracking and service mix analysis
- 🔁 Improved customer retention via prepaid packages
- 👥 Staff-friendly interface with minimal training required

