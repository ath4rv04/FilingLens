from abc import ABC, abstractmethod
from filinglens.ocr.models import OCRPage

class BaseOCRProvider(ABC):
    @abstractmethod
    def process_page(self, image_path: str, page_number: int) -> OCRPage:
        pass
