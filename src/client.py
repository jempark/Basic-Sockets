import argparse
from socket import *

# Takes in the symbol and the string of random characters.
# Checks to see how many times the symbol appears within the string.
# Returns the count in String. 
def findSymbol(symbol, random):
	count = random.count(symbol) 
	return str(count)

# Default inputs prior to user input 
hostName = ""
serverPort = 27993
sslSocket = 27994 
huskyID = 0

# Checks the argument that was given by the user
# Will give an error if improper inputs were given
parser = argparse.ArgumentParser()

parser.add_argument("-p", type = int)
parser.add_argument("-s", type = int)
parser.add_argument("[hostname]")
parser.add_argument("[NEU ID]")

# Checks to see if the user inputted any flags
# Appropriately updates default values if it does
args = parser.parse_args()
if args.p:
	serverPort = args.p

if args.s:
	sslSocket = args.s

d = vars(args)

hostName = d["[hostname]"]
huskyID = d["[NEU ID]"]

# Creates the client socket.
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((hostName, serverPort))

# Initializing the HELLO Msg and Count Msg
# Sends the first outgoing message including the inputted NUID
HELLOMSG = "cs3700spring2020 HELLO " + huskyID + "\n"
COUNTMSG = "cs3700spring2020 COUNT "
clientSocket.send(HELLOMSG)

# While the server is sending the FIND messages,
# Sends the server back the count of numbers a given character appears in a 
# list of random strings. 
# Makes sure to check if the received message ends with a new line 
# Otherwise continue to receive message and add to count until the message ends
# with a new line. 
serverExpression = True
while serverExpression:
	count = 0
	STATUS = clientSocket.recv(8192)		
	splitString = STATUS.split(" ")
	if splitString[1] == "BYE":
		serverExpression = False
		break
	elif splitString[1] == "FIND" and  "\n" in splitString[3]:
		answer = findSymbol(splitString[2], splitString[3])
		clientSocket.send((COUNTMSG + answer + "\n"))
	elif splitString[1] == "FIND":
		symbol = splitString[2]
		count += int(findSymbol(symbol, splitString[3]))
		noNewLine = True
		while noNewLine:  
			STATUS = clientSocket.recv(8192)
			if "\n" in STATUS:	
				noNewLine = False
				count += int(findSymbol(symbol, STATUS))
			else:
				count += int(findSymbol(symbol, STATUS))
		clientSocket.send((COUNTMSG + str(count) + "\n"))
	else:
		print("Unrecognized Input")

# Once the BYE message is received, breaks out of the while loop
# Close the socket and takes in secretFlag
if "\n" in splitString[2]:
	secretFlag = splitString[2]
else: 
	secretFlag = splitString[2] + "\n"

clientSocket.close()

# Creates a file that contains the secret_flag
f = open("secret_flags", "w+")
f.write(secretFlag)
f.close()
