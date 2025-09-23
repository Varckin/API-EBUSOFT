from fastapi import APIRouter, HTTPException
from gen_faker.models import FakerRequest, FakerResponse
from gen_faker.service import generate
from gen_faker.settings import CONFIG


router = APIRouter(prefix="/faker", tags=["faker"])


@router.post("", response_model=FakerResponse)
async def generate_post(req: FakerRequest):
    try:
        results = generate(
            provider=req.provider,
            locale=req.locale or CONFIG.default_locale,
            seed=req.seed,
            quantity=min(req.quantity, CONFIG.max_bulk),
            kwargs=req.provider_kwargs,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return FakerResponse(
        provider=req.provider,
        locale=req.locale or CONFIG.default_locale,
        seed=req.seed,
        quantity=req.quantity,
        results=results,
    )
