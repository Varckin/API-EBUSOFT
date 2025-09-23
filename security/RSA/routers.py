from fastapi import HTTPException, Response, APIRouter
from security.RSA.models import RSAKeyRequest, RSAKeyResponse
from security.RSA.service import generate_private_key, serialize_private_key, serialize_public_key, encode_base64


router = APIRouter(prefix="/rsa", tags=["rsa"])


@router.get("/health", response_model=str)
async def health() -> str:
    """Health check specifically for the rsa module."""
    return "ok"

@router.post("")
async def generate_rsa_keys(req: RSAKeyRequest):
    """
    Generate RSA key pair according to the specified parameters.
    The output can be returned as JSON or a downloadable PEM file.
    """
    try:
        private_key = generate_private_key(req.key_size, req.public_exponent)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    private_pem = serialize_private_key(private_key, req.private_format, req.passphrase if req.encrypt_private else None)
    public_pem = serialize_public_key(private_key, req.public_format)

    if req.output_base64:
        private_out = encode_base64(private_pem)
        public_out = encode_base64(public_pem)
    else:
        private_out = private_pem.decode("utf-8")
        public_out = public_pem.decode("utf-8")

    if req.output_type == "download":
        content = b"-----BEGIN PRIVATE KEY-----\n" + private_pem + b"\n-----END PRIVATE KEY-----\n\n" + public_pem
        headers = {
            "Content-Disposition": f'attachment; filename="rsa_{req.key_size}.pem"',
            "Content-Type": "application/x-pem-file",
        }
        return Response(content=content, media_type="application/x-pem-file", headers=headers)

    return RSAKeyResponse(
        private_key=private_out,
        public_key=public_out,
        key_size=req.key_size,
        public_exponent=req.public_exponent,
    )
