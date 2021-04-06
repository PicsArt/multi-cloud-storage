import sys
import time
import datetime
import socket
import struct
import random
import numpy as np
import uuid


class CLFLogGenerator(object):
    def __init__(self,
                 speed: int,
                 users: list,
                 request_methods: list,
                 resources: list,
                 response_types: list,
                 ip_range: tuple = (0xaaaaaaaa, 0xaaaaaaff)):
        """
        @param speed: how many requests per second should log generator produce
        @type speed: int

        @param users: List of user names alongside with their probabilities to
        appear in logs.
        E.g: [("Frank", 0.5), ("Mar", 0.4), ("Joe", 0.1)].
        Important! probabilities should sum to 1.0
        @type users: list of tuples

        @param request_methods: List of request methods alongside with their
        probabilities to appear in logs.
        E.g: [("GET", 0.8), ("POST", 0.15), ("DELETE", 0.05)].
        Important! probabilities should sum to 1.0
        @type request_methods: list of tuples

        @param resources: List of resources alongside with their probabilities
        to appear in logs.
        E.g: [("/user/{0}", 0.45), ("/pages/{0}", 0.35), ("/explore/{0}", 0.2)].
        Important! probabilities should sum to 1.0
        @type resources: list of tuples

        @param response_types: List of response types alongside with their
        probabilities to appear in logs.
        E.g: [(200, 0.85), (300, 0.1), (404, 0.04), (500, 0.01)].
        Important! probabilities should sum to 1.0
        @type response_types: list of tuples

        @param ip_range:
        @type ip_range: tuple

        """

        self.speed = speed

        self.users = [user[0] for user in users]
        self.users_prob = [user[1] for user in users]

        self.req_methods = [method[0] for method in request_methods]
        self.req_methods_prob = [method[1] for method in request_methods]

        self.resources = [res[0] for res in resources]
        self.resources_prob = [res[1] for res in resources]

        self.res_types = [res_type[0] for res_type in response_types]
        self.res_types_prob = [res_type[1] for res_type in response_types]

        self.start_ip = ip_range[0]
        self.end_ip = ip_range[1]

    def random_ipv4(self):
        """
        1. First generate random int within range start_ip - end_ip
        2. Then convert that int to binary formatted string. Formatted as
        Unsigned int with big-endian format. Because socket library and many
        other networking libraries expect big-endian formatted.
        3. Convert big-endian byte string to string IP address

        """
        rand_int_ip = random.randint(self.start_ip, self.end_ip)
        bin_packed_ip = struct.pack('>I', rand_int_ip)

        # Convert an IP address from 32-bit packed binary format to string format
        ipv4 = socket.inet_ntoa(bin_packed_ip)

        return ipv4

    def random_user(self):
        user = np.random.choice(self.users, p=self.users_prob)
        return user

    @staticmethod
    def current_time():
        dt_temp = "{0!s} {1!s}"
        date = datetime.datetime.now().strftime('%d/%b/%Y:%H:%M:%S')
        tz = time.strftime("%z", time.gmtime())
        current_datetime = dt_temp.format(date, tz)
        return current_datetime

    def random_request_method(self, ):
        request_method = np.random.choice(self.req_methods,
                                          p=self.req_methods_prob)
        return request_method

    def random_resource(self):
        resource_tmp = np.random.choice(self.resources,
                                        p=self.resources_prob)
        resource = resource_tmp.format(str(uuid.uuid4())[:8])
        return resource

    def random_response_type(self):
        response_type = np.random.choice(self.res_types,
                                         p=self.res_types_prob)
        return response_type

    def random_body_size(self):
        pass

    def get_random_clf_log(self) -> str:
        log_temp = '{0!s} - {1!s} [{2!s}] "{3!s} {4!s} HTTP/1.0" {5!s} {6!s}'

        ipv4 = self.random_ipv4()
        current_dt = self.current_time()
        user = self.random_user()
        request_method = self.random_request_method()
        resource = self.random_resource()
        response_type = self.random_response_type()

        clf_log = log_temp.format(
            ipv4,
            user,
            current_dt,
            request_method,
            resource,
            response_type,
            random.randint(1, 4098)
        )

        return clf_log

    def start(self):
        """

        """
        sleep_time = 1/self.speed
        while True:
            sys.stdout.write(self.get_random_clf_log())
            sys.stdout.write('\n')
            time.sleep(sleep_time)
