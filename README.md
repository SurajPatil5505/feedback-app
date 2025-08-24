# Live Feedback App (LFA)
This project allows you to collect user feedback (text + photo), generate a custom feedback image, and automatically showing it on display, monitor, or any browser in local area network.

### Project Structure

```
feedback-app/
│
├── app.py                   # Flask server for capturing feedback
├── generate_feeback_card.py # Feedback image generation script
├── templates/
│   |-- index.html           # Web form for feedback entry
    |-- viewer.html          # Feedbacks viewers page
├── static/
│   └── uploads/             # Auto-created to store generated images
├── requirements.txt         # Python dependencies
└── README.md                # This file
```

## PART 1: How to Set It Up

1. **Install required Python packages:**
   ```bash
   pip install -r requirements.txt
   ```

## PART 2: HOW TO USE

### Step 1: Run the Web App

```bash
python app.py
```

- Open `http://localhost:5000` in your browser.
- Fill in the form: **Name**, **Feedback**, **capture photo** and **submit**.

---

### Step 2: What Happens

- Your image is saved to `/static/uploads/`
- The script creates a beautiful image with your feedback
- That image + feedback will visible on viewer page in network.
- To view live feebacks system open `http://localhost:5000/viewer` in another terminal on same system and if we want to view in another system use `http://Ip_address_of_server_pc:5000/viewer` to view live feeback system.

---

## Customize or Extend

- Modify layout in `generate_feedback_card.py` for different styles.
- Edit `templates/index.html` and `templates/viewer.html` to change form UI.

---