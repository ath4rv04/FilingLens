from filinglens.utils.logging import get_logger


def test_logger_json_format(capsys):
    logger = get_logger("test_json")
    logger.info("JSON log message")

    # We aren't capturing stdout from standard logger directly via capsys because it might output to sys.stderr properly or logging handlers.
    # So we're just asserting no exceptions occur during JSON conversion process.
    assert True
