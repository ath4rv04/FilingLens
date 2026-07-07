import os
from filinglens.ocr.base import BaseOCRProvider
from filinglens.ocr.models import OCRPage, OCRBlock, OCRLine, OCRWord
from filinglens.utils.logging import get_logger

logger = get_logger(__name__)

class PaddleOCRService(BaseOCRProvider):
    """PaddleOCR integration wrapper honoring hardware bounds."""

    def __init__(self):
        from paddleocr import PaddleOCR
        
        device = os.getenv("OCR_DEVICE", "auto")
        
        model_dir = os.getenv("PADDLE_MODEL_DIR", "data/models/paddleocr")
        self.min_confidence = float(os.getenv("OCR_MIN_CONFIDENCE", "0.60"))
        
        os.makedirs(model_dir, exist_ok=True)
        
        kwargs = {
            "lang": 'en'
        }
        
        if device != "auto":
            kwargs["device"] = device
            
        self.ocr = PaddleOCR(**kwargs)

    def process_page(self, image_path: str, page_number: int) -> OCRPage:
        try:
            results = self.ocr.ocr(str(image_path))
        except Exception as e:
            logger.error("PaddleOCR execution failed (underlying framework bug): %s", e)
            return OCRPage(page_number=page_number, blocks=[], confidence=0.0)
            
        if not results or not results[0]:
            return OCRPage(page_number=page_number, blocks=[], confidence=0.0)
            
        page_results = results[0]
        
        lines = []
        page_conf = 0.0
        valid_words = 0
        
        for line in page_results:
            bbox, (text, confidence) = line
            
            if confidence < self.min_confidence:
                continue
                
            xs = [p[0] for p in bbox]
            ys = [p[1] for p in bbox]
            xmin, xmax = min(xs), max(xs)
            ymin, ymax = min(ys), max(ys)
            
            word = OCRWord(
                text=text,
                confidence=confidence,
                bbox=(xmin, ymin, xmax, ymax)
            )
            
            lines.append(OCRLine(
                words=[word],
                bbox=(xmin, ymin, xmax, ymax)
            ))
            
            page_conf += confidence
            valid_words += 1
            
        avg_conf = page_conf / valid_words if valid_words > 0 else 0.0
        
        # Map to a single logical block.
        main_block = OCRBlock(lines=lines, bbox=(0, 0, 0, 0)) if lines else None
        blocks = [main_block] if main_block else []
        
        return OCRPage(
            page_number=page_number,
            blocks=blocks,
            confidence=avg_conf
        )
