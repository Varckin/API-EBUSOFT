from fastapi import UploadFile, File, Form, HTTPException, APIRouter
from security.AES.service import generate_key, encrypt_aes, decrypt_aes
from security.AES.settings import SETTINGS
from security.AES.models import EncryptResponse, DecryptResponse
import base64


router = APIRouter(prefix="/aes", tags=["aes"])


@router.get("/health", response_model=str)
async def health() -> str:
    """Health check specifically for the aes module."""
    return "ok"

@router.get("/generate-key")
async def get_key():
    """Generate a new AES key"""
    return {"key": generate_key()}

@router.post("/encrypt", response_model=EncryptResponse)
async def encrypt(
    key: str = Form(...),
    plaintext: str | None = Form(None, description="Text to encrypt"),
    file: UploadFile | None = File(None, description="File to encrypt")
):
    """Universal endpoint for encrypting text or files"""
    if not plaintext and not file:
        raise HTTPException(status_code=400, detail="Either 'plaintext' or 'file' must be provided")

    # Get data
    if plaintext:
        data = plaintext.encode()
    else:
        if file.spool_max_size > SETTINGS.MAX_FILE_SIZE_BYTES:
            raise HTTPException(
                status_code=400,
                detail=f"Maximum file size is {SETTINGS.MAX_FILE_SIZE_BYTES} bytes"
            )
        data = await file.read()

    # Encrypt
    try:
        result = encrypt_aes(data, key)
        return EncryptResponse(
            ciphertext=result["ciphertext"],
            nonce=result["nonce"],
            tag=result["tag"],
            filename=file.filename + ".enc" if file else None
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/decrypt", response_model=DecryptResponse)
async def decrypt(
    key: str = Form(...),
    nonce: str = Form(...),
    tag: str = Form(...),
    ciphertext: str | None = Form(None, description="Text to decrypt"),
    file: UploadFile | None = File(None, description="File to decrypt (Base64 encoded)")
):
    """Universal endpoint for decrypting text or files"""
    if not ciphertext and not file:
        raise HTTPException(status_code=400, detail="Either 'ciphertext' or 'file' must be provided")

    # Get data
    if ciphertext:
        data = ciphertext
    else:
        if file.spool_max_size > SETTINGS.MAX_FILE_SIZE_BYTES:
            raise HTTPException(
                status_code=400,
                detail=f"Maximum file size is {SETTINGS.MAX_FILE_SIZE_BYTES} bytes"
            )
        content = await file.read()
        data = content.decode()  # File should be Base64

    # Decrypt
    try:
        plaintext_bytes = decrypt_aes(data, key, nonce, tag)
        if file:
            return DecryptResponse(
                filename=file.filename.replace(".enc", ""),
                content_b64=base64.b64encode(plaintext_bytes).decode()
            )
        else:
            return DecryptResponse(plaintext=plaintext_bytes.decode())
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
