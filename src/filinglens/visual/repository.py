import sqlite3
from pathlib import Path
from PIL import Image
from filinglens.settings import FINANCE_DB_PATH

class VisualRepository:
    def __init__(self, db_path: str | Path = FINANCE_DB_PATH):
        self.db_path = db_path
        self._init_db()
        
    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS page_images (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    company TEXT NOT NULL,
                    year TEXT NOT NULL,
                    page INTEGER NOT NULL,
                    image_path TEXT NOT NULL,
                    dpi INTEGER,
                    width INTEGER,
                    height INTEGER,
                    UNIQUE(company, year, page)
                )
            """)
            
    def store_page(self, company: str, year: str, page: int, image_path: str):
        path_obj = Path(image_path)
        if not path_obj.exists():
            return
            
        with Image.open(image_path) as img:
            width, height = img.size
            if 'dpi' in img.info:
                dpi = img.info['dpi'][0]
            else:
                dpi = 72
            
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT OR REPLACE INTO page_images 
                (company, year, page, image_path, dpi, width, height)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (company, year, page, str(image_path), int(dpi), width, height))
            
    def get_image_path(self, company: str, year: str, page: int) -> str | None:
        with sqlite3.connect(self.db_path) as conn:
            res = conn.execute(
                "SELECT image_path FROM page_images WHERE company=? AND year=? AND page=?",
                (company, year, page)
            ).fetchone()
            return res[0] if res else None
