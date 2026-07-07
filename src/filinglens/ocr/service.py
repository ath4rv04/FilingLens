from filinglens.ocr.base import BaseOCRProvider
from filinglens.utils.logging import get_logger

logger = get_logger(__name__)

class OCRService:
    def __init__(self):
        self._provider: BaseOCRProvider | None = None
        
    def get_provider(self) -> BaseOCRProvider:
        if self._provider is None:
            logger.info("Initializing PaddleOCR bindings...")
            from filinglens.ocr.paddle import PaddleOCRService
            self._provider = PaddleOCRService()
        return self._provider

def get_ocr_service() -> OCRService:
    return OCRService()
