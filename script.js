document.getElementById('emailForm').addEventListener('submit', async function (e) {
  e.preventDefault();
  const subject = document.getElementById('subject').value;
  const recipients = document.getElementById('recipients').value;
  const prompt = document.getElementById('prompt').value;
  const responseDiv = document.getElementById('response');

  const recipientList = recipients.split(',').map(email => email.trim());

  try {
    const response = await fetch('http://127.0.0.1:8000/send_email/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ subject, recipients: recipientList, prompt })
    });
    const data = await response.json();
    if (data.error) {
      responseDiv.innerHTML = `<p style="color: red;">❌ Error: ${data.error}</p>`;
    } else {
      responseDiv.innerHTML = `✅ Email sent to: ${data.recipients.join(', ')}<br><br><strong>Generated Email:</strong><br>${data.email_body}`;
    }
  } catch (error) {
    responseDiv.innerHTML = `<p style="color: red;">🔌 Connection error: ${error}</p>`;
  }
});
