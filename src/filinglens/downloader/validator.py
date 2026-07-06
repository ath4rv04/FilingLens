import fitz


class FilingValidator:
    """Validates structural HTTP rules seamlessly binding file logic against binary payloads prior to physical writes."""

    @staticmethod
    def is_valid_pdf_content(content: bytes) -> tuple[bool, int, str]:
        if not content:
            return False, 0, "Empty payload"

        if not content.startswith(b"%PDF"):
            return False, 0, "Invalid magic bytes (not a PDF)."

        if (
            len(content) < 100 * 1024
        ):  # Less than 100KB typically means 404 or anti-bot payload rather than a full annual report
            return (
                False,
                0,
                "Payload dimension smaller than typical Annual Reports bounds (100KB).",
            )

        try:
            doc = fitz.open(stream=content, filetype="pdf")
            pages = len(doc)
            if pages == 0:
                return False, 0, "No pages detected natively."
            return True, pages, "success"
        except Exception as e:
            return False, 0, f"Corrupted PDF formatting: {e}"
