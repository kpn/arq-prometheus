import pytest

TEST_CASES = [
    (
        "j_complete=0 j_failed=0 j_retried=0 j_ongoing=0 queued=0",
        {
            "completed": 0,
            "failed": 0,
            "retried": 0,
            "ongoing": 0,
            "queued": 0,
        },
    ),
    (
        "j_complete=3 j_failed=0 j_retried=0 j_ongoing=0 queued=0",
        {
            "completed": 3,
            "failed": 0,
            "retried": 0,
            "ongoing": 0,
            "queued": 0,
        },
    ),
    (
        "j_complete=3 j_failed=40 j_retried=100 j_ongoing=0 queued=0",
        {
            "completed": 3,
            "failed": 40,
            "retried": 100,
            "ongoing": 0,
            "queued": 0,
        },
    ),
    ("j_complete=3 j_failed= j_retried=100 j_ongoing=0 queued=0", None),
    ("j_complete= j_failed= j_retried= j_ongoing= queued=", None),
]


@pytest.mark.parametrize("result, parseddict", TEST_CASES)
def test_regex_results(result, parseddict, arq_prom_instance):
    assert arq_prom_instance.parse(result) == parseddict
