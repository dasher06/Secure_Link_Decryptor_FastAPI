import base64
import os
from pathlib import Path
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from cryptography.fernet import Fernet

app = FastAPI()

# === Template Configuration ===
BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

# Debug prints should be disabled in production
# print("TEMPLATE DIR:", BASE_DIR / "templates")

# === OAuth Callback Endpoint (optional - can be removed if not used) ===
@app.get("/", response_class=HTMLResponse)
async def oauth_callback(request: Request):
    code = request.query_params.get("code")
    if code:
        return HTMLResponse(content=f"<h3>✅ OAuth Code Received:</h3><p>{code}</p>", status_code=200)
    return HTMLResponse(content="<h3>⚠️ No OAuth Code Found.</h3>", status_code=400)

# === GET Request to Show Decryption Form ===
@app.get("/decrypt_link", response_class=HTMLResponse)
async def get_decrypt_link(request: Request, encrypted: str = ""):
    return templates.TemplateResponse("decrypt_link.html", {
        "request": request,
        "encrypted": encrypted,
        "decrypted": None,
        "error": None
    })

# === POST Request to Decrypt the Link ===
@app.post("/decrypt_link", response_class=HTMLResponse)
async def post_decrypt_link(
    request: Request,
    encrypted: str = Form(...),
    key: str = Form(...)
):
    error = None
    decrypted = None

    if not key or len(key) != 10 or not key.isdigit():
        error = "Invalid key: must be 10 digits"
    else:
        try:
            custom_key = key.ljust(32, '0').encode()
            fernet = Fernet(base64.urlsafe_b64encode(custom_key))
            decrypted = fernet.decrypt(encrypted.encode()).decode()
        except Exception as e:
            error = "Decryption failed. Please check your key and try again."
            # Avoid leaking internals to user: don't expose `str(e)` in production

    return templates.TemplateResponse("decrypt_link.html", {
        "request": request,
        "encrypted": encrypted,
        "decrypted": decrypted,
        "error": error
    })

# === Health Check Endpoints ===
@app.get("/status")
async def status():
    return {"status": "FastAPI is working!"}

@app.get("/healthz")
async def healthz():
    return {"ok": True}
