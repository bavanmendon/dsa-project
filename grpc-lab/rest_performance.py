import requests
import time

URL = "http://localhost:5000/items/3"
n = 10000


start_time = time.time()

for i in range(n):
    start = time.time()
    response = requests.get(URL)
    end = time.time()
    
    if response.status_code == 200:
        print(f"Time per request: {end - start}")
    else:
        print(f"Request failed with status {response.status_code}")

end_time = time.time()

total_time =  end_time - start_time
average_time = total_time / n
    
    
print(f"Total time for {n} requests: {total_time:.4f} seconds")
print(f"Average time per request: {average_time:.4f} seconds")