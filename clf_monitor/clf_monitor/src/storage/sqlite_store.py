import sqlite3
import time
import threading
from storage.base_storage import BaseCLFStorageEngine


class SLFSQLiteStore(BaseCLFStorageEngine):
    def __init__(self, connection_str=":memory:", ttl=120, test=False):
        """
        @param connection_str: Connection string for Sqlite db.
        @type connection_str: str
        @param ttl: time to live in seconds, after that record will be deleted
        @type ttl: int
        """

        super().__init__()

        self.conn = sqlite3.connect(connection_str, check_same_thread=False)
        self.ttl = ttl
        self.lock = threading.Lock()

        self.cursor = self.conn.cursor()
        # Create table in in_memory sqlite db.
        create_table = '''CREATE TABLE clf_log
                       (ip text, user text, log_time long, method text, 
                       resource text,protocol text, response_code int, 
                       size int )'''

        self.cursor.execute(create_table)
        if test is False:
            threading.Thread(target=self._ttl_thread).start()

    def _insert(self, entry):
        query_temp = """INSERT INTO clf_log VALUES 
                        ('{0}','{1}',{2},'{3}','{4}', '{5}',{6},{7})"""

        query = query_temp.format(
            entry["ip"],
            entry["user"],
            entry["log_time"],
            entry["method"],
            entry["resource"],
            entry["protocol"],
            entry["response_code"],
            entry["size"]
        )
        try:
            self.lock.acquire(True)
            self.cursor.execute(query)
        finally:
            self.lock.release()

    def _group_by(self, fields, aggr_method, aggr_field, start_time, end_time):
        query_temp = """SELECT {0}, {1}({2}) as {1}_{3}
                        FROM clf_log
                        WHERE log_time BETWEEN {4} AND {5}
                        GROUP BY {0}"""
        query_str = query_temp.format(fields,
                                      aggr_method,
                                      aggr_field,
                                      aggr_field if aggr_field != "*" else "ALL",
                                      start_time,
                                      end_time)

        return self._query(query_str)

    def _aggregate_by(self, field, aggr_method, start_time, end_time):
        query_temp = """SELECT {1}({0}) from clf_log 
                        WHERE log_time BETWEEN {2} AND {3}"""
        query_str = query_temp.format(field,
                                      aggr_method,
                                      start_time,
                                      end_time)
        return self._query(query_str)

    def _ttl_thread(self):

        while True:
            time.sleep(30)
            delete_temp = """DELETE FROM clf_log WHERE log_time <= {0}"""
            delete_query = delete_temp.format(int(time.time()-self.ttl))
            try:
                self.lock.acquire(True)
                self.cursor.execute(delete_query)
            finally:
                self.lock.release()

    def _query(self, query_str):
        res = None
        with self.lock:
            res = list(self.cursor.execute(query_str))
        return res
