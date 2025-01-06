import csv
import os
import random
import threading
import time
import json
from datetime import datetime, timedelta

import pandas as pd
import requests
from flask import jsonify

"""Stresstest Build:
    - Inputs: Duration, Interval, Amount
    - sends async every interval, amount of requests
        - does not wait for the answers
    - after duration: wait for all results in result array
    - print results to csv
"""
results = []
sms_array = pd.read_csv('ML/spam.csv', encoding='latin1')["v2"]
lock = threading.Lock()


def run_stresstest(request_url, req_per_interval, interval_length, reps):
    """

    :param request_url: url to send requests to
    :param req_per_interval: amount of requests send to the server in one interval
    :param interval_length: length in seconds of each interval
    :param reps: how many intervals should be repeated
    :return:
    """
    for rep in range(reps):
        start_time = datetime.now()

        for i in range(req_per_interval):
            sms = sms_array[random.randint(0, len(sms_array) - 1)]
            threading.Thread(target=request_task(sms, request_url)).start()

        #wait for interval time to be full
        # Calculate remaining time in the interval
        elapsed_time = datetime.now() - start_time
        remaining_time = max(timedelta(0), interval_length - elapsed_time)
        print(f"{rep + 1}. Interval got sent. Waiting for {remaining_time} seconds...")
        # Pause for the remaining time
        time.sleep(remaining_time.total_seconds())


def request_task(sms_text, request_url):
    try:
        start_time = datetime.now()
        response=requests.post(url=request_url, json={"sms_text": sms_text})
        response_info = json.loads(response.text)
        response_time = response_info.get("response_time_in_ms")
        classification = response_info.get("classification")
        request_time = (datetime.now() - start_time).microseconds
        with lock:
            results.append(
                {"request_time_microseconds": request_time, "calculation_time_microseconds": response_time, "classification": classification}
            )

    except Exception as e:
        with lock:
            results.append(
                {"request_time_microseconds": "error", "calculation_time_microseconds": "error",
                 "classification": e}
            )


def write_result(csv_file, total_requests):
    while True:
        with lock:
            if results.__len__() == total_requests:
                break
        time.sleep(5)

    print("ALL RESULTS ARE SAVED - Write to csv")
    output_dir = os.path.dirname(output_csv)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
    with open(csv_file, "w+", newline="", encoding="utf-8") as csvfile:
        print(f"writing to csv:{output_csv}")
        fieldnames = ["request_time_microseconds", "calculation_time_microseconds", "classification"]

        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)


def dialog():
    target_ip = input("Enter the target IP address (or default 127.0.0.1): ") or "127.0.0.1"
    port = input("Enter the port (default 5000): ") or 5000
    endpoint_url: str = f"http://{target_ip}:{port}/api/classification"
    num_requests_per_intervall = int(input("Enter the number of requests to send (default 1): ") or 1)
    interval_input = int(input("Enter the interval (default 10): ") or 10)
    repetitions = int(input("Enter the repetition of intervals (default 10): ") or 10)
    total_requests = repetitions * num_requests_per_intervall
    # Send POST requests
    output_csv = (f"stress-test/v2/results/stress_test-2_results-"
                  f"Req:{num_requests_per_intervall}-Interval:{interval_input}-total:{total_requests}.csv")
    return endpoint_url, num_requests_per_intervall, interval_input, repetitions, output_csv

if __name__ == "__main__":
    url, reqs_in_interval, interval_len, repetitions, output_csv = dialog()
    run_stresstest(url, reqs_in_interval, timedelta(seconds=interval_len), repetitions)
    write_result(output_csv, repetitions*reqs_in_interval)