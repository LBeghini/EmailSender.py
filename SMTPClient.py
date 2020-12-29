from socket import *
import base64
import ssl
import os
import re

ENDMSG = '\r\n.\r\n'

ENDSTR = '\r\n'

COLOR = {
    "PURPLE": '\033[95m',
    "CYAN": '\033[96m',
    "DARKCYAN": '\033[36m',
    "BLUE": '\033[94m',
    "GREEN": '\033[92m',
    "YELLOW": '\033[93m',
    "RED": '\033[91m',
    "BOLD": '\033[1m',
    "UNDERLINE": '\033[4m',
    "END": '\033[0m'
}
print(
    "  _____ __  __ _______ _____   _____ _ _            _     \n"
    " / ____|  \/  |__   __|  __ \ / ____| (_)          | |    \n"
    "| (___ | \  / |  | |  | |__) | |    | |_  ___ _ __ | |_   \n"
    " \___ \| |\/| |  | |  |  ___/| |    | | |/ _ \ '_ \| __|  \n"
    " ____) | |  | |  | |  | |    | |____| | |  __/ | | | |_   \n"
    "|_____/|_|  |_|  |_|  |_|     \_____|_|_|\___|_| |_|\__|  \n"
)
input("PRESS ENTER TO START")
os.system('cls')

# Create socket called clientSocket and establish a TCP connection with mailServer
print(f'{COLOR["YELLOW"]}CREATING CONNECTION SOCKET...{COLOR["END"]}')
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.settimeout(1)
clientSocketSLL = ssl.wrap_socket(clientSocket)

# Choose a mail server (e.g. Google mail server) and call it mailServer
while True:
    mailServer = 'smtp.gmail.com'
    port = 465
    input_server = input(f'{COLOR["YELLOW"]}\nMAIL SERVER [press enter to use default]: {COLOR["END"]}')
    if input_server != '':
        verify = re.fullmatch(r'^(([a-zA-Z0-9\-]*)(\.)){2,}([a-zA-Z]{2,3})$', input_server)
        if verify is None:
            print(f'{COLOR["RED"]}\nERROR: INVALID MAIL SERVER{COLOR["END"]}')
            continue
        else:
            mailServer = input_server.lower()
            while True:
                input_port = input(f'{COLOR["YELLOW"]}\nPORT [press enter to use default]: {COLOR["END"]}')
                if input_port != '':
                    verify = re.fullmatch(r'^\d{3,4}$', input_port)
                    if verify is None:
                        print(f'{COLOR["RED"]}\nERROR: INVALID PORT NUMBER{COLOR["END"]}')
                        continue
                    else:
                        port = int(input_port)
                        break
                else:
                    break

    # Port number may change according to the mail server
    print(f'{COLOR["YELLOW"]}\nCONNECTING TO SERVER...{COLOR["END"]}')
    try:
        clientSocketSLL.connect((mailServer, port))
    except (TimeoutError, timeout, gaierror):
        print(f'{COLOR["RED"]}\nERROR: INVALID MAIL SERVER OR PORT{COLOR["END"]}')
        continue
    break

recv = clientSocketSLL.recv(1024)
if recv[:3] != bytes('220', 'utf8'):
    print(f'{COLOR["RED"]}\n{recv.decode("utf8")}{COLOR["END"]}')
    exit(-1)
else:
    print(f'{COLOR["GREEN"]}\n{recv.decode("utf8")}{COLOR["END"]}')

# Send EHLO command and print server response.
heloCommand = f'EHLO {mailServer}{ENDSTR}'
print(COLOR["YELLOW"] + heloCommand + COLOR["END"])
clientSocketSLL.send(bytes(heloCommand, 'utf8'))
recv = clientSocketSLL.recv(1024)
if recv[:3] != bytes('250', 'utf8'):
    print(f'{COLOR["RED"]}{recv.decode("utf8")}{COLOR["END"]}')
    exit(-1)
else:
    print(f'{COLOR["GREEN"]}{recv.decode("utf8")}{COLOR["END"]}')

