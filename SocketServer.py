import socket
import termios, tty, sys
import threading
import pickle
from writeCSV import WriteCSV

# A thread class from https://www.tutorialspoint.com/python/python_multithreading.htm
class CSVBackgroundThread (threading.Thread):
   def __init__(self, threadID, name, counter, writer):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
        self.writer = writer
   def run(self):

        #Need to change this later to write to CSV file
        while True:
           data = conn.recv(4096)
           listOfValues = pickle.loads(data)
           print('ls:%0.3f rs:%0.3f lu:%0.3f ru:%0.3f lm:%0.3f rm:%0.3f' % (listOfValues[0], listOfValues[1], listOfValues[2], listOfValues[3], listOfValues[4], listOfValues[5]))

# ==============================================

def startNewThread(name, writer):
    # Create a new daemon thread just for taking in sensory-motor values
    thread1 = CSVBackgroundThread(1, "Thread-1", 1, writer)
    thread1.daemon = True
    thread1.start()

# ==============================================

def openCSVFile():
    writer = WriteCSV('output.csv')
    writer.openFile()
    return writer

# ==============================================

def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    tty.setcbreak(fd)
    ch = sys.stdin.read(1)
    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    return ch


# ==============================================


# Code is based on https://stackoverflow.com/questions/41294848/python-sockets-how-to-connect-between-two-computers-on-the-same-wifi
def Main():
    host = '0.0.0.0'
    port = 5000

    mySocket = socket.socket()
    mySocket.bind((host, port))

    mySocket.listen(1)
    global conn
    conn, addr = mySocket.accept() #WORK FROM HERE - NEW THREAD FOR CONN TO RECEIVE DATA FROM CLIENT



    print("Opening output.csv")
    writer = openCSVFile()
    writer.writeHeader()
    print('Starting thread')
    startNewThread('Thread-1', writer)


    #print("Exiting program")
    writer.closeFile()




    # Robot controls on main thread
    # Starting the program on server side (and client side)
    print("Connection from: " + str(addr)) #Here is where we say "Connected to the EV3DEV robot"
    while True:
        #data = conn.recv(1024).decode()
        #if not data:
        #    break
        #print("from connected  user: " + str(data))

        # data = str(data).upper()

        k = getch()

        print("sending: " + str(k))
        conn.send(k.encode())

        if k == 'q':
            break;

    conn.close()


if __name__ == '__main__':
    Main()
