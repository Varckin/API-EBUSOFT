from fastapi import FastAPI, Depends
from contextlib import asynccontextmanager
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from cert.routers import router as cert
from speech.routers import router as speech
from ytdlp.routers import router as ytdlp
from gen_uuid.routers import router as genuuid
from gen_pass.routers import router as genpass
from ip_geo_lookup.routers import router as ipgeo
from dns_forw_rev.routers import router as dns
from traceroute.routers import router as traceroute
from gen_id.routers import router as idgen
from slug.routers import router as slug
from gen_hash.routers import router as hash
from base64_coder.routers import router as base64
from url_codec.routers import router as urlcodec
from qr_code.routers import router as qr_code
from data_validator.routers import router as validator
from data_converter.routers import router as converter
from security.AES.routers import router as aes
from security.PGP.routers import router as pgp
from security.RSA.routers import router as rsa
from gen_faker.routers import router as faker
from clamav_antivirus.routers import router as clamav
from core.auth.user_endpoints import router as auth_user

from internal_functional.sollaire.routers import router as sollaire
from internal_functional.info.routers import router as info
from core.auth.admin_endpoints import router as auth_admin

from core.rate_limit.middleware import RateLimitMiddleware
from core.auth.middleware import TokenAuthMiddleware
from core.auth.database import init_db
from core.auth.dependencies import require_role
from dotenv import load_dotenv

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(title="API EBUSOFT TECHNOLOGY", version= "1.38 (MVP)",
              redoc_url=None, lifespan=lifespan)

app.add_middleware(RateLimitMiddleware)
app.add_middleware(TokenAuthMiddleware)
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(cert, dependencies=[Depends(require_role('admin', 'dev', 'user'))])
app.include_router(speech, dependencies=[Depends(require_role('admin', 'dev', 'user'))])
app.include_router(ytdlp, dependencies=[Depends(require_role('admin', 'dev', 'user'))])
app.include_router(genuuid, dependencies=[Depends(require_role('admin', 'dev', 'user'))])
app.include_router(genpass, dependencies=[Depends(require_role('admin', 'dev', 'user'))])
app.include_router(ipgeo, dependencies=[Depends(require_role('admin', 'dev', 'user'))])
app.include_router(dns, dependencies=[Depends(require_role('admin', 'dev', 'user'))])
app.include_router(traceroute, dependencies=[Depends(require_role('admin', 'dev', 'user'))])
app.include_router(idgen, dependencies=[Depends(require_role('admin', 'dev', 'user'))])
app.include_router(slug, dependencies=[Depends(require_role('admin', 'dev', 'user'))])
app.include_router(hash, dependencies=[Depends(require_role('admin', 'dev', 'user'))])
app.include_router(base64, dependencies=[Depends(require_role('admin', 'dev', 'user'))])
app.include_router(urlcodec, dependencies=[Depends(require_role('admin', 'dev', 'user'))])
app.include_router(qr_code, dependencies=[Depends(require_role('admin', 'dev', 'user'))])
app.include_router(validator, dependencies=[Depends(require_role('admin', 'dev', 'user'))])
app.include_router(converter, dependencies=[Depends(require_role('admin', 'dev', 'user'))])
app.include_router(aes, dependencies=[Depends(require_role('admin', 'dev', 'user'))])
app.include_router(pgp, dependencies=[Depends(require_role('admin', 'dev', 'user'))])
app.include_router(rsa, dependencies=[Depends(require_role('admin', 'dev', 'user'))])
app.include_router(faker, dependencies=[Depends(require_role('admin', 'dev', 'user'))])
app.include_router(clamav, dependencies=[Depends(require_role('admin', 'dev', 'user'))])
app.include_router(auth_user, dependencies=[Depends(require_role('admin', 'dev', 'user'))])

app.include_router(sollaire, include_in_schema=False, dependencies=[Depends(require_role('admin'))])
app.include_router(info, include_in_schema=False, dependencies=[Depends(require_role('admin'))])
app.include_router(auth_admin, include_in_schema=False)


@app.get("/health")
async def health() -> str:
    return "ok"

@app.get("/favicon.ico")
async def favicon():
    return FileResponse("static/LogoEbusoft.png")
