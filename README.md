# pyUpdater :: updater.exe
Script that automatically updates the Destination IP address to 255.255.255.255 of any analog Ethernet CallerID.com unit.

You can change SEND_REC_PORT if needed. 

Also, this gives some lower-level udp socket commands as example of communication between a python script and CallerID.com's Whozz Calling ethernet units.

# Important Note:
This program runs quickly, in the background. Output logs are stored in a created folder of C:\temp. One file is create for verbose logging: caller_id_log.txt, which will display complete status of previously ran script.

Another file will be create ONLY ON FAILURE: caller_id_ERROR.txt which will provide the reason for failure and also an error code.
