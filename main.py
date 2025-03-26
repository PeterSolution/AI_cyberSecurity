import torch
import numpy as np
import pandas as pd
import psutil
import csv
import os
from datetime import datetime, timedelta
import threading

# def get_active_ips():
#     connections = psutil.net_connections(kind='inet')
#     for conn in connections:
#         if conn.raddr:  # Sprawdzamy tylko aktywne połączenia wychodzące
#             print(f"Adres lokalny: {conn.laddr.ip}:{conn.laddr.port} ↔ Adres zdalny: {conn.raddr.ip}:{conn.raddr.port}")
#
# get_active_ips()

EnemyIP=["127.0.0.1"]

def connection_check(ip):
    EndTime = datetime.now() + timedelta(minutes=10)
    flagEnd=0
    while flagEnd != 1:
        if datetime.now()>EndTime:
            flagEnd=1
    EnemyIP.remove(ip)

def get_incoming_connections():

    while True:
        connections = psutil.net_connections(kind='inet')
        ip_counter = {}

        for conn in connections:
            if conn.status == 'ESTABLISHED' and conn.raddr:

                remote_ip = conn.raddr.ip


                if remote_ip in ip_counter:
                    ip_counter[remote_ip] += 1
                else:
                    ip_counter[remote_ip] = 1

        entries_to_save = []



        for ip, count in ip_counter.items():
            if count > 50 and ip not in EnemyIP:
                entries_to_save.append((ip, count))
                EnemyIP.append(ip)
                IpDelayRaport = threading.Thread(target=connection_check,args=(ip,))
                IpDelayRaport.start()
            # print(ip_counter.items()) # < - Do sprawdzenia obecnyhch polaczen

        csv_file = 'incoming_connections.csv'

        file_exists = os.path.isfile(csv_file)

        with open(csv_file, mode='a', newline='') as file:
            writer = csv.writer(file)

            if not file_exists:
                writer.writerow(['Data', 'IP', 'Amount of requests'])

            for ip, count in entries_to_save:
                current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                writer.writerow([current_time, ip, count])



DdosCheckThread=threading.Thread(target=get_incoming_connections)
DdosCheckThread.start()















