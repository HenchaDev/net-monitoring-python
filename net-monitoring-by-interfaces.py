# In this code the network usage is 
#monitored as per network interface

import psutil
import time
import os
import pandas as pd

UPDATE_DELAY = 1 

def get_size(bytes):
    for unit in ['', 'K', 'M', 'G', 'T', 'P']:
        if bytes < 1024:
            return f"{bytes: .2f}{unit}B"
        bytes /= 1024

io = psutil.net_io_counters(pernic=True)

while True:
    
    time.sleep(UPDATE_DELAY)
    io_2 = psutil.net_io_counters(pernic=True)
    data = []
    for iface, iface_io in io.items():
        upload_speed, download_speed = io_2[iface].bytes_sent - iface_io.bytes_sent, io_2[iface].bytes_recv - iface_io.bytes_recv

        data.append({
            "iface": iface, "Download": get_size(io_2[iface].bytes_recv),
            "Upload": get_size(io_2[iface].bytes_sent),
            "Upload Speed": f"{get_size(upload_speed / UPDATE_DELAY)}/s",
            "Download Speed": f"{get_size(download_speed  / UPDATE_DELAY)}/s"
        })
    
    io = io_2
    df = pd.DataFrame(data)
    df.sort_values("Download", inplace=True, ascending=False)
    os.system("cls") if "nt" in os.name else os.system("clear")

    print(df.to_string())