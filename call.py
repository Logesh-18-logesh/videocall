from vidstream_modified import CameraClient, StreamingServer, AudioReceiver, AudioSender
import threading, time, cv2, struct, pickle
from urllib.request import urlretrieve
import socket

# Get the hostname of the machine
hostname = socket.gethostname()

# Get the IP address associated with the hostname
ip_address = socket.gethostbyname(hostname)

print("Your Computer Name is:", hostname)
print("Your Computer IP Address is:", ip_address)
class CallServer(StreamingServer):
    def __init__(self, host, port, slots=8, quit_key='q'):
        super().__init__(host, port, slots, quit_key)

    def _handle_client(self, connection, address):
        """ Overridden method to handle incoming client connections. """
        print(f"Incoming connection from {address}. Accept? (y/n)")

        user_input = input()  # Wait for user input to accept or reject the call

        if user_input.lower() != 'y':
            print("Connection rejected.")
            connection.close()
            return

        print("Connection accepted.")
        self._used_slots += 1  # Increment used slots only if accepted

        payload_size = struct.calcsize('>L')
        data = b""
        
        while self._running:
            break_loop = False
            
            while len(data) < payload_size:
                received = connection.recv(4096)
                if received == b'':  # Client disconnected
                    connection.close()
                    self._used_slots -= 1
                    break_loop = True
                    break
                data += received
            
            if break_loop:
                break
            
            packed_msg_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack(">L", packed_msg_size)[0]
            
            while len(data) < msg_size:
                data += connection.recv(4096)
            
            frame_data = data[:msg_size]
            data = data[msg_size:]
            frame = pickle.loads(frame_data, fix_imports=True, encoding="bytes")
            frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
            cv2.imshow(str(address), frame)
            
            if cv2.waitKey(1) == ord(self._quit_key):
                connection.close()
                self._used_slots -= 1
                break


sender=""  #ENTER THE SENDER IP (THE OTHER DEVICE)
receiver=ip_address
url1="https://images.unsplash.com/photo-1475139441338-693e7dbe20b6?auto=format&fit=crop&w=640&q=427"
url2="https://images.unsplash.com/photo-1617713964959-d9a36bbc7b52?fm=jpg&q=60&w=3000&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxleHBsb3JlLWZlZWR8MTB8fHxlbnwwfHx8fHw%3D"
url3="https://images.unsplash.com/photo-1601370690183-1c7796ecec61?fm=jpg&q=60&w=3000&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NHx8Z3JlZW58ZW58MHx8MHx8fDA%3D"
# Initialize server and client
r = CallServer(receiver, 9999)
n = int(input("Enter background type: \n1 stars\n2 white \n3 green\n4 blur\n5 default\n"))

if n == 1:
    urlretrieve(url1, "backgroundcall.jpg")
    s = CameraClient(sender, 9999, "backgroundcall.jpg")
elif n == 2:
    urlretrieve(url2, "backgroundcall.jpg")
    s = CameraClient(sender, 9999, "backgroundcall.jpg")
elif n == 3:
    urlretrieve(url3, "backgroundcall.jpg")
    s = CameraClient(sender, 9999, "backgroundcall.jpg")
elif n == 4:
    s = CameraClient(sender, 9999, "blur")
else:
    s = CameraClient(sender, 9999, "no")

ar = AudioReceiver(receiver, 9998)
a = AudioSender(sender, 9998)

# Start server thread
t1 = threading.Thread(target=r.start_server)
t1.start()
t3 = threading.Thread(target=ar.start_server)
t3.start()

# Allow time for server to start
time.sleep(2)

# Start client stream thread
t2 = threading.Thread(target=s.start_stream)
t2.start()
t4 = threading.Thread(target=a.start_stream)
t4.start()

# Wait for user input to stop the stream
while input("").lower() != "stop":
    continue

# Stop streaming and server when done
r.stop_server()
s.stop_stream()
ar.stop_server()
a.stop_stream()
