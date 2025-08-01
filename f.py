import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/send_email/"

st.set_page_config(page_title="AI Email Sender", layout="centered")
st.title("📧 AI Email Sender")

with st.form("email_form"):
    subject = st.text_input("Subject")
    recipients = st.text_area("Recipient Emails (comma separated)", height=100)
    prompt = st.text_area("Custom Prompt for LLM (Optional)", height=150, placeholder="Leave blank to use the default email template.")
    submitted = st.form_submit_button("Send Email")

    if submitted:
        if not subject or not recipients:
            st.warning("Please fill in both the subject and recipient emails.")
        else:
            # Split recipient string into list
            recipient_list = [email.strip() for email in recipients.split(",") if email.strip()]
            try:
                response = requests.post(API_URL, json={
                    "subject": subject,
                    "recipients": recipient_list,
                    "prompt": prompt
                })
                if response.status_code == 200:
                    data = response.json()
                    if "error" in data:
                        st.error(f"❌ Error: {data['error']}")
                    else:
                        st.success("✅ Email sent to all recipients!")
                        st.write(f"📬 Sent to: {', '.join(data['recipients'])}")
                        with st.expander("Show Generated Email"):
                            st.write(data["email_body"])
                else:
                    st.error(f"❌ Server error: {response.status_code}")
            except Exception as e:
                st.error(f"🔌 Connection error: {str(e)}")
