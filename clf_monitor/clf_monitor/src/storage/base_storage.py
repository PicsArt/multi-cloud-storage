import abc


class BaseCLFStorageEngine:
    """
    This base class is used as enforcer to make sure that implementations obey
    the interface/rules of application design.
    data schema (
            ip: str,
            user: str,
            log_time: int,
            method: str,
            resource: str,
            protocol: str,
            response_code: int,
            size: int
    )
    """
    def __init__(self):
        self.schema = {
            "ip": "str",
            "user": "str",
            "log_time": "int",
            "method": "str",
            "resource": "str",
            "protocol": "str",
            "response_code": "int",
            "size": "int"
        }

    @abc.abstractmethod
    def _insert(self, entry):
        raise NotImplementedError("_insert should be implemented!!!")

    def insert(self, entry):
        """
        Enforces insert interface and does type checks to make sure log object
        is correctly formatted.

        @param entry: json formatted log object
        @type entry: dict

        """
        if entry is None:
            raise ValueError("Entry can not be None")
        type_error = "{0} in entry should be of type {1}!"
        for key in entry.keys():
            if not isinstance(entry[key], eval(self.schema[key])):
                raise TypeError(type_error.format(key, eval(self.schema[key])))

        self._insert(entry=entry)

    @abc.abstractmethod
    def _group_by(self, fields, aggr_method, aggr_field, start_time, end_time):
        raise NotImplementedError("group_by should be implemented!!!")

    def group_by(self, fields, aggr_method, aggr_field, start_time, end_time):
        """

        @param fields: grouping fields. One or many. E.g "resource, method"
        or "resource". Each field should be valid field
        Grouping fields: ["ip", "user", "method", "resource", "response_code"]
        @type fields: str

        @param aggr_method:
        Aggregation methods: ["COUNT", "SUM", "AVG", "MIN", "MAX"]

        @type aggr_method: str
        @param aggr_field:

        Aggregation fields: ["*", "size"]
        @type aggr_field: str

        @param start_time: Start timestamp for log filter.
        @type start_time: int

        @param end_time: End timestamp for log filter.
        @type end_time: int

        @return: list of values
        @rtype: list

        """
        grouping_fields = {"ip", "user", "method", "resource", "response_code"}
        aggr_methods = {"COUNT", "SUM", "AVG", "MIN", "MAX"}
        aggr_fields = {"*", "size"}

        fields = fields.replace(" ", "")
        if fields is None or fields == "":
            raise ValueError("Incorrect grouping field value!!!"
                             "Allowed values are {}".format(grouping_fields))
        for field in fields.split(","):
            if field not in grouping_fields:
                raise ValueError("Incorrect grouping field value!!!"
                                 "Allowed values are {}".format(grouping_fields))

        if aggr_method not in aggr_methods:
            raise ValueError("Incorrect aggr_method value!!!"
                             "Allowed values are {}".format(aggr_methods))

        if aggr_field not in aggr_fields:
            raise ValueError("Incorrect aggr_field value!!!"
                             "Allowed values are {}".format(aggr_fields))

        if not isinstance(start_time, int):
            raise TypeError("start_time should be int")

        if not isinstance(end_time, int):
            raise TypeError("start_time should be int")

        result = self._group_by(fields=fields,
                                 aggr_method=aggr_method,
                                 aggr_field=aggr_field,
                                 start_time=start_time,
                                 end_time=end_time)

        return result

    @abc.abstractmethod
    def _aggregate_by(self, field, aggr_method, start_time, end_time):
        raise NotImplementedError("__aggregate_by should be implemented!!!")

    def aggregate_by(self, field, aggr_method, start_time, end_time):
        """

        @param field: aggregation filed.
        Aggregation fields: ["*", "size", "log_time"]
        @type field: str

        @param aggr_method:
        Aggregation methods: ["COUNT", "SUM", "AVG", "MIN", "MAX"]

        @param start_time: Start timestamp for log filter.
        @type start_time: int

        @param end_time: End timestamp for log filter.
        @type end_time: int

        @return: Return aggregation result. tuple within list.
        @rtype: list

        """
        aggr_fields = {"*", "size", "log_time"}
        aggr_methods = {"COUNT", "SUM", "AVG", "MIN", "MAX"}

        if field not in aggr_fields:
            raise ValueError("Incorrect field value!!!"
                             "Allowed values are {}".format(aggr_fields))

        if aggr_method not in aggr_methods:
            raise ValueError("Incorrect aggr_method value!!!"
                             "Allowed values are {}".format(aggr_methods))

        if not isinstance(start_time, int):
            raise TypeError("start_time should be int")

        if not isinstance(end_time, int):
            raise TypeError("start_time should be int")

        result = self._aggregate_by(
            field=field,
            aggr_method=aggr_method,
            start_time=start_time,
            end_time=end_time)

        return result

# st = BaseCLFStorageEngine()
#
# # st.insert({
# #             "ip": "34",
# #             "user": "asd",
# #             "log_time": 34,
# #             "method": "Asd",
# #             "resource": "sda",
# #             "protocol": "asd",
# #             "response_code": 34,
# #             "size": 34
# #         })
#
# # st.group_by("ip", "COUNT", "*", 343, 343)
#
