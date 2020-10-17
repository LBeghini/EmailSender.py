from socket import *
import ssl

# Message to send
msg = '\r\nTEST!'
endmsg = '\r\n.\r\n'

# Choose a mail server (e.g. Google mail server) and call it mailserver
mailserver = 'smtp.gmail.com'

# Create socket called clientSocket and establish a TCP connection with mailserver
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocketSLL = ssl.wrap_socket(clientSocket)

# Port number may change according to the mail server
clientSocketSLL.connect((mailserver, 465))
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


login = 'YmFzZTY0bG9naW4=\r\n'
clientSocketSLL.send(bytes(login, 'utf8'))
recv = clientSocketSLL.recv(1024)
print(recv)
if recv[:3] != bytes('334', 'utf8'):
	print('334 reply not received from server.')


password = 'YmFzZTY0cGFzc3dvcmQ=\r\n'
clientSocketSLL.send(bytes(password, 'utf8'))
recv = clientSocketSLL.recv(1024)
print(recv)
if recv[:3] != bytes('235', 'utf8'):
	print('235 reply not received from server.')

# Send MAIL FROM command and print server response.
mailfrom = 'MAIL FROM: <foo@foo.com>\r\n'
clientSocketSLL.send(bytes(mailfrom, 'utf8'))
recv = clientSocketSLL.recv(1024)
print(recv)
if recv[:3] != bytes('250', 'utf8'):
	print('250 reply not received from server.')


# Send RCPT TO command and print server response.
rcptto = 'RCPT TO: <foo@foo.com>\r\n'
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
clientSocketSLL.send(bytes('SUBJECT: TEST!\r\n', 'utf8'))
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
