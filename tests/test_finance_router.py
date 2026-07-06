from filinglens.finance.router import IntentRouter


def test_intent_router_recognizes_comparisons():
    assert IntentRouter.route("Compare Infosys and TCS margins") == "ComparisonQuery"


def test_intent_router_recognizes_explicit_metric_queries():
    assert IntentRouter.route("What was the net profit?") == "MetricQuery"
    assert IntentRouter.route("Give me the current ebitda bounds") == "MetricQuery"


def test_intent_router_recognizes_tables():
    assert IntentRouter.route("Show the table containing assets") == "TableQuery"


def test_intent_router_defaults_to_narrative_search():
    assert (
        IntentRouter.route("What factors did the board identify for growth?")
        == "NarrativeQuery"
    )