while True:
    # Send AUTH LOGIN to authenticate to server
    auth = f'AUTH LOGIN{ENDSTR}'
    print(COLOR["YELLOW"] + auth + COLOR["END"])
    clientSocketSLL.send(bytes(auth, 'utf8'))
    recv = clientSocketSLL.recv(1024)
    if recv[:3] != bytes('334', 'utf8'):
        print(f'{COLOR["RED"]}{recv.decode("utf8")}{COLOR["END"]}')
        exit(-1)
    else:
        msg = recv.decode('utf8')
        print(f'{COLOR["GREEN"]}{recv.decode("utf8")[:3]} {base64.b64decode(msg[3:]).decode("ascii")}{COLOR["END"]}',
              end=' ')
    email = input()
    login = base64.b64encode(email.encode('utf8'))
    login += ENDSTR.encode('utf8')
    clientSocketSLL.send(login)
    recv = clientSocketSLL.recv(1024)
    msg = recv.decode('utf8')
    print(f'{COLOR["GREEN"]}{recv.decode("utf8")[:3]} {base64.b64decode(msg[3:]).decode("ascii")}{COLOR["END"]}',
          end=' ')

    password = base64.b64encode(input().encode('utf8'))
    password += ENDSTR.encode('utf8')
    clientSocketSLL.send(password)
    recv = clientSocketSLL.recv(1024)
    if recv[:3] != bytes('235', 'utf8'):
        print(f'{COLOR["RED"]}{recv.decode("utf8")}{COLOR["END"]}')
        if recv[:3] == bytes('535', 'utf8'):
            continue
        else:
            exit(-1)
    else:
        print(f'{COLOR["GREEN"]}{recv.decode("utf8")}{COLOR["END"]}')
        break

# Send MAIL FROM command and print server response.
print(f'{COLOR["YELLOW"]}MAIL FROM: <{email}>')
mailFrom = f'MAIL FROM: <{email}>{ENDSTR}'
print(COLOR["END"])
clientSocketSLL.send(bytes(mailFrom, 'utf8'))
recv = clientSocketSLL.recv(1024)
if recv[:3] != bytes('250', 'utf8'):
    print(f'{COLOR["RED"]}{recv.decode("utf8")}{COLOR["END"]}')
    exit(-1)
else:
    print(f'{COLOR["GREEN"]}{recv.decode("utf8")}{COLOR["END"]}')

# Send RCPT TO command and print server response.
rcp = input(f'{COLOR["YELLOW"]}RCPT TO: ')
rcptTo = f'RCPT TO: <{rcp}>{ENDSTR}'
print(COLOR["END"])
clientSocketSLL.send(bytes(rcptTo, 'utf8'))
recv = clientSocketSLL.recv(1024)
if recv[:3] != bytes('250', 'utf8'):
    print(f'{COLOR["RED"]}{recv.decode("utf8")}{COLOR["END"]}')
    exit(-1)
else:
    print(f'{COLOR["GREEN"]}{recv.decode("utf8")}{COLOR["END"]}')

# Send DATA command and print server response.
data = f'DATA{ENDSTR}'
print(f'{COLOR["YELLOW"]}{data}{COLOR["END"]}')
clientSocketSLL.send(bytes(data, 'utf8'))
recv = clientSocketSLL.recv(1024)
if recv[:3] != bytes('354', 'utf8'):
    print(f'{COLOR["RED"]}{recv.decode("utf8")}{COLOR["END"]}')
    exit(-1)
else:
    print(f'{COLOR["GREEN"]}{recv.decode("utf8")}{COLOR["END"]}')

# Send message data.
subject = input(f'{COLOR["YELLOW"]}SUBJECT: ')
clientSocketSLL.send(bytes(f'SUBJECT: {subject}{ENDSTR}', 'utf8'))
line = ''
msg = ''
print(f'{COLOR["YELLOW"]}\nMESSAGE [enter a single . to finish]: {COLOR["END"]}')
print(COLOR["CYAN"])
while True:
    line = input('\t')
    if line == '.':
        break
    msg += line + '\n'
print(COLOR["END"])
clientSocketSLL.send(bytes(msg, 'utf8'))

# Message ends with a single period.
clientSocketSLL.send(bytes(ENDMSG, 'utf8'))
recv = clientSocketSLL.recv(1024)
if recv[:3] != bytes('250', 'utf8'):
    print('here')
    print(f'{COLOR["RED"]}{recv.decode("utf8")}{COLOR["END"]}')
    exit(-1)
else:
    print(f'{COLOR["GREEN"]}{recv.decode("utf8")}{COLOR["END"]}')

# Send QUIT command and get server response.
quitCommand = f'QUIT{ENDSTR}'
print(f'{COLOR["YELLOW"]}{quitCommand}{COLOR["END"]}')
clientSocketSLL.send(bytes(quitCommand, 'utf8'))
recv = clientSocketSLL.recv(1024)
if recv[:3] != bytes('221', 'utf8'):
    print(f'{COLOR["RED"]}{recv.decode("utf8")}{COLOR["END"]}')
    exit(-1)
else:
    print(f'{COLOR["GREEN"]}{recv.decode("utf8")}{COLOR["END"]}')
