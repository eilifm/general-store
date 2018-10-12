import generalstore.ntplib.ntplib as ntp
import time
from typing import List, Dict
import statistics as stats
import numpy as np
from scipy.stats import norm
import tableprint
from string import Template
from tabulate import tabulate
import math
from subprocess import Popen, PIPE


poll = True


last_compute = 0
poll_freq = 3

def weighted_avg_and_std(values, weights):
    """
    Return the weighted average and standard deviation.

    values, weights -- Numpy ndarrays with the same shape.
    """
    average = np.average(values, weights=weights[-len(values):])
    # Fast and numerically precise:
    variance = np.average((values-average)**2, weights=weights[-len(values):])
    return (average, math.sqrt(variance))



class NTPMonitor:
    def __init__(self, poll_freq, server, poll_samples, sample_retention = 20, cert = .9999):
        self._client = ntp.NTPClient()
        self.data: List[ntp.NTPStats] = []
        self.poll_freq = poll_freq
        self.last_computed_sys_time = 0
        self._server = server
        self.poll_samples = poll_samples
        self._max_samples = sample_retention
        self._cert = cert
        self._weights = (np.array(list(range(self._max_samples))) + 1)/50

        # process = Popen(['ntpdate', '-u', 'time.google.com'], stdout=PIPE, stderr=PIPE)
        # stdout, stderr = process.communicate()

        self.poll(samples = 6, init=True)

    @property
    def last(self) -> ntp.NTPStats:
        return self.data[-1]

    @property
    def mean(self) -> float:
        return weighted_avg_and_std(np.array([x.offset for x in self.data]), self._weights)[0]

    @property
    def rms_offset(self)-> float:
        return np.sqrt(np.mean(np.array([x.offset for x in self.data]) ** 2))

    @property
    def stdev(self) -> float:
        # return stats.stdev([x.offset for x in self.data])
        return weighted_avg_and_std(np.array([x.offset for x in self.data]), self._weights)[1]

    @property
    def delay_stdev(self) -> float:
        return stats.stdev([x.delay for x in self.data])

    @property
    def delay_median(self) -> float:
        return stats.median([x.delay for x in self.data])

    @property
    def range(self) -> List[float]:
        return [min([x.offset for x in self.data]), max([x.offset for x in self.data])]

    def poll(self, samples = None, init = False):

        if not samples:
            tmp = [self._client.request(self._server, version=3) for i in range(self.poll_samples)]

        else:
            tmp = [self._client.request(self._server, version=3) for i in range(samples)]

        for r in tmp:
            self.data.append(r)

        self.last_computed_sys_time = self.data[-1].recv_time

        if not init:
            # Restrict data to last n samples
            if len(self.data) > self._max_samples:
                self.data = self.data[-self._max_samples:]

            s = self.delay_stdev
            mean = self.delay_median

            # NTP Delay Range Filter
            self.data = list(filter(lambda x: True if x.delay <= (mean+(s*2)) else False, self.data))

            # print(len(self.data))

    def NTPStatsToDict(self, ntp_struct: ntp.NTPStats):
        return {'offset': ntp_struct.offset,
                'orig_time': ntp_struct.orig_time,
                'delay': ntp_struct.delay,
                'sys_tx_time': ntp_struct.tx_time,
                'sys_rx_time': ntp_struct.recv_time,
                'sys_orig_time': ntp_struct.orig_time,
                'sys_ref_time': ntp_struct.ref_time,
                'poll': ntp_struct.poll,
                'precision': ntp_struct.precision,
                'ref_id': ntp_struct.ref_id,
                'stratum': ntp_struct.stratum
                }

    def status_dict(self) -> Dict:
        return self.NTPStatsToDict(self.data[-1])

    def status(self) -> ntp.NTPStats:
        return self.data[-1]

    # def tt_now(self):
    #     self.poll(1)
    #     # return time.time() + self.status().root_dispersion

    def tt_interval(self):
        now = time.time()
        me = norm.ppf(self._cert, loc=abs(self.mean), scale=self.stdev)
        return [(now-me), (now+me), now, me*2]


samples = NTPMonitor(1, 'time.google.com', 3, 50, .9999999)


width = 22
print(tableprint.header(['Last Offset (us)', 'Last Delay', 'Mean Offset (us)', 'RMS Offset', 'Offset St. Dev. (us)', 'Interval Width (us)'], style='clean', width=width))

print(tableprint.row([samples.last.offset*1e+6, samples.status().delay, samples.mean*1e+6, samples.rms_offset*1e6, samples.stdev*1e+6, samples.tt_interval()[3]*1e6], width=width, style='clean'))

last_tti = None
while True:
    now = time.time()
    if now > samples.last_computed_sys_time + samples.poll_freq:
        samples.poll()
        print(tableprint.row([samples.last.offset * 1e+6, samples.status().delay, samples.mean * 1e+6, samples.rms_offset*1e6, samples.stdev * 1e+6, samples.tt_interval()[3]*1e6], width=width, style='clean'))

    tti = samples.tt_interval()
    # print(tti)
    # print(abs(tti[1]-tti[2]))

    if not last_tti:
        last_tti = tti
        time.sleep((tti[1] - tti[2]))
        continue
    else:
        if tti[2] < last_tti[1]:
            print("Time Violation")
            print(last_tti)
            print(tti)
            break
        last_tti = tti

    time.sleep((tti[1] - tti[2]))



        # print(strng.format(samples.last.offset*1e+6, samples.mean*1e+6, samples.stdev*1e+6))
        # print(samples.mean)
        # print(samples.tt_interval())
        # print(samples.last.offset)
        # print()

