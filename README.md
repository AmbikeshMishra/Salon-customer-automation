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


📸 Demo Screens
- Customer lookup and balance view
- Service selection and billing preview
- Top-up flow
- Transaction history panel
- QR scanner interface
(Add screenshots or GIFs in assets/ and embed here)

📊 Business Impact
- ⏱️ Faster checkout and reduced billing errors
- 📈 Clear revenue tracking and service mix analysis
- 🔁 Improved customer retention via prepaid packages
- 👥 Staff-friendly interface with minimal training required

🔮 Future Enhancements
- Inventory tracking for consumables
- Multi-branch support
- Role-based access control
- Thermal printer integration for receipts
- Loyalty points and referral system

👨‍💻 About Me
I’m Ambikesh Mishra, a freelance IT professional specializing in Python, agentic AI, and workflow automation. This app is part of my portfolio showcasing hyperlocal automation solutions for small businesses.

Let me know if you'd like help writing a matching LinkedIn post or Upwork pitch to showcase this project professionally.
