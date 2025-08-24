# LinkedIn Feedback Post App

This project allows you to collect user feedback (text + photo), generate a custom feedback image, and automatically post it to your **LinkedIn personal account** via API — all running locally on a Raspberry Pi using Python.

---

## PART 1: SETUP GUIDE

### What You’ll Need

-  Raspberry Pi (or any system) with Python 3.9+ installed
-  LinkedIn Developer Account
-  LinkedIn App with required permission: `w_member_social`
-  `.env` file with your LinkedIn access token

---

### Project Structure

```
feedback-app/
│
├── app.py                   # Flask server for capturing feedback
├── linkedin.py              # LinkedIn API integration
├── generate_feeback_card.py # Feedback image generation script
├── templates/
│   └── index.html           # Web form for feedback entry
├── static/
│   └── uploads/             # Auto-created to store generated images
├── .env                     # Store your LinkedIn token here
├── requirements.txt         # Python dependencies
└── README.md                # This file
```

---

### How to Set It Up

1. **Install required Python packages:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create `.env` file in the project root:**
   ```env
   LINKEDIN_ACCESS_TOKEN=your_linkedin_access_token_here
   ```

   >  Use your personal LinkedIn access token here.

5. **Make sure your LinkedIn App is properly set up:**
   - Visit: https://www.linkedin.com/developers/
   - Ensure `w_member_social` scope is enabled in your app
   - Generate an access token using Postman or a script (token lasts 60 days)

---

## PART 2: HOW TO USE

### Step 1: Run the Web App

```bash
python app.py
```

- Open `http://localhost:5000` in your browser.
- Fill in the form: **Name**, **Feedback**, and upload a **photo**.

---

### Step 2: What Happens

- Your image is saved to `/static/uploads/`
- The script creates a beautiful image with your feedback
- That image + feedback is posted to **your LinkedIn timeline**

> Your post will be public by default.
> You can modify the LinkedIn API payload to change visibility.

---

## Customize or Extend

- Modify layout in `generate_feedback_card.py` for different styles.
- Edit `templates/index.html` to change form UI.

---

## Tips & Testing

- Try submitting a few test entries to verify formatting.
- Make sure the image is under LinkedIn size limits.
- Check terminal logs for any posting errors.

---

## Cleaning Up

All uploaded and generated images are stored locally in `static/uploads`. You can delete them manually or set up auto-cleanup if needed.

---

## LinkedIn API Docs

Need more help with tokens or setup? Visit:
🔗 https://learn.microsoft.com/en-us/linkedin/consumer/integrations/self-serve/sign-in-with-linkedin

---