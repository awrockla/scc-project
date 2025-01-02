import csv
import os
import numpy as np
import statistics
import matplotlib.pyplot as plt

from exceptiongroup import catch

# Den aktuellen Ordner ermitteln, in dem das Skript ausgeführt wird
current_directory = os.getcwd()
read_results = []
file_counter = 0
# average and median response time
# average and median calculation time
# error percentage
# Datei: Request - Calculation
calculated_results = []

print("read files")
# Alle Dateien im aktuellen Verzeichnis auflisten
for filename in os.listdir(current_directory):
    file_path = os.path.join(current_directory, filename)

    # Prüfen, ob es sich um eine Datei handelt (keine Unterordner)
    if (os.path.isfile(file_path) and filename.endswith(('.txt', '.csv'))
            and filename.startswith('stress_test-2')):

        # Dateiinhalt lesen und in der Konsole ausgeben
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                data = [row for row in reader]  # Li
                read_results.extend(data)
        except Exception as e:
            print(f"Fehler beim Lesen der Datei {filename}: {e}")
print(f"read {file_counter} files")


print("calculate informations")
# Print the array of arrays
calculated_result = {
    "request_amount": 0,
    "average_respondtime" : 0,
    "median_respondtime" : 0,
    "average_calculation-time" : 0,
    "median_calculation-time" : 0,
    "error_percentage": 0
}
calculations = []
request_times = []
request_amount = read_results.__len__()

error_amount = 0

for row in read_results:
    request = row.get('request_time_microseconds')
    calculation = row.get('calculation_time_microseconds')

    if request == "error":
        error_amount += 1
    else:
        try:
            calculations.append(int(calculation))
            request_times.append(int(request))
        except Exception as e:
            print("Error reading respond/calculation time")
            print(e)
            print(f"request time: {request} - calculation time: {calculation}")
            print("----------------------")


average_respond = statistics.mean(request_times) / 1000
median_respond = statistics.median(request_times) / 1000
average_calculation = statistics.mean(calculations) / 1000
median_calculation = statistics.median(calculations) / 1000
error_percentage = error_amount / request_amount * 100

min_respond = min(request_times) / 1000
max_respond = max(request_times) / 1000

min_calculation = min(calculations) / 1000
max_calculation = max(calculations) / 1000

std_respond = statistics.stdev(request_times) / 1000
var_respond = statistics.variance(request_times) / 1000000

result = {
    "average_respond": average_respond,
    "median_respond": median_respond,
    "average_calculation": average_calculation,
    "median_calculation": median_calculation,
    "error_percentage": error_percentage,
    "min_respond": min_respond,
    "max_respond": max_respond,
    "min_calculation": min_calculation,
    "max_calculation": max_calculation,
    "std_respond": std_respond,
    "var_respond": var_respond
}

print(result)
plt.hist([time / 1000 for time in request_times], bins=20, edgecolor='black', range=(0, 100))
plt.title("Distribution of Respond Times")
plt.xlabel("Respond Time (ms)")
plt.ylabel("Frequency")

# Speichern der Grafik als PNG-Datei
plt.savefig('respond_times_histogram.png')

# Optional: die Grafik schließen, um Ressourcen zu schonen
plt.close()

print("Graph saved as 'respond_times_histogram.png'")
#print(read_results[:10])

