""" 
Project Brief: Network Scanner
Project name: Python Network Scanner

Purpose: Build a Python tool that checks whether a specified device can be reached through a particular TCP port.

Overview: The Network Scanner will allow a user to enter an IP address and a port number. It will validate the IP address using Python’s ipaddress library, then use the socket library to attempt a TCP connection to that port. The program will report the result, helping the user understand basic network connectivity and port accessibility.
Core features
- IP validation: Check whether the entered IP address is valid.
- Port checking: Attempt a TCP connection to a specified port.
- Timeout handling: Prevent the program from waiting indefinitely for a response.
- Clear results: Report whether the connection succeeded or failed.
- Error handling: Handle invalid inputs and connection errors.
- Future improvements: Scan a small, user-selected list of ports, record timestamps, generate reports and add automated tests.
Technologies
- ipaddress — validates and interprets IP addresses.
- socket — attempts network connections.
- datetime — records when scans take place.
- logging — records events and errors.
Learning objectives
By completing this project, I aim to improve my understanding of IP addressing, TCP connections, ports, Python networking libraries, input validation and error handling.

Security boundary: The scanner will only be used on my own devices or systems I have explicit permission to test. A successful connection indicates that a TCP connection was accepted; it does not prove that a service is vulnerable.

Success criteria: The first version will be complete when it can validate an IP address, test one specified TCP port, handle invalid input and timeouts, and display a clear result.

"""