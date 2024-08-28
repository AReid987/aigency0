import requests
import time
import statistics


import requests
import time
import statistics


def benchmark_llama_cpp(prompt, num_runs=10):
    url = "http://localhost:8080/completion"
    data = {
        "prompt": prompt,
        "n_predict": 100
    }
    times = []
    for _ in range(num_runs):
        start_time = time.time()
        response = requests.post(url, json=data)
        end_time = time.time()
        times.append(end_time - start_time)

    avg_time = statistics.mean(times)
    std_dev = statistics.stdev(times)
    return avg_time, std_dev


prompt = "def fibonacci(n):"
avg_time, std_dev = benchmark_llama_cpp(prompt)
print(f"llama.cpp: Avg time: {avg_time:.4f}s, Std Dev: {std_dev:.4f}s")


def benchmark(url, prompt, num_runs=10):
    times = []
    for _ in range(num_runs):
        start_time = time.time()
        response = requests.post(url, json={'prompt': prompt})
        end_time = time.time()
        times.append(end_time - start_time)

    avg_time = statistics.mean(times)
    std_dev = statistics.stdev(times)

    return avg_time, std_dev


prompt = "def fibonacci(n):"
urls = [
    "http://<name-of-container-goes-here>:5001/generate",
    "http://<name-of-container-goes-here>:5002/generate",
    "http://<name-of-container-goes-here>:5003/generate"
]

for i, url in enumerate(urls):
    avg_time, std_dev = benchmark(url, prompt)
    print(
        f"Container {i+1}: Avg time: {avg_time:.4f}s, Std Dev: {std_dev:.4f}s")
