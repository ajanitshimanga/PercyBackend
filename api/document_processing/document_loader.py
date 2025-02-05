from pathlib import Path
from typing import Optional

class DocumentLoader:
    def __init__(self, base_dir: str = "data"):
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(exist_ok=True)
    
    def load_local(self, filename: str) -> str:
        """Load document from local file"""
        file_path = self.base_dir / filename
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        return file_path.read_text() 