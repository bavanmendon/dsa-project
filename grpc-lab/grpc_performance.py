import grpc
import time
import myitems_pb2
import myitems_pb2_grpc

grpc_address = "localhost:50051"
n = 10000
item_id = 1

channel = grpc.insecure_channel(grpc_address)
stub = myitems_pb2_grpc.ItemServiceStub(channel)	

start_time = time.time()

for i in range(n):
    start = time.time()
    response = stub.GetItemById(myitems_pb2.ItemRequest(id = 1))							
    end = time.time()
    print(f"Time per request: {end - start}")

end_time = time.time()

total_time =  end_time - start_time
average_time = total_time / n
    
    
print(f"Total time for {n} requests: {total_time:.4f} seconds")
print(f"Average time per request: {average_time:.4f} seconds")