from filinglens.finance.normalizer import normalize_metric_name


def test_normalizer_unifies_aliases():
    assert normalize_metric_name("Net Sales") == "Revenue"
    assert normalize_metric_name("operating revenue") == "Revenue"


def test_normalizer_defaults_to_title_case():
    assert normalize_metric_name("unknown custom field") == "Unknown Custom Field"


def test_normalizer_handles_white_space():
    assert normalize_metric_name("  Profit After Tax ") == "Net Profit"
