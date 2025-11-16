import socket
import threading
import os


class PhonebookServer:
    def __init__(self, host='127.0.0.1', port=6000):
        self.host = host
        self.port = port
        self.phonebook = {}
        self.filename = "PhonebookList.txt"
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.load_from_file()

    def load_from_file(self):
        try:
            if os.path.exists(self.filename):
                with open(self.filename, 'r', encoding='utf-8') as file:
                    for line in file:
                        line = line.strip()
                        if line and '|' in line:
                            parts = line.split('|')
                            if len(parts) == 2:
                                name = parts[0].strip()
                                phone = parts[1].strip()
                                self.phonebook[name] = phone
                print(f"📂 Loaded {len(self.phonebook)} contacts from {self.filename}")
            else:
                print(f"📂 No existing file found. Starting with empty phonebook.")
        except Exception as e:
            print(f"❌ Error loading file: {e}")

    def save_to_file(self):
        try:
            with open(self.filename, 'w', encoding='utf-8') as file:
                for name, phone in self.phonebook.items():
                    file.write(f"{name}|{phone}\n")
            print(f"💾 Saved {len(self.phonebook)} contacts to {self.filename}")
        except Exception as e:
            print(f"❌ Error saving file: {e}")

    def start(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"📞 Phonebook Server listening on {self.host}:{self.port}")
        print(f"Waiting for connection (Please Run Client)")

        while True:
            try:
                client_socket, client_address = self.server_socket.accept()
                print(f"🔌 Client connected: {client_address}")
                print(f"✅ Go on Client: {client_address}")

                thread = threading.Thread(
                    target=self.handle_client,
                    args=(client_socket,)
                )
                thread.daemon = True
                thread.start()
            except KeyboardInterrupt:
                print("\n🛑 Server shutting down...")
                break
            except Exception as e:
                print(f"❌ Server error: {e}")

    def handle_client(self, client_socket):
        try:
            while True:
                data = client_socket.recv(1024)

                if not data:
                    break

                request = data.decode('utf-8').strip()
                print(f"📨 Received: {request}")

                response = self.process_request(request)
                print(f"📤 Sending: {response}")

                client_socket.send(response.encode('utf-8'))

        except ConnectionResetError:
            print("⚠️  Client disconnected unexpectedly")
        except Exception as e:
            print(f"❌ Error handling client: {e}")
        finally:
            client_socket.close()
            print("🔌 Client connection closed")

    def process_request(self, request):
        """עיבוד הבקשה והחזרת תשובה"""
        try:
            parts = request.strip().split('|')

            if len(parts) == 0:
                return "ERROR: Empty command"

            command = parts[0].upper()

            if command == "ADD":
                if len(parts) == 4:
                    name = parts[1].strip()
                    lastname = parts[2].strip()
                    phone = parts[3].strip()

                    if not name or not lastname or not phone:
                        return "ERROR: Name, lastname and phone cannot be empty"

                    full_name = name + " " + lastname
                    self.phonebook[full_name] = phone
                    self.save_to_file()

                    return f"✅ Added: {full_name} -> {phone}"
                else:
                    return "ERROR: Format should be ADD|Name|Lastname|Phone"

            elif command == "GET":
                if len(parts) == 3:
                    name = parts[1].strip()
                    lastname = parts[2].strip()
                    full_name = name + " " + lastname
                    phone = self.phonebook.get(full_name)

                    if phone:
                        return f"{phone}"
                    else:
                        return "NOT_FOUND"
                else:
                    return "ERROR: Format should be GET|Name|Lastname"

            elif command == "UPDATE":
                if len(parts) == 4:
                    name = parts[1].strip()
                    lastname = parts[2].strip()
                    new_phone = parts[3].strip()

                    if not name or not lastname or not new_phone:
                        return "ERROR: Name, lastname and phone cannot be empty"

                    full_name = name + " " + lastname

                    if full_name in self.phonebook:
                        old_phone = self.phonebook[full_name]
                        self.phonebook[full_name] = new_phone
                        self.save_to_file()
                        return f"🔄 Updated: {full_name} | Old: {old_phone} -> New: {new_phone}"
                    else:
                        return "NOT_FOUND"
                else:
                    return "ERROR: Format should be UPDATE|Name|Lastname|NewPhone"

            elif command == "REMOVE":
                if len(parts) == 3:
                    name = parts[1].strip()
                    lastname = parts[2].strip()
                    full_name = name + " " + lastname

                    if full_name in self.phonebook:
                        phone = self.phonebook[full_name]
                        del self.phonebook[full_name]
                        self.save_to_file()

                        return f"🗑️ Deleted: {full_name} ({phone})"
                    else:
                        return "NOT_FOUND"
                else:
                    return "ERROR: Format should be REMOVE|Name|Lastname"

            elif command == "LIST":
                if len(self.phonebook) == 0:
                    return "EMPTY"
                else:
                    result = []
                    for name, phone in self.phonebook.items():
                        result.append(f"{name}: {phone}")
                    return "\n".join(result)

            else:
                return f"ERROR: Unknown command '{command}'. Use ADD, GET, DELETE, UPDATE, or LIST"

        except Exception as e:
            return f"ERROR: {str(e)}"


if __name__ == "__main__":
    server = PhonebookServer()
    try:
        server.start()
    except KeyboardInterrupt:
        print("\n👋 Server stopped")