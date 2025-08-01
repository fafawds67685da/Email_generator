import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/send_email/"

st.set_page_config(page_title="AI Email Sender", layout="centered")
st.title("📧 AI Email Sender")

with st.form("email_form"):
    subject = st.text_input("Subject")
    recipient = st.text_input("Recipient Email")
    submitted = st.form_submit_button("Send Email")

    if submitted:
        if not subject or not recipient:
            st.warning("Please fill in both the subject and recipient.")
        else:
            try:
                response = requests.post(API_URL, json={
                    "subject": subject,
                    "recipient": recipient
                })
                if response.status_code == 200:
                    data = response.json()
                    if "error" in data:
                        st.error(f"❌ Error: {data['error']}")
                    else:
                        st.success("✅ Email sent successfully!")
                        with st.expander("Show Generated Email"):
                            st.write(data["email_body"])
                else:
                    st.error(f"❌ Server error: {response.status_code}")
            except Exception as e:
                st.error(f"🔌 Connection error: {str(e)}")
