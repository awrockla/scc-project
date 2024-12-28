import asyncio
import aiohttp
import csv
from datetime import datetime
from typing import List

import pandas as pd

from random import randrange

async def stress_test(url, data, output):
    results = []
    async with aiohttp.ClientSession() as session:
        tasks = [send_request(session, url, {"sms_text": d}, results) for d in data]
        await asyncio.gather(*tasks)

    # Write results to CSV

    with open(output, "w+", newline="", encoding="utf-8") as csvfile:
        print(f"writing to csv:{output_csv}")
        fieldnames = ["url", "status", "sms", "response_time", "response_time_client", "content_snippet"]

        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    print(results)
async def send_request(session, url, data, results):
    start_time = datetime.now()

    try:
        async with session.post(url, json=data) as response:
            #das mit der Response Time nochmal überarbeiten
            response_info = await response.text()
            status = response.status
            content = response_info.__getitem__(0)
            response_time = response_info.__getitem__(1)
            results.append({
                "url": url,
                "status": status,
                "sms": data.get("sms_text"),
                "response_time": response_time,
                "response_time_client": (datetime.now() - start_time).microseconds,
                "content_snippet": content[:5],  # Save first 100 characters of response
            })

    except Exception as e:
        response_time = (datetime.now() - start_time).total_seconds()
        results.append({
            "url": url,
            "status": "error",
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

    # Send POST requests
    output_csv = f"stress-test/stress_test_results-{datetime.now().time()}.csv"
    asyncio.run(stress_test(f"http://{target_ip}:{port}/api/classification",  data=generate_input(num_requests), output=output_csv))