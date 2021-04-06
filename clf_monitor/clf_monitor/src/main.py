from fs.log_reader import CLFLogReader
from controller.clf_monitor import MonitorController
from log_aggregators.summary_stats_generator import SummaryStatGenerator
from log_aggregators.traffic_speed_alert import TrafficSpeedAlert
from storage.sqlite_store import SLFSQLiteStore

import argparse

parser = argparse.ArgumentParser(__file__,
                                 description="synthetic CFL log generator ")
parser.add_argument("--log_path", "-lp", dest='log_path',
                    default="/tmp/access.log", required=False, type=str,
                    help="Log file path!")

parser.add_argument("--summary_interval", "-si", dest='summary_interval',
                    default=10, required=False, type=int,
                    help="Time interval in second to calculate summary on!")

parser.add_argument("--traffic_alert_interval", "-ti", dest='traffic_interval',
                    default=20, required=False, type=int,
                    help="Time interval in second to calculate avg "
                         "traffic speed!")

parser.add_argument("--traffic_speed_threshold", "-tst", dest='speed_threshold',
                    default=10, required=False, type=int,
                    help="Speed threshold for traffic alert in rpc.!")

args = parser.parse_args()


def main():
    # Create instance of monitoring controller.
    monitor_controller = MonitorController()

    # Create instance of Storage. TTL should be max interval value of your
    # monitors and alerts
    in_memory_log_store = SLFSQLiteStore(":memory:", ttl=120)

    # Create log reader instance
    log_reader = CLFLogReader(args.log_path)

    # Summary metric generator
    summary_generator = SummaryStatGenerator(name="10s stats",
                                             interval=args.summary_interval,
                                             period=args.summary_interval,
                                             store=in_memory_log_store)
    # Traffic speed alerter
    traffic_alert = TrafficSpeedAlert(name="2 Min avg. speed",
                                      interval=args.traffic_interval,
                                      period=5,
                                      speed_threshold=args.speed_threshold,
                                      store=in_memory_log_store)

    # Set log reader
    monitor_controller.set_log_reader(log_reader)

    # Set log storage and aggregation engine.
    monitor_controller.set_log_store(in_memory_log_store)

    # Set traffic stat generators and alerts. You can add as much as you want!
    monitor_controller.add_log_processor(log_processor=summary_generator)
    monitor_controller.add_log_processor(log_processor=traffic_alert)

    # start monitoring
    monitor_controller.start()


if __name__ == "__main__":
    main()
