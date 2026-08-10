from src.metrics import calculate_funnel, calculate_logging_coverage, metrics_by_model_version, metrics_by_position, safe_rate


def test_metrics_and_zero_denominators(logger, store, impression):
    logger.log_click(impression.impression_id)
    logger.log_apply(impression.impression_id, "app")
    logger.log_shortlist(impression.impression_id, "app", "short")
    events = store.read_all(); funnel = calculate_funnel(events)
    assert funnel["ctr"] == funnel["apply_rate_per_click"] == funnel["shortlist_rate_per_application"] == 1.0
    assert metrics_by_position(events)["1"]["shortlists"] == 1
    assert metrics_by_model_version(events)["v1"]["clicks"] == 1
    assert calculate_logging_coverage(events)["position_coverage"] == 1.0
    assert safe_rate(1, 0) == 0.0


def test_empty_funnel_does_not_crash():
    assert calculate_funnel([])["ctr"] == 0.0
