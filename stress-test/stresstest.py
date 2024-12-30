import asyncio
import aiohttp
import csv
from datetime import datetime
from typing import List

import pandas as pd

from random import randrange


async def stress_test(url, num, output, interval, duration):
    results = []
    end_time = asyncio.get_event_loop().time() + duration  # Endzeit berechnen

    while asyncio.get_event_loop().time() < end_time:
        async with aiohttp.ClientSession() as session:
            tasks = [send_request(session, url, {"sms_text": d}, results) for d in generate_input(num)]
            await asyncio.gather(*tasks)

        print(f"Batch complete. Waiting {interval} seconds...")
        await asyncio.sleep(interval)  # Wartezeit zwischen den Anfragen

    print("All requests completed.")

    # Write results to CSV

    with open(output, "w+", newline="", encoding="utf-8") as csvfile:
        print(f"writing to csv:{output_csv}")
        fieldnames = ["url", "status", "sms", "response_time", "response_time_client", "content_snippet"]

        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    for result in results:
        print(result)


async def send_request(session, url, data, results):
    start_time = datetime.now()

    try:
        async with session.post(url, json=data) as response:
            response_info = await response.text()
            print(f"response_info:{response_info}")
            classification = response_info.get("classification")
            response_time = response_info.get("response_time_in_ms")
            status = response.status

            results.append({
                    "url": url,
                    "status": status,
                    "sms": data.get("sms_text"),
                    "response_time": response_time,
                    "response_time_client": ((datetime.now() - start_time).microseconds/1000),
                    "content_snippet": classification,
                    })
    except Exception as e:
        response_time = (datetime.now() - start_time).total_seconds()
        results.append({
            "url": url,
            "status": "error in request",
            "sms": data.get("sms_text"),
            "response_time": response_time,
            "response_time_client": (datetime.now() - start_time).microseconds,
            "content_snippet": str(e),
        })


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
    interval_input = int(input("Enter the interval (default 10): ") or 10)
    duration_input = int(input("Enter the duration in seconds (default 60): ") or 60)

    # Send POST requests
    output_csv = (f"stress-test/stress_test_results-"
                  f"-Interval:{interval_input}-Duration:{duration_input}.csv")
    asyncio.run(stress_test(f"http://{target_ip}:{port}/api/classification",  num=num_requests, output=output_csv,
                            interval=interval_input, duration=duration_input))