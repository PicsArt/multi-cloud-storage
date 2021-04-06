import abc
import os
import time


class LogReader:

    def __init__(self, log_path):
        self.log_path = log_path

    @abc.abstractmethod
    def next(self):
        raise NotImplementedError('Please implement next method!')


class CLFLogReader(LogReader):
    def __init__(self, log_path):
        super().__init__(log_path)

        # Open the file and move cursor the end of the file
        # Here we are imitating `tail -f` functionality.
        self.file_obj = open(log_path)
        self.file_obj.seek(0, 2)

        self.descriptor = os.fstat(self.file_obj.fileno())
        self.size = self.descriptor.st_size
        self.current_inode = self.descriptor.st_ino

    def watch_for_file_change(self):
        """
        As log files can be rotated that can potentially break our file object.
        So it can happen in 2 ways.
        1. First content of the file is removed. In this case we need to update
        file object cursor to start reading from the beginning of the file.
        2. Second file might have been deleted and recreated instantly! In this
        case we need to catch that event and reopen file object. We are doing
        it by following changes of inode_id. If inode_if of file at our location
        was changed we will recreate file object from scratch.

        """

        if self.size > os.fstat(self.file_obj.fileno()).st_size:
            self.file_obj.seek(0, 0)
            self.size = os.fstat(self.file_obj.fileno()).st_size

        if os.path.exists(self.log_path) and self.current_inode != \
                os.stat(self.log_path).st_ino:
            self.file_obj = open(self.log_path)
            self.file_obj.seek(0, 0)
            self.descriptor = os.fstat(self.file_obj.fileno())
            self.size = self.descriptor.st_size
            self.current_inode = self.descriptor.st_ino

    def next(self):
        line = self.file_obj.readline()
        while line is None or line == "" or line == "\n":
            self.watch_for_file_change()
            line = self.file_obj.readline()
        self.size = os.fstat(self.file_obj.fileno()).st_size
        return line
