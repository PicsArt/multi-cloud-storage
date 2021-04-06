from clf import CLFLogGenerator
import argparse

parser = argparse.ArgumentParser(__file__,
                                 description="synthetic CFL log generator ")
parser.add_argument("--speed", "-s", dest='speed',
                    required=True, type=int,
                    help="How many requests per second should be generated!")
args = parser.parse_args()


def main():

    users = [("James", 0.25), ("Marry", 0.5), ("Frank", 0.15), ("Joe", 0.1)]

    request_methods = [("GET", 0.65), ("POST", 0.15), ("PUT", 0.1),
                       ("DELETE", 0.05), ("PATCH", 0.05)]

    resources = [("/user/{0}", 0.2), ("/pages/{0}", 0.4),
                 ("/explore/{0}", 0.2),
                 ("/review/{0}", 0.1), ("/image/{0}", 0.1)]

    response_types = [(200, 0.8), (404, 0.05), (401, 0.05),
                      (500, 0.01), (402, 0.01), (301, 0.08)]

    # (aa.aa.aa.aa - aa.aa.aa.ff) - hex ranges
    # 170.170.170.170 - 170.170.170.255 - ip ranges
    ip_range = (0xaaaaaaaa, 0xaaaaaaff)

    log_generator = CLFLogGenerator(
        speed=args.speed,  # Speed
        users=users,
        request_methods=request_methods,
        resources=resources,
        response_types=response_types,
        ip_range=ip_range
    )

    log_generator.start()


if __name__ == "__main__":
    main()
