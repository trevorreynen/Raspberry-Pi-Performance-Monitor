# Client.py
# Created by Trevor Reynen, Jason Loesch, Garrett Roach

# cd Documents/GitHub/Raspberry-Pi-Performance-Monitor-Project

# Import Modules.
import socket   # Provides access to BSD socket interface. | https://docs.python.org/3/library/socket.html
import GPUtil   # Gets GPU status from Nvidia GPUs. | https://pypi.org/project/GPUtil/
import psutil   # Gets process and system monitoring information. | https://pypi.org/project/psutil/
import time     # Provides time related functions. | https://docs.python.org/3/library/time.html

def main():
	# Create a socket object for the Client.
	clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	# Get and print the IP Address of local machine.
	clientIP = socket.gethostbyname(socket.gethostname())
	print('Current IP Address of Client:', clientIP)

	# Set port to connect to.
	port = 25565

	# Manually enter the IP Address to connect to.
	hostIP = input('Enter the Host\'s IP Address: ')

	# Connect to the host.
	connectedToHost = False
	while not connectedToHost:
		try:
			clientSocket.connect((hostIP, port))
		except socket.exceptions.ConnectionError as err:
			print('An error has occurred while attempting to connect to Host: %s.' % str(err))
		else:
			connectedToHosts = True
			print('Connection established.')



			while connectedToHosts:
				# CPU Usage.
				msg = str(psutil.cpu_percent())

				# RAM/Memory Usage.
				msg += ' ' + str(psutil.virtual_memory().percent)

				# GPU Temp.
				clientGPU = GPUtil.getGPUs()[0]
				msg += ' ' + str(clientGPU.temperature)

				########################################
				# IGNORE. DOES NOT WORK ON ANY OS OTHER THAN LINUX.
				# CPU Frequency.
				#current, min, max = psutil.cpu_freq()
				#msg += ' ' + str(current) + ' ' + str(min) + ' ' + str(max)
				########################################

				# Send message.
				clientSocket.sendall(msg.encode('utf-8'))

				# Uncomment below for debugging purposes.
				#print(msg)

				# Wait X seconds before repeating while loop.
				time.sleep(1.5)

	clientSocket.close()


main()
