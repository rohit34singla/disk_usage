I am a DevOps engineer tasked with monitoring disk usage across multiple servers. I need a Python script that fulfills the following requirements:

1. SSH Connection: The script should connect to each server using SSH and retrieve disk usage information.

2. Disk Usage Data: For each server, it should record the total space, used space, and free space available on the disk.

3. Usage Percentage Calculation: The script must calculate the disk usage percentage for each server, rounding the result to one decimal place.

4. Reporting: It should generate a report listing only those servers with a disk usage percentage exceeding 80%, sorted in descending order by usage percentage.

5. Error Logging: The script must log any errors encountered while retrieving disk usage information from a server.
