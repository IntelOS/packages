import pip._internal as pip
# Psutil
try:
    import psutil
except ImportError:
    pip.main(['install', 'psutil'])
    import psutil
# Pandas
try:
    import pandas as pd
except ImportError:
    pip.main(['install', 'pandas'])
    import pandas as pd
from datetime import datetime
import time
import os
def get_size(bytes):
    """
    Returns size of bytes in a nice format
    """
    for unit in ['', 'K', 'M', 'G', 'T', 'P']:
        if bytes < 1024:
            return f"{bytes:.2f}{unit}B"
        bytes /= 1024
def get_processes_info():
    # the list the contain all process dictionaries
    processes = []
    for process in psutil.process_iter():
        # get all process info in one shot
        with process.oneshot():
            # get the process id
            pid = process.pid
            if pid == 0:
                continue
            name = process.name()
            try:
                create_time = datetime.fromtimestamp(process.create_time())
            except OSError:
                create_time = datetime.fromtimestamp(psutil.boot_time())
            try:
                cores = len(process.cpu_affinity())
            except psutil.AccessDenied:
                cores = 0
            cpu_usage = process.cpu_percent()
            status = process.status()
            try:
                nice = int(process.nice())
            except psutil.AccessDenied:
                nice = 0
            try:
                memory_usage = process.memory_full_info().uss
            except psutil.AccessDenied:
                memory_usage = 0
            io_counters = process.io_counters()
            read_bytes = io_counters.read_bytes
            write_bytes = io_counters.write_bytes
            n_threads = process.num_threads()
            try:
                username = process.username()
            except psutil.AccessDenied:
                username = "N/A"   
        processes.append({
            'pid': pid, 'name': name, 'create_time': create_time,
            'cores': cores, 'cpu_usage': cpu_usage, 'status': status, 'nice': nice,
            'memory_usage': memory_usage, 'read_bytes': read_bytes, 'write_bytes': write_bytes,
            'n_threads': n_threads, 'username': username,
        })
    return processes
def construct_dataframe(processes):
    df = pd.DataFrame(processes)
    df.set_index('pid', inplace=True)
    df.sort_values(sort_by, inplace=True, ascending=not descending)
    df['memory_usage'] = df['memory_usage'].apply(get_size)
    df['write_bytes'] = df['write_bytes'].apply(get_size)
    df['read_bytes'] = df['read_bytes'].apply(get_size)
    df['create_time'] = df['create_time'].apply(datetime.strftime, args=("%Y-%m-%d %H:%M:%S",))
    df = df[columns.split(",")]
    return df
if __name__ == "__main__":
    columns = "name,cpu_usage,memory_usage,status,nice,n_threads,cores"
    sort_by = "cpu_usage"
    descending = True
    n = int(25)
    live_update = 3
    processes = get_processes_info()
    df = construct_dataframe(processes)
    if n == 0:
        print(df.to_string())
    elif n > 0:
        print(df.head(n).to_string())
    while live_update:
        try:
            processes = get_processes_info()
            df = construct_dataframe(processes)
            os.system("cls") if "nt" in os.name else os.system("clear")
            if n == 0:
                print(df.to_string())
            elif n > 0:
                print(df.head(n).to_string())
            time.sleep(0.7)
        except KeyboardInterrupt:
            os.system("cls") if "nt" in os.name else os.system("clear")
            exit(1)
