import httpx
from translate.models import TranslateRequest, TranslateResponse
from translate.settings import CONFIG


class TranslateService:
    """
    Service layer responsible for interacting with the Translate API.
    """

    def __init__(self):
        self.base_url = CONFIG.TRANSLATE_BASE_URL
        self.timeout = CONFIG.timeout

    async def translate(self, request: TranslateRequest) -> TranslateResponse:
        """
        Sends a request to the Translate API and returns the parsed response.
        """
        params = {"dl": request.dl, "text": request.text}
        if request.sl:
            params["sl"] = request.sl

        async with httpx.AsyncClient(base_url=self.base_url, timeout=self.timeout) as client:
            response = await client.get("/translate", params=params)
            response.raise_for_status()
            return TranslateResponse(**response.json())

    async def get_languages(self) -> dict:
        """
        Retrieves a list of supported languages from the Translate API.
        """
        async with httpx.AsyncClient(base_url=self.base_url, timeout=self.timeout) as client:
            response = await client.get("/languages")
            response.raise_for_status()
            return response.json()
