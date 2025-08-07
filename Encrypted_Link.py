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
        # ✅ Correct production Cloud Run URL
        base_url = "https://email-link-fastapi-1068809376566.us-central1.run.app"
    else:
        # Localhost URL for testing
        port = int(os.environ.get("PORT", 8181))
        base_url = f"http://127.0.0.1:{port}"

    decryption_page_url = f"{base_url}/decrypt_link?encrypted={encrypted_link}"
    print(f"\nSend this link to decrypt the file:\n{decryption_page_url}")

    # ========== EMAIL SENDING ==========
    sender_email = "trinabshan06@gmail.com"
    receiver_email = "trinabtime@gmail.com"
    password = "yhcq gspr pnal rlfu"  # App Password

    message = MIMEMultipart("alternative")
    message["Subject"] = "Encrypted Google Drive Link"
    message["From"] = sender_email
    message["To"] = receiver_email

    text = f"""
Hello Kiruba mama,

I’ve created an encrypted Google Drive file link and deployed a secure decryption service.

To view the file:

🔓 Decryption Page:
{decryption_page_url}

When prompted, enter the decryption key below:
🔐 Decryption Key: {custom_key_input}

The decryption key is the number code for the word "Sorry".

Once the key is entered, the page will decrypt the original Google Drive link and allow you to access the file directly.

Thank you,
Trinab Shan
"""
    part = MIMEText(text, "plain")
    message.attach(part)
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
            print("Email sent successfully!")
    except Exception as e:
        print(f"An error occurred while sending the email: {e}")

    # Show link for manual testing (again)
    print(f"\n🔗 Open this URL in your browser to decrypt manually:")
    print(decryption_page_url)
