# ----------------------------------------------
# CallerID.com (c) 2022
# sam penland - sam@callerid.com
#
# UDP application to set analog units to
# a destination IP address of 255.255.255.255
#
#    Exit Codes:
#       - 0 : Success
#       - 1 : Couldn't bind to SEND_REC_PORT
#       - 2 : Couldn't find Unit
#       - 3 : Couldn't change IP address of unit
# ----------------------------------------------

import socket
import sys
import threading
import os
from datetime import datetime
from time import sleep

SEND_REC_PORT = 3520

pc_address = ""
listening = True
x_reception = False
ok_reception = False


def parse_packet(data, address):

    if address[0] == pc_address:
        return

    packet_len = len(data)

    packet_ascii = ""
    try:
        packet_ascii = str(data, 'ISO-8859-1')
    except Exception as err:
        pass

    if packet_len == 90:

        global x_reception
        x_reception = True
        return

    if "ok" in packet_ascii:

        global ok_reception
        ok_reception = True
        return


def listen_to_udp():

    global listening
    global s

    while listening:
        try:
            data, address = s.recvfrom(1500)
            parse_packet(data, address)
        except Exception as e:
            pass


def send_udp_bytes(byte_array):

    ss = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    ss.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    ss.bind(("", 0))
    ss.sendto(byte_array, ("255.255.255.255", SEND_REC_PORT))


def send_udp(message):
    send_udp_bytes(bytes(message, "utf-8"))


def send_udp_with_bytes(message, extra_bytes):

    msg_bytes = bytes(message, "utf-8")
    full_array_of_bytes = bytearray()

    for b in msg_bytes:
        full_array_of_bytes.append(b)

    for b in extra_bytes:
        full_array_of_bytes.append(b)

    send_udp_bytes(full_array_of_bytes)


def log(text):

    f = open("C:/temp/caller_id_log.txt", "a+")
    f.write(text + "\n")

    print(text + "\n")


def write_error(text):

    f = open("C:\\temp\\caller_id_ERROR.txt", "w+")
    f.write(text + "\n")

    print(text + "\n")


def end_with_code(code):

    global listening

    global s

    listening = False
    s.close()
    listen_thread.join()
    sys.exit(code)

# --------------------------------------------------------
# Execution
# --------------------------------------------------------
try:
    os.mkdir("C:/temp")
except Exception as ex:
    pass

log('Running configuration process')
log("Binding to port...")

# Sockets / UDP Receiver
try:

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    s.bind(("0.0.0.0", SEND_REC_PORT))

    pc_address = socket.gethostbyname(socket.gethostname())

    listen_thread = threading.Thread(target=listen_to_udp, args=())
    listen_thread.start()

except Exception as ex:
    write_error("Could not bind to port: Exit 1")
    end_with_code(1)


log("-------------------------")
log(str(datetime.now()))
log("Attempting unit destination IP address update to: 255.255.255.255")
log("-------------------------")
log("Bound to port " + str(SEND_REC_PORT) + " on new thread...")
log("Checking connection...")

x_reception = False

c = 0
while not x_reception and c < 3:
    send_udp("^^IdX")
    sleep(1)
    c += 1

if x_reception:
    log("Found unit.")
    log("Changing IP to: 255.255.255.255")
else:
    write_error("Could not connect to unit: EXIT 2")
    end_with_code(2)

ok_reception = False
send_udp("^^IdDFFFFFFFF")

c = 0
while not ok_reception and c < 3:
    send_udp("^^IdX")
    sleep(1)
    c += 1

if ok_reception:
    log("Successfully changed IP address to 255.255.255.255")
    end_with_code(0)
else:
    write_error("Connected to unit but could not change IP address. EXIT 3")
    end_with_code(3)
