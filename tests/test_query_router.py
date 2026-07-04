from filinglens.agents import QueryRouter


def test_query_router_routes_metric_questions_to_tables():
    route = QueryRouter().route("What was FY2024 revenue?")

    assert route.use_tables is True
    assert route.use_retrieval is False


def test_query_router_routes_disclosure_questions_to_retrieval():
    route = QueryRouter().route("Explain the management outlook on demand")

    assert route.use_retrieval is True
    assert route.use_tables is False


def test_query_router_routes_mixed_questions_to_both():
    route = QueryRouter().route("Explain why EBITDA margin changed in FY2024")

    assert route.use_retrieval is True
    assert route.use_tables is True
