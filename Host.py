# Host.py
# Created by Trevor Reynen, Jason Loesch, Garrett Roach

# Import Modules
import socket       							# Provides access to BSD socket interface. | https://docs.python.org/3/library/socket.html
import collections								# Implements specialized container datatypes. | https://docs.python.org/3/library/collections.html
from matplotlib.animation import FuncAnimation	# Allows making live animations. | https://matplotlib.org/stable/api/animation_api.html
import matplotlib.pyplot as plt					# Allows creating plots/graphs. | https://matplotlib.org/stable/api/pyplot_summary.html
import numpy as np								# Scientific computing module for Python. | https://numpy.org/doc/stable/user/whatisnumpy.html


CPU_USAGE = collections.deque(np.zeros(10))
MEM_USAGE = collections.deque(np.zeros(10))
GPU_TEMP = collections.deque(np.zeros(10))
indexes = [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]


def Update(i):
	# Get Data.
	CPU_USAGE_DATA, MEM_USAGE_DATA, GPU_TEMP_DATA = clientSocket.recv(1024).decode('utf-8').split(' ')

	CPU_USAGE.popleft()
	CPU_USAGE.append(float(CPU_USAGE_DATA))

	MEM_USAGE.popleft()
	MEM_USAGE.append(float(MEM_USAGE_DATA))

	GPU_TEMP.popleft()
	GPU_TEMP.append(float(GPU_TEMP_DATA))


	# Clear Axis.
	axs['ax0'].cla()
	axs['ax1'].cla()
	axs['ax2'].cla()


	# Plot CPU Usage.
	#axs['ax0'].plot(indexes, CPU_USAGE)	# Keep if want to remove colors by %.
	#axs['ax0'].scatter(0, CPU_USAGE[-1])	# Keep if want to remove colors by %.

	if CPU_USAGE[-1] >= 0.0 and CPU_USAGE[-1] < 70.0:
		axs['ax0'].plot(indexes, CPU_USAGE, color='#0b0')
		axs['ax0'].scatter(0, CPU_USAGE[-1], color='#0b0')
	elif CPU_USAGE[-1] >= 70.0 and CPU_USAGE[-1] < 90.0:
		axs['ax0'].plot(indexes, CPU_USAGE, color='#fb0')
		axs['ax0'].scatter(0, CPU_USAGE[-1], color='#fb0')
	elif CPU_USAGE[-1] >= 90.0 and CPU_USAGE[-1] <= 100.0:
		axs['ax0'].plot(indexes, CPU_USAGE, color='#f00')
		axs['ax0'].scatter(0, CPU_USAGE[-1], color='#f00')

	axs['ax0'].text(x=2, y=CPU_USAGE[-1] + 3, s='{}%'.format(CPU_USAGE[-1]), fontweight='bold')
	axs['ax0'].invert_xaxis()
	axs['ax0'].set(title='CPU Usage (%)', xlabel='Time', ylim=(0, 100))


	# Plot RAM/Memory Usage.

	#axs['ax1'].plot(indexes, MEM_USAGE)	# Keep if want to remove colors by %.
	#axs['ax1'].scatter(0, MEM_USAGE[-1])	# Keep if want to remove colors by %.

	if MEM_USAGE[-1] >= 0.0 and MEM_USAGE[-1] < 70.0:
		axs['ax1'].plot(indexes, MEM_USAGE, color='#0b0')
		axs['ax1'].scatter(0, MEM_USAGE[-1], color='#0b0')
	elif MEM_USAGE[-1] >= 70.0 and MEM_USAGE[-1] < 90.0:
		axs['ax1'].plot(indexes, MEM_USAGE, color='#fb0')
		axs['ax1'].scatter(0, MEM_USAGE[-1], color='#fb0')
	elif MEM_USAGE[-1] >= 90.0 and MEM_USAGE[-1] <= 100.0:
		axs['ax1'].plot(indexes, MEM_USAGE, color='#f00')
		axs['ax1'].scatter(0, MEM_USAGE[-1], color='#f00')

	axs['ax1'].text(x=2.5, y=MEM_USAGE[-1] + 3, s='{}%'.format(MEM_USAGE[-1]), fontweight='bold')
	axs['ax1'].invert_xaxis()
	axs['ax1'].set(title='Memory Usage (%)', xlabel='Time', ylim=(0, 100))


	# Plot GPU Temp.
	#axs['ax2'].plot(indexes, GPU_TEMP)	# Keep if want to remove colors by %.
	#axs['ax2'].scatter(0, GPU_TEMP[-1])	# Keep if want to remove colors by %.

	if GPU_TEMP[-1] >= 0.0 and GPU_TEMP[-1] < 70.0:
		axs['ax2'].plot(indexes, GPU_TEMP, color='#0b0')
		axs['ax2'].scatter(0, GPU_TEMP[-1], color='#0b0')
	elif GPU_TEMP[-1] >= 70.0 and GPU_TEMP[-1] < 90.0:
		axs['ax2'].plot(indexes, GPU_TEMP, color='#fb0')
		axs['ax2'].scatter(0, GPU_TEMP[-1], color='#fb0')
	elif GPU_TEMP[-1] >= 90.0 and GPU_TEMP[-1] <= 100.0:
		axs['ax2'].plot(indexes, GPU_TEMP, color='#f00')
		axs['ax2'].scatter(0, GPU_TEMP[-1], color='#f00')

	axs['ax2'].text(x=2.5, y=GPU_TEMP[-1] + 3, s='{}°C'.format(GPU_TEMP[-1]), fontweight='bold')
	axs['ax2'].invert_xaxis()
	axs['ax2'].set(title='GPU Temp (C)', xlabel='Time', ylim=(0, 100))

	#try to fix stalling
	msg = "continue"
	clientSocket.sendall(msg.encode('utf-8'))


# Create a socket object for the Host.
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Get and print the IP Address of local machine.
hostIPName = socket.gethostname()
hostIPAddr = socket.gethostbyname(hostIPName + '.local')
print('Current IP Address of Host:', hostIPAddr)

# Set port to connect to.
port = 25565

#set timeout to 10 seconds
serverSocket.settimeout(10)

# Bind to the port.
serverSocket.bind((hostIPAddr, port))

# Queue up to 2 connection requests.
serverSocket.listen(2)
print('Waiting for a connection...')

# Establish a connection.
clientSocket, addr = serverSocket.accept()

# Print the connected machine IP Address.
print('Got a connection from %s' % str(addr))

fig, axs = plt.subplot_mosaic([['ax0', 'ax1', 'ax2']], constrained_layout=True)
fig.canvas.manager.full_screen_toggle()    # Toggles fullscreen but then you can't easily and safely close window.

#
ani = FuncAnimation(fig, Update, frames=8, interval=250)
plt.show()


clientSocket.close()
