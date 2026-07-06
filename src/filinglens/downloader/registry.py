import json
from pathlib import Path
from filinglens.settings import DATA_DIR
from filinglens.downloader.models import CompanyProfile


class CompanyRegistry:
    def __init__(self, registry_path: Path = None):
        self.registry_path = registry_path or (DATA_DIR / "company_registry.json")
        self.companies = self._load()

    def _load(self) -> dict[str, CompanyProfile]:
        if not self.registry_path.exists():
            return {}
        with self.registry_path.open() as f:
            data = json.load(f)

        out = {}
        for name, config in data.items():
            out[name] = CompanyProfile(
                name=name,
                bse_code=config.get("bse"),
                nse_symbol=config.get("symbol"),
                investor_relations_url=config.get("investor_relations"),
            )
        return out

    def get(self, company_name: str) -> CompanyProfile:
        if company_name not in self.companies:
            raise ValueError(f"Company {company_name} not found in registry.")
        return self.companies[company_name]
