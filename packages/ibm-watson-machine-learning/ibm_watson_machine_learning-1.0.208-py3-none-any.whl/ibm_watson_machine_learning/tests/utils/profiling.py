#  (C) Copyright IBM Corp. 2022.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import psutil
import sys
import time
import threading
from builtins import property


class IOProfiler(object):
    '''A help class to profile process I/O using `psutil`
    '''
    def __init__(self):
        self.psthread = None
        self.psstop = False
        self.psstorage = []
        self.proc = psutil.Process()

    def start(self):
        def instr_io(proc, storage):
            while(not self.psstop):
                storage.append((time.time(), proc.io_counters()))
                time.sleep(1)

        self.psthread = threading.Thread(target=instr_io,
                                         args=(self.proc,
                                               self.psstorage))
        self.psthread.start()

    def stop(self):
        self.psstop = True
        self.psthread.join()

    @property
    def mbyte_count(self):
        t0, startpio = self.psstorage[0]
        t_last, endpio = self.psstorage[-1]
        bc = (endpio.other_bytes - startpio.other_bytes) / (1024*1024)
        return bc

    @property
    def elapsed_time(self):
        t0, startpio = self.psstorage[0]
        t_last, endpio = self.psstorage[-1]
        return t_last - t0

    @property
    def rate(self):
        return self.mbyte_count / self.elapsed_time

    def write_info(self, filelike):
        filelike.write(f"Number of bytes read: {self.mbyte_count} MB, rate={self.rate} MB/sec, elapsed={self.elapsed_time}\n")

    def print_info(self):
        self.write_info(sys.stdout)

    def save_csv(self, outputname):
        '''Writes a csv with columns `time,io_count,io_bytes`
        '''
        t0, startpio = self.psstorage[0]

        with open(outputname, mode="w") as s:
            s.write("time,io_count,io_bytes")
            for t, c in self.psstorage:
                elapsed = t-t0
                io_count = c.other_count - startpio.other_count
                io_bytes = c.other_bytes - startpio.other_bytes
                s.write(f"{elapsed},{io_count},{io_bytes}\n")
