from flask import Flask, request, jsonify
import smtplib
import random

app = Flask(__name__)

@app.route('/api/send-otp', methods=['POST'])
def send_otp():
    data = request.json
    email = data.get('email')

    if not email:
        return jsonify({'message': 'Email is required'}), 400

    # Generate a random OTP
    otp_code = str(random.randint(100000, 999999))

    # Email configuration
    sender_email = "your_email@example.com"
    sender_password = "your_password"
    subject = "Your OTP Verification Code"
    body = f"Your verification code is: {otp_code}"

    try:
        # Send the email
        with smtplib.SMTP("smtp.example.com", 587) as server:  # Replace with your SMTP server
            server.starttls()
            server.login(sender_email, sender_password)
            message = f"Subject: {subject}\n\n{body}"
            server.sendmail(sender_email, email, message)

        # Store the OTP for verification (e.g., in a session or database)
        # Example: session[email] = otp_code

        return jsonify({'message': 'OTP sent successfully', 'email': email}), 200

    except Exception as e:
        print("Error sending email:", e)
        return jsonify({'message': 'Failed to send OTP'}), 500

if __name__ == '__main__':
    app.run(debug=True)
