# Protocol
The server runs on the machine fring.ccs.neu.edu and listens for requests on a TCP socket bound to port 27993. This exercise has four types of messages: HELLO, FIND, COUNT, and BYE. Each message is an ASCII string consisting of multiple fields separated by spaces (0x20) and terminated with a line feed (0x0A, \n). The maximum length of each message is 8192 bytes. Messages are case sensitive.

The protocol works as follows. The client initiates the protocol by creating a TCP socket connection to the server. Once the socket is connected, the client sends a HELLO message to the server. The format of the HELLO message is:

`cs3700spring2020 HELLO [your NEU ID]`

In the client program you should replace [your NEU ID] with your NEU ID (including any leading zeroes). You must supply your NEU ID so the server can look up the appropriate secret flag for you. The server will reply with either a FIND message or a BYE message below. The format of the FIND message is:

`cs3700spring2020 FIND [A single ASCII symbol] [A string of random characters]`

The two variable fields contain (1) a single ASCII symbol, such as "A", "f", "4", or "%", without quotes, and (2) a string of random characters. Your program must count the number of times the given ASCII symbol appears in the random string and return this count to the server in a COUNT message. The COUNT message has the following format:

`cs3700spring2020 COUNT [the count of the given symbol in the given string]`

It is okay for the count to be zero.

The server will respond to the COUNT message with either another FIND message, or a BYE message. If the server terminates the connection, one of several things may have happened:
1. The format of the message was incorrect
2. The count your program returned was incorrect
3. Your program took too long to respond and the server closed the connection
4. (If you recieve no messages) The server was busy and couldn't handle your request

If the server sends another FIND message, your program must count the occurances of the new given symbol and return another COUNT message. The server will ask your program to count hundreds of strings; the exact number of strings is chosen at random. Eventually, the server will return a BYE message. The BYE message has the following format:

`cs3700spring2020 BYE [a 64 byte secret flag]`
	
The 64-byte string is your secret flag: write this value down, since you need to turn it in along with your code. Once your program has received the BYE message, it can close the connection to the server. If the server returns "Unknown_Husky_ID" in the place of the secret flag, that means it did not recognize the NEU ID that you supplied in the HELLO message. You may validly print out "Unknown_Husky_ID" in this case.

# The client program
The client program must execute on the command line using the following command.

`$ ./client <-p port> <-s> [hostname] [NEU ID]`
1. The -p port parameter is optional; it specifies the TCP port that the server is listening on. If this parameter is not supplied on the command line, your program must assume that the port is 27993
2. The -s flag is optional; if given, the client should use an SSL encrypted socket connection. Your client only needs to support -s if you are trying to get the extra credit point
3. The [hostname] parameter is required, and specifies the name of the server (either a DNS name or an IP address in dotted notation).
4. The [NEU ID] parameter is required. Your code must support NEU IDs that have leading zeroes (do not strip them!).

Your program must follow this command line syntax exactly, i.e. your program must be called client and it must accept these two optional and two required parameters in exactly this order. If you cannot name your program client (e.g. your program is in Java and you can only generate client.class) then you must include a script called client in your submission that accepts these parameters and then executes your actual program. Keep in mind that all of your submissions will be evaluated by grading scripts; if your program does not conform exactly to the specification then the grading scripts may fail, which will result in loss of points.

Your program should print exactly one line of output: the secret flag from the server's BYE message. If your program encounters an error, it may print an error message before terminating. Your program must not write any files to disk, especially to the secret_flags file!