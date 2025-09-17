from fastapi import FastAPI
from cert.routers import router as cert
from speech.routers import router as speech
from ytdlp.routers import router as ytdlp
from gen_uuid.routers import router as genuuid
from gen_pass.routers import router as genpass
from ip_geo_lookup.routers import router as ipgeo
from dns_forw_rev.routers import router as dns
from traceroute.routers import router as traceroute
from dotenv import load_dotenv

load_dotenv()
app = FastAPI(title="API EBUSOFT TECHNOLOGY", version= "0.5.21")

app.include_router(cert)
app.include_router(speech)
app.include_router(ytdlp)
app.include_router(genuuid)
app.include_router(genpass)
app.include_router(ipgeo)
app.include_router(dns)
app.include_router(traceroute)


@app.get("/health")
async def health() -> str:
    return "ok"
