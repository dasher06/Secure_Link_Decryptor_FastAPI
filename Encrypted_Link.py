import os
import base64
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from cryptography.fernet import Fernet

if __name__ == "__main__":
    # 1. OAuth & Drive setup
    settings_file_path = "client_secrets.json"

    if not os.path.exists(settings_file_path):
        raise FileNotFoundError(f"No such file or directory: '{settings_file_path}'")

    print("File found")

    gauth = GoogleAuth()
    gauth.settings_file = settings_file_path
    gauth.LoadClientConfigFile(settings_file_path)
    gauth.LocalWebserverAuth()
    print("✅ Authentication complete")

    drive = GoogleDrive(gauth)

    file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
    print("Files in Google Drive:")
    for i, file in enumerate(file_list):
        print(f"{i + 1}. Title: {file['title']}, ID: {file['id']}")

    file_number = int(input("Enter the number of the file you want to choose: ")) - 1
    selected_file = file_list[file_number]

    print(f"Selected file: Title: {selected_file['title']}, ID: {selected_file['id']}")

    selected_file.InsertPermission({
        'type': 'anyone',
        'role': 'reader'
    })
    print(f"Permission granted to anyone for file: {selected_file['title']}")

    custom_key_input = input("Enter your custom encryption key (10 digits): ")
    if len(custom_key_input) != 10 or not custom_key_input.isdigit():
        raise ValueError("The custom encryption key must be exactly 10 digits long.")

    custom_key = custom_key_input.ljust(32, '0').encode()
    cipher_suite = Fernet(base64.urlsafe_b64encode(custom_key))
    shared_link = f'https://drive.google.com/file/d/{selected_file["id"]}/view'
    encrypted_link = cipher_suite.encrypt(shared_link.encode()).decode()

    print(f'Encrypted link: {encrypted_link}')
    print(f'Decryption key: {custom_key_input}')

    # ========== DECRYPTION LINK GENERATION ==========

    USE_CLOUD_RUN = True  # ← PRODUCTION mode ON

    if USE_CLOUD_RUN:
        # ✅ Replace with your actual deployed Cloud Run URL
        base_url = "https://your-cloud-run-url.run.app"
    else:
        # Localhost for development/testing
        port = int(os.environ.get("PORT", 8181))
        base_url = f"http://127.0.0.1:{port}"

    decryption_page_url = f"{base_url}/decrypt_link?encrypted={encrypted_link}"
    print(f"\nSend this link to decrypt the file:\n{decryption_page_url}")

    # ========== EMAIL SENDING (Edit your message & credentials here) ==========

    sender_email = "your_email@gmail.com"  # 🔒 Replace with your Gmail
    receiver_email = "recipient_email@example.com"  # 🔒 Replace with recipient's email
    password = "your_app_password"  # 🔒 Use environment variables or secrets in production

    message = MIMEMultipart("alternative")
    message["Subject"] = "Encrypted Google Drive Link"
    message["From"] = sender_email
    message["To"] = receiver_email

    # 📝 Replace this text with your actual email content
    text = f"""
Hello,

This is your encrypted file link.

Decryption Page:
{decryption_page_url}

Decryption Key: {custom_key_input}

You can update this email body to suit your needs.

Thank you.
"""
    part = MIMEText(text, "plain")
    message.attach(part)

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
            print("✅ Email sent successfully!")
    except Exception as e:
        print(f"❌ An error occurred while sending the email: {e}")

    # Manual testing reminder
    print(f"\n🔗 Open this URL in your browser to decrypt manually:")
    print(decryption_page_url)
