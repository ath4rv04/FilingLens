from filinglens.ocr.models import OCRResult, OCRPage, OCRBlock, OCRLine, OCRWord
from filinglens.ocr.base import BaseOCRProvider
from filinglens.ocr.paddle import PaddleOCRService
from filinglens.ocr.service import get_ocr_service, OCRService

__all__ = [
    "OCRResult", 
    "OCRPage", 
    "OCRBlock", 
    "OCRLine", 
    "OCRWord",
    "BaseOCRProvider",
    "PaddleOCRService",
    "get_ocr_service",
    "OCRService"
]
