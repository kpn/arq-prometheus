import pytest

METRICS_DATA = [
    {
        "completed": 0,
        "failed": 0,
        "retried": 0,
        "ongoing": 0,
        "queued": 0,
    },
    {
        "completed": 10,
        "failed": 20,
        "retried": 30,
        "ongoing": 10,
        "queued": 20,
    },
    {
        "completed": 30,
        "failed": 50,
        "retried": 0,
        "ongoing": 10,
        "queued": 230,
    },
]


@pytest.mark.parametrize("data", METRICS_DATA)
def test_generate_metrics(data, arq_prom_instance):

    arq_prom_instance.generate_metrics(data)

    assert (
        arq_prom_instance.registry.get_sample_value("arq_jobs_completed")
        == data["completed"]
    )
    assert (
        arq_prom_instance.registry.get_sample_value("arq_jobs_failed") == data["failed"]
    )
    assert (
        arq_prom_instance.registry.get_sample_value("arq_jobs_retried")
        == data["retried"]
    )
    assert (
        arq_prom_instance.registry.get_sample_value("arq_jobs_ongoing")
        == data["ongoing"]
    )
    assert (
        arq_prom_instance.registry.get_sample_value("arq_queued_inprogress")
        == data["queued"]
    )
