from filinglens.downloader.registry import CompanyRegistry


def test_registry_loading():
    registry = CompanyRegistry()
    tcs = registry.get("TCS")
    assert tcs.nse_symbol == "TCS"
    assert "tcs.com" in tcs.investor_relations_url
