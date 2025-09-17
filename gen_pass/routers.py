from fastapi import APIRouter, HTTPException
from gen_pass.models import PasswordRequest
from typing import List
from gen_pass.service import GeneratorPass

router = APIRouter(prefix="/genpass", tags=["genpass"])


@router.get("/health", response_model=str)
async def health() -> str:
    """Health check specifically for the genpass module."""
    return "ok"

@router.post("/generate", response_model=List[str])
async def gen_pass(request: PasswordRequest) -> List[str]:
    """Generate a random password using parameters"""
    result: List[str] = []
    pass_service = GeneratorPass()

    for _ in range(request.count):
        try:
            result.append(
                pass_service.gen_pass(
                    length=request.length,
                    use_lower=request.use_lower,
                    use_upper=request.use_upper,
                    use_digits=request.use_digits,
                    use_special=request.use_special
                )
            )
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

    return result
