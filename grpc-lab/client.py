import grpc
import time
import myitems_pb2
import myitems_pb2_grpc

messages = [
	myitems_pb2.ChatMessage(user = "Client", message = "Hello"),
	myitems_pb2.ChatMessage(user = "Client", message = "What's up?"),
	myitems_pb2.ChatMessage(user = "Client", message = "Bidirectional testing")
]

def run():
	channel = grpc.insecure_channel("localhost:50051")										# Connect client to port 50051 (sever is connected to the same already)
	stub = myitems_pb2_grpc.ItemServiceStub(channel)										# Use functions calls from grpc which will invoke the definition from server

	# 1. Unary call
	print("=== Unary RPC: GetItemById ===")
	response = stub.GetItemById(myitems_pb2.ItemRequest(id = 1))							# Uses pb2_grpc to get stub/function compiled from .proto and pb2 as argument for streaming
	print("Unary response:", response)

	# 2. Server-streaming
	print("\n=== Server-streaming RPC: ListAllItems ===")
	for item in stub.ListAllItems(myitems_pb2.Empty()):
		print("Server-streaming item:", item)

	# 3. Client-streaming
	# Create an iterator of ItemRequest messages
	# Then call stub.AddItems(...) and capture the final result
	print("\n=== Client-streaming RPC: AddItems ===")
	
	def send_items():
		items = [
			myitems_pb2.SendStream(name = "Name 4"),
			myitems_pb2.SendStream(name = "Name 5"),
			myitems_pb2.SendStream(name = "Name 6")
		]

		for item in items:																	# Iterator to send client stream
			print(f"Sending: {item.name}")
			yield item
			time.sleep(1)
	
	response = stub.AddItems(send_items())
	print(f"Client-streaming result: {response.total_count} items added")

	# 4. Bidirectional
	# Open a stub.ChatAboutItems() stream
	# Send ChatMessage objects and read responses in a loop
	def chat_stream():
		for content in messages:
			print(f"{content.user}:{content.message}")
			yield content
			time.sleep(1)
	responses = stub.ChatAboutItems(chat_stream())
	for response in responses:
		print(f"Server: {response.message}")

if __name__ == "__main__":
	run()
