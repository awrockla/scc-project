import csv
from typing import List

import pandas as pd
import requests
from random import randrange

def send_requests(ip, port, data=None):
    print("Sending requests")
    url = f"http://{ip}:{port}/api/classification"

    for data in data:
        request_data = {"sms_text": data}
        response = requests.post(url, json=request_data)
        print("Sms response")
        print(response.content)


def generate_input(requests: int) -> List[str]:
    inputs = []

    sms_array = pd.read_csv('ML/spam.csv', encoding='latin1')["v2"]

    for i in range(requests):
        sms = sms_array[randrange(sms_array.__len__())]
        inputs.append(sms)

    return inputs

if __name__ == "__main__":
    # User inputs
    target_ip = input("Enter the target IP address (or default 127.0.0.1): ") or "127.0.0.1"
    port = input("Enter the port (default 5000): ") or 5000
    num_requests = int(input("Enter the number of requests to send (default 1): ") or 1)

    # Send POST requests
    send_requests(target_ip, port=port,  data=generate_input(num_requests))