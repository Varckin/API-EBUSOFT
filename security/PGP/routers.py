from fastapi import HTTPException, Form, UploadFile, File, APIRouter
from security.PGP.models import PGPKeyRequest, PGPKeyResponse, PGPEncryptResponse, PGPDecryptResponse
from security.PGP.service import generate_pgp_key, encrypt_message, decrypt_message, encrypt_file, decrypt_file


router = APIRouter(prefix="/pgp", tags=["pgp"])


@router.get("/health", response_model=str)
async def health() -> str:
    """Health check specifically for the pgp module."""
    return "ok"

@router.post("/generate-key", response_model=PGPKeyResponse)
async def generate_key(request: PGPKeyRequest):
    """
    Generate PGP keys (RSA/ECC) with optional passphrase protection.
    """
    try:
        public_key, private_key = generate_pgp_key(request)
        return PGPKeyResponse(public_key=public_key, private_key=private_key)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/encrypt", response_model=PGPEncryptResponse)
async def encrypt_endpoint(
    public_key: str = Form(...),
    text: str | None = Form(None),
    file: UploadFile | None = File(None),
):
    """
    Encrypt either text or a file using the provided public PGP key.
    """
    try:
        if text:
            encrypted = encrypt_message(text, public_key)
            return PGPEncryptResponse(encrypted_data=encrypted, type="text")
        elif file:
            encrypted = encrypt_file(file, public_key)
            return PGPEncryptResponse(encrypted_data=encrypted, type="file")
        else:
            raise HTTPException(status_code=400, detail="Either 'text' or 'file' must be provided")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Encryption failed: {e}")

@router.post("/decrypt", response_model=PGPDecryptResponse)
async def decrypt_endpoint(
    private_key: str = Form(...),
    passphrase: str | None = Form(None),
    encrypted_text: str | None = Form(None),
    encrypted_file: str | None = Form(None),
):
    """
    Decrypt either text or a file using the provided private PGP key.
    """
    try:
        if encrypted_text:
            decrypted = decrypt_message(encrypted_text, private_key, passphrase)
            return PGPDecryptResponse(decrypted_data=decrypted, type="text")

        elif encrypted_file:
            decrypted_bytes = decrypt_file(encrypted_file, private_key, passphrase)
            return PGPDecryptResponse(
                decrypted_data=decrypted_bytes.decode(errors="ignore"),
                type="file"
            )

        else:
            raise HTTPException(status_code=400, detail="Either 'encrypted_text' or 'encrypted_file' must be provided")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Decryption failed: {e}")
