from storage.sqlite_store import SLFSQLiteStore
from log_aggregators.summary_stats_generator import *
from tools import populate_store


def test_summary_aggregation_logic():
    # Test data
    # This now, test_data, ground_truth is tightly coupled together
    # if you want to change one of those value make sure to recalculate rest.
    now = 1598182270
    ground_truth = SummaryStats()
    ground_truth.TOP_RESOURCES = [('/pages/*', 6), ('/image/*', 2),
                                  ('/explore/*', 1)]
    ground_truth.TOP_USERS = [('Marry', 6), ('Frank', 2), ('Joe', 1)]
    ground_truth.TOP_METHODS = [('GET', 5), ('POST', 2), ('PUT', 2)]
    ground_truth.TOP_RESPONSE_CODES = [(200, 9)]
    ground_truth.AVG_REQUEST_SIZE = 1592
    ground_truth.REQUEST_COUNT = 9
    ground_truth.TRAFFIC_SPEED = 0.9

    # Start test
    storage_engine = SLFSQLiteStore(":memory:", ttl=10, test=True)
    populate_store(data_path="./aggregators/test_data.json",
                   store=storage_engine)

    sum_gen = SummaryStatGenerator(name="SummaryStat",
                                   interval=10,
                                   period=10,  # don't need this for test
                                   store=storage_engine)

    response = sum_gen._aggregate(now)
    assert ground_truth == response
