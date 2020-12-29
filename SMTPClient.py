from socket import *
import base64
import ssl


endmsg = '\r\n.\r\n'

# Choose a mail server (e.g. Google mail server) and call it mailserver
mailserver = input('Choose mail server: [type enter to use default (Google Mail Server)]')
if mailserver == '':
	mailserver = 'smtp.gmail.com'
	port = 465
else:
	port = int(input(f'Type the port number for {mailserver}: '))

# Create socket called clientSocket and establish a TCP connection with mailserver
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocketSLL = ssl.wrap_socket(clientSocket)

# Port number may change according to the mail server
clientSocketSLL.connect((mailserver, port))
recv = clientSocketSLL.recv(1024)
print(recv)
if recv[:3] != bytes('220', 'utf8'):
	print('220 reply not received from server.')

# # Send EHLO command and print server response.
heloCommand = 'EHLO smtp.gmail.com\r\n'
clientSocketSLL.send(bytes(heloCommand, 'utf8'))
recv = clientSocketSLL.recv(1024)
print(recv)
if recv[:3] != bytes('250', 'utf8'):
	print('250 reply not received from server.')


auth = 'AUTH LOGIN\r\n'
clientSocketSLL.send(bytes(auth, 'utf8'))
recv = clientSocketSLL.recv(1024)
print(recv)
if recv[:3] != bytes('334', 'utf8'):
	print('334 reply not received from server.')


login = base64.b64encode(input('Type your login:').encode('ascii'))
login += ('\r\n').encode('ascii')
clientSocketSLL.send(login)
recv = clientSocketSLL.recv(1024)
print(recv)
if recv[:3] != bytes('334', 'utf8'):
	print('334 reply not received from server.')

password = base64.b64encode(input('Type your password:').encode('ascii'))
password += ('\r\n').encode('ascii')
clientSocketSLL.send(password)
recv = clientSocketSLL.recv(1024)
print(recv)
if recv[:3] != bytes('235', 'utf8'):
	print('235 reply not received from server.')

# Send MAIL FROM command and print server response.
email = input('Type your email: ')
mailfrom = f'MAIL FROM: <{email}>\r\n'
clientSocketSLL.send(bytes(mailfrom, 'utf8'))
recv = clientSocketSLL.recv(1024)
print(recv)
if recv[:3] != bytes('250', 'utf8'):
	print('250 reply not received from server.')


# Send RCPT TO command and print server response.
rcp = input('Type your rcp: ')
rcptto = f'RCPT TO: <{rcp}>\r\n'
clientSocketSLL.send(bytes(rcptto, 'utf8'))
recv = clientSocketSLL.recv(1024)
print(recv)
if recv[:3] != bytes('250', 'utf8'):
	print('250 reply not received from server.')

# Send DATA command and print server response.
data = 'DATA\r\n'
clientSocketSLL.send(bytes(data, 'utf8'))
recv = clientSocketSLL.recv(1024)
print(recv)
if recv[:3] != bytes('354', 'utf8'):
	print('354 reply not received from server.')

# Send message data.
subject = input('Type subject: ')
msg = input('Type message: ')
clientSocketSLL.send(bytes(f'SUBJECT: {subject}\r\n', 'utf8'))
clientSocketSLL.send(bytes(msg, 'utf8'))

# Message ends with a single period.
clientSocketSLL.send(bytes(endmsg, 'utf8'))
recv = clientSocketSLL.recv(1024)
print(recv)
if recv[:3] != '250':
	print('250 reply not received from server.')

# Send QUIT command and get server response.
quitcommand = 'QUIT\r\n'
clientSocketSLL.send(bytes(quitcommand, 'utf8'))
recv = clientSocketSLL.recv(1024)
print(recv)
if recv[:3] != bytes('221', 'utf8'):
	print('221 reply not received from server.')
