from fastapi import FastAPI
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
from id_generator.routers import router as idgen
from slug.routers import router as slug
from gen_hash.routers import router as hash
from base64_coder.routers import router as base64
from url_codec.routers import router as urlcodec
from qr_code.routers import router as qr_code
from dotenv import load_dotenv

load_dotenv()
app = FastAPI(title="API EBUSOFT TECHNOLOGY", version= "0.7.95",
              redoc_url=None)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(cert)
app.include_router(speech)
app.include_router(ytdlp)
app.include_router(genuuid)
app.include_router(genpass)
app.include_router(ipgeo)
app.include_router(dns)
app.include_router(traceroute)
app.include_router(idgen)
app.include_router(slug)
app.include_router(hash)
app.include_router(base64)
app.include_router(urlcodec)
app.include_router(qr_code)


@app.get("/health")
async def health() -> str:
    return "ok"

@app.get("/favicon.ico")
async def favicon():
    return FileResponse("static/LogoEbusoft.png")
