import pytest

from filinglens.ocr import PaddleOCRService


class FakeOCREngine:
    def ocr(self, image_path, cls):
        self.image_path = image_path
        self.cls = cls
        return [[[[0, 0], ["Revenue grew", 0.9]], [[1, 1], ["in FY2024", 0.8]]]]


def test_paddle_ocr_service_normalizes_text_and_confidence(tmp_path):
    image_path = tmp_path / "page_001.png"
    image_path.write_text("fake", encoding="utf-8")
    engine = FakeOCREngine()

    result = PaddleOCRService(ocr_engine=engine).extract_image(image_path)

    assert result.text == "Revenue grew in FY2024"
    assert result.confidence == pytest.approx(0.85)
    assert engine.cls is True
