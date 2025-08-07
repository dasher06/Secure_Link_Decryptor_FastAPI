# Secure GDrive Link Encryptor and Decryptor (FastAPI Version)

This project helps you to securely share **Google Drive files** by encrypting the file link using a **10-digit password**. The encrypted link is shared with recipient, and they can decrypt it using a simple web interface.

This version is built using **FastAPI**, replacing the earlier version that used **Flask**.

For the **Flask** version you can visit:  
- https://github.com/dasher06/Secure_Gdrive_File

---

## How to Run the Project Locally

### Steps

1. **Clone this repository**:
   ```bash
   git clone https://github.com/your-username/Secure_Link_Decryptor_FastAPI.git
   cd Secure_Link_Decryptor_FastAPI
   ```

2. **Install the required Python packages**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Start the FastAPI server**:
   ```bash
   uvicorn decrypt_api:app --reload
   ```

4. **Open in browser**:
   - Go to [http://127.0.0.1:8000/decrypt_link](http://127.0.0.1:8000/decrypt_link)

---

## How to Deploy to Google Cloud Run

1. **Create a Google Cloud Project** and enable:
   - Cloud Run
   - Cloud Build
   - Artifact Registry

2. **Install Google Cloud CLI** and log in:
   ```bash
   gcloud auth login
   gcloud config set project [PROJECT_ID]
   ```

3. **Submit your app for deployment**:
   ```bash
   gcloud builds submit --tag gcr.io/[PROJECT_ID]/secure-gdrive-fastapi
   gcloud run deploy secure-gdrive-fastapi \
       --image gcr.io/[PROJECT_ID]/secure-gdrive-fastapi \
       --platform managed \
       --region [YOUR_REGION] \
       --allow-unauthenticated
   ```

4. Once deployed, you’ll get a public link to use like this:
   - `https://secure-gdrive-fastapi-xxxxxx.run.app/decrypt_link?encrypted=...`

Share this URL along with the password.

---

## How the Project Works

1. You take a **Google Drive file link** and encrypt it with a **10-digit password**.
2. You share the **encrypted string** using a URL.
3. The recipient visits the **decryption page**, pastes the encrypted string, and types in the password.
4. If correct, the original **Google Drive link** is revealed.

---

## How I Ran the Project (Deployment Steps)

### 1. Localhost (Basic Testing)

Initially, I ran the Python Flask application locally on my machine for basic testing.

I opened a terminal and executed:
```bash
uvicorn decrypt_api:app --reload
```

This started the web server at:

- `http://127.0.0.1:5000/decrypt_link`

This setup was sufficient for local testing, but access was limited to my machine only.

---

### 2. Ngrok (Temporary Public Access)

To enable temporary **public access**, I used **ngrok**.

After installing it, I ran the following command:
```bash
ngrok http 5000
```

**Ngrok** provided a public-facing URL **(please note: these links are no longer active)**:

- `https://secure-decryptor-1068809376566.us-central1.run.app/decrypt_link?encrypted=gAAAAABoV_6h-28TYpIJehShsPnfESGRAaXWLMhSsXC1kfINaxaL-4dPT1Lsuba7OSvJgk0U5XgpXLmKuAXPBqmA6ap5m-MH_66UW9HMQ117N1HHpWDRmuPTJxCwfYj0bTX_uW1CsfHr8nXQo_Vm6_1rvn4NWvOwYpBj92HyepVK4PC_rDYZ6J8=`


This allowed anyone with the link to access the web page. 

However, my local terminal had to remain active, and the HTTPS certificate provided by ngrok was self-signed, which may trigger browser security warnings.

---

### 3. Render (Permanent Public Access)

Later, I deployed the application to **Render.com**, a free hosting platform for web apps.

I pushed my code to GitHub and connected the repository to Render for **automatic deployment**.

Although **Render** successfully built and deployed the application, it introduced significant changes to the code and output. The **original logic** was altered in several areas, which was not ideal for this project.

Here’s an example of a Render-generated URL **(note: link is no longer active)**:

- `https://encryptedlinkapp.onrender.com/decrypt_link?encrypted=gAAAAABoVWml-d0XY_H9foOHshdv4WE11_l7Bony0O2AGPYcKtF2UfE49_8yMbcEyJKKtv8W1KnRuDOF47_hP-oMBWQqYlf4bLy-nicouNw_IT5HVfU3dBHimdZ9KrW5CgEczV3GA3CK86yHihpxrrjmjz4pR83AFQ==`

Even though this made the application publicly available 24/7, the deployment compromised the integrity of the original code.

---

### 4. Google Cloud Platform (Current Deployment using FastAPI)

Currently, the project is deployed on **Google Cloud Platform (GCP)** using **Cloud Run**, specifically to avoid the **code alterations** that occurred with **Render**.

I created a **Dockerfile** for the FastAPI app, but used the gcloud CLI to build and deploy it via **Google Cloud Build**, which handled the **containerization** automatically.

Here’s a sample live deployment link (accessible at the time of writing):

🔓 Decryption Page:

- https://email-link-encryption-1068809376566.us-central1.run.app/decrypt_link?encrypted=gAAAAABoitaIj1z0f2zVW2wLOPVAknYV76n3z_S05YRbn4DHVvDVM2tNIhVJbOMZEOfwQrtv-iimHoLpNj1aNm4Dp5zAzgvXV81ObXzt2-NfYebmagNpJcJVmCOZokJenMyKLt6B7Tm5mob7BL6D-bBpZHgmOlyuUlTimu4-NndsSZI5xaOvmtU=

When prompted, enter the decryption key:

🔐 Decryption Key: 

- **1234567890**

This approach has proven to be the most **effective**. The server is live 24/7, and I was able to deploy the application without any **code modifications** or **runtime errors**.

---

## What's in the Project

- `decrypt_api.py`: The FastAPI application for link decryption
- `requirements.txt`: Python packages needed to run the app
- `templates/decrypt_link.html`: The form where users paste their encrypted link and key
- `Dockerfile`: Helps in building the app if needed (used by Cloud Build)
- `.dockerignore`: Prevents unnecessary files from going into the Docker image
- `.gitignore`: Keeps sensitive or unnecessary files out of version control

> Note: Although this repository contains a Dockerfile and .dockerignore, Docker was not manually used to build or run the application during deployment. Instead, Google Cloud Build automatically handled the containerization process based on the Dockerfile. This approach eliminated the need to run docker build or docker push commands locally.
---

## Technologies Used

- Python 3
- FastAPI (Web framework)
- Cryptography (For encryption and decryption)
- Jinja2 (For HTML templates)
- Uvicorn (Local server for FastAPI)
- Google Cloud Platform (Deployment)

---

## Acknowledgements

Thanks to my uncles **Kiru Veerappan** and **Udhayan Nagarajan** for their encouragement and support.

---

Created by **Trinab Shan**  
GitHub: [@dasher06](https://github.com/dasher06)

