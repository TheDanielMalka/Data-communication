import socket


class PhonebookClient:
    def __init__(self, server_host='127.0.0.1', server_port=6000):
        self.server_address = (server_host, server_port)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        """התחברות לשרת"""
        try:
            self.socket.connect(self.server_address)
            print("✅ Connected to phonebook server")
            print("✅200 Ok!")
            return True
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            print(f"❌ Please run server first than run client")
            print(f"❌503 Service Unavailable")
            return False

    def send_command(self, command):
        try:
            self.socket.send(command.encode('utf-8'))
            response = self.socket.recv(128).decode('utf-8')
            return response
        except Exception as e:
            print(f"❌ Error: {e}")
            print(f"❌503 Service Unavailable")
            return None

    def add_contact(self, name, lastname, phone):
        """הוספת איש קשר"""
        command = f"ADD|{name}|{lastname}|{phone}"
        response = self.send_command(command)
        print(f"{response}")

    def get_contact(self, name, lastname):
        """קבלת מספר טלפון לפי שם"""
        command = f"GET|{name}|{lastname}"
        response = self.send_command(command)
        print(f"{name} {lastname} :{response}")

    def remove_contact(self, name, lastname):
        """מחיקת איש קשר"""
        command = f"REMOVE|{name}|{lastname}"
        response = self.send_command(command)
        print(f"{response}")

    def update_contact(self, name, lastname, new_phone):
        command = f"UPDATE|{name}|{lastname}|{new_phone}"
        response = self.send_command(command)
        print(f"{response}")

    def list_all(self):
        """הצגת כל אנשי הקשר"""
        command = "LIST"
        response = self.send_command(command)
        print(f"Phonebook:\n{response}")

    def interactive_mode(self):
        """מצב אינטראקטיבי"""
        print("\n📞 Phonebook Client - Interactive Mode")
        print("Commands:")
        print("  add <name> <lastname> <phone>  - Add contact")
        print("  get <name> <lastname>  - Get phone number")
        print("  remove <name> <phone> - Remove contact")
        print("  update <name> <lastname> <phone>  - Update contact")
        print("  list  - List all contacts")
        print("  quit  - Exit\n")

        while True:
            user_input = input(">>> ").strip()

            if not user_input:
                continue

            parts = user_input.split()
            command = parts[0].lower()

            if command == "quit":
                break
            elif command == "add" and len(parts) == 4:
                self.add_contact(parts[1], parts[2],parts[3])
            elif command == "get" and len(parts) == 3:
                self.get_contact(parts[1],parts[2])
            elif command == "remove" and len(parts) == 3:
                self.remove_contact(parts[1], parts[2])
            elif command == "update" and len(parts) == 4:
                self.update_contact(parts[1], parts[2], parts[3])
            elif command == "list":
                self.list_all()
            else:
                print("❌400 Bad Request")

    def close(self):
        self.socket.close()
        print("🔌 Disconnected")
        print("✅200 Ok!")



if __name__ == "__main__":
    client = PhonebookClient()

    if client.connect():
        client.interactive_mode()
        client.close()