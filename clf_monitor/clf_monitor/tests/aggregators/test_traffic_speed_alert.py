from storage.sqlite_store import SLFSQLiteStore
from log_aggregators.traffic_speed_alert import TrafficSpeedAlert
from tools import populate_store


def test_alert():
    # Test data
    alert_up_now = 1598182288
    truth_alert_message = "High traffic generated an alert - hits = 1.1, " \
                          "triggered at 2020-08-23 11:31:28"

    truth_stable_message = None

    alert_recovered_time = 1598182298
    truth_recovery_message = "Recovered from Traffic Alert  - his = 0.4 " \
                             "recovered at 2020-08-23 11:31:38"

    # Start test
    storage_engine = SLFSQLiteStore(":memory:", ttl=10, test=True)
    populate_store(data_path="./aggregators/test_data.json",
                   store=storage_engine)

    traffic_alert = TrafficSpeedAlert(name="2 Min avg. speed",
                                      interval=10,
                                      period=5,  # don't need for test
                                      speed_threshold=1,
                                      store=storage_engine)

    alert_message = traffic_alert._aggregate(alert_up_now)
    stable_message = traffic_alert._aggregate(alert_up_now + 1)
    recovered_message = traffic_alert._aggregate(alert_recovered_time)

    assert alert_message == truth_alert_message and \
           stable_message == truth_stable_message and \
           recovered_message == truth_recovery_message
