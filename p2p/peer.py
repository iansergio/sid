import socket
import threading
import os

HOST = 'localhost'
PORT = int(input("Enter this peer port (e.g. 5000, 5001): "))
FOLDER = f'files_{PORT}'

os.makedirs(FOLDER, exist_ok=True)

def server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(5)

    print(f"[SERVER] Running on {HOST}:{PORT}")

    while True:
        conn, addr = s.accept()
        print(f"[CONNECTION] {addr}")

        try:
            command = conn.recv(1024).decode().strip()

            # list
            if command == "LIST":
                files = os.listdir(FOLDER)
                mp3_files = [f for f in files if f.endswith(".mp3")]

                if mp3_files:
                    response = "\n".join(mp3_files)
                else:
                    response = "No MP3 files available"

                conn.send(response.encode())

            # get
            elif command.startswith("GET"):
                parts = command.split(" ")

                if len(parts) < 2:
                    conn.send(b"ERROR")
                    conn.close()
                    continue

                filename = parts[1]

                # basic security (prevent invalid paths)
                if "/" in filename or "\\" in filename:
                    conn.send(b"ERROR")
                    conn.close()
                    continue

                filepath = os.path.abspath(os.path.join(FOLDER, filename))

                if os.path.exists(filepath) and os.path.isfile(filepath):
                    conn.send(b"OK")

                    with open(filepath, "rb") as f:
                        while True:
                            data = f.read(1024)
                            if not data:
                                break
                            conn.sendall(data)

                    print(f"[SEND] {filename}")

                else:
                    conn.send(b"ERROR")

        except Exception as e:
            print(f"[SERVER ERROR] {e}")

        finally:
            conn.close()

def client():
    while True:
        cmd = input("\nCommands: list / get <file.mp3> / exit\n> ").strip()

        if cmd == "exit":
            break

        try:
            target_port = int(input("Enter target peer port: "))

            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((HOST, target_port))

            # list
            if cmd == "list":
                s.send(b"LIST")
                data = s.recv(4096).decode()

                print("\nAvailable files:")
                print(data)

            # get
            elif cmd.startswith("get"):
                parts = cmd.split(" ")

                if len(parts) < 2:
                    print("Usage: get <file.mp3>")
                    s.close()
                    continue

                filename = parts[1]

                s.send(cmd.encode())

                status = s.recv(1024)

                if status == b"OK":
                    filepath = os.path.join(FOLDER, filename)

                    with open(filepath, "wb") as f:
                        while True:
                            data = s.recv(1024)
                            if not data:
                                break
                            f.write(data)

                    print(f"[DOWNLOAD COMPLETE] {filename}")

                else:
                    print("[ERROR] File not found")

            else:
                print("Invalid command")

            s.close()

        except Exception as e:
            print(f"[CLIENT ERROR] {e}")

# main
threading.Thread(target=server, daemon=True).start()
client()