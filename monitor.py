import psutil
import GPUtil
import time
import argparse
import os
import csv

from threading import Thread
from datetime import datetime


class Monitor(Thread):
    def __init__(self, delay, path):
        super(Monitor, self).__init__()
        self.stopped = False
        self.delay = delay
        self.path = path
        self.start()

    def run(self):
        while not self.stopped:
            cpu_usage = psutil.cpu_percent()
            mem_usage = psutil.virtual_memory().percent
            print(f'CPU: {cpu_usage:.1f}%, RAM: {mem_usage:.1f}%')
            GPUstring = GPUtil.showUtilization()
            gpus = GPUtil.getGPUs()
            current_time = datetime.now().strftime("%H:%M-%d-%m-%Y")
            for gpu in gpus:
                with open(f"{self.path}/GPU_{gpu.id}.csv", 'a') as f:
                    csv.writer(f).writerow([current_time,gpu.load*100,gpu.memoryUtil*100])
            with open(f"{self.path}/CPU.csv", 'a') as f:
                csv.writer(f).writerow([current_time,cpu_usage,mem_usage])
            print("\n")
            time.sleep(self.delay*60) # minutes to seconds


    def stop(self):
        self.stopped = True

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-p','--period', type=float, default=7, help="Specify the period (days) to monitor the server")
    parser.add_argument('-i','--interval', type=float, default=30, help="Specify the interval (mins) to monitor the server")
    parser.add_argument('--path', type=str, default='./results', help="Specify the path to write the results")
    args = parser.parse_args()
    if not os.path.isdir(args.path):
         os.makedirs(args.path)
    gpus = GPUtil.getGPUs()
    current_time = datetime.now().strftime("%H:%M-%d-%m-%Y")
    results_dir = args.path+'/'+current_time
    os.makedirs(results_dir)
    headers = ['Time','Util','Mem']
    for gpu in gpus:
        with open(f"{results_dir}/GPU_{gpu.id}.csv", 'w') as f:
            csv.writer(f).writerow(headers)
    with open(f"{results_dir}/CPU.csv", 'w') as f:
        csv.writer(f).writerow(headers)

    monitor = Monitor(args.interval,results_dir)
    time.sleep(args.period*24*60*60) # days to seconds
    monitor.stop()