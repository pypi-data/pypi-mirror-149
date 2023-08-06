import os
import socket
import ssl


try_ext_host = "www.google.com"


def check_internal():
    context = ssl.create_default_context()
    conn = context.wrap_socket(
        socket.socket(socket.AF_INET),
        server_hostname=try_ext_host,
    )
    try:
        conn.connect((try_ext_host, 443))
        cert = conn.getpeercert()
        conn.close()
        for crldp in cert.get("crlDistributionPoints"):
            if "Dell_SSL_Decryption" in crldp:
                return True
    except ssl.SSLError:
        return True
    return False


def check_superuser():
    try:
        return os.getuid() == 0
    except AttributeError:
        return False  # getuid does not exist on Windows


scary = ""

if check_superuser():
    scary += " and have executed it as superuser"


if check_internal():
    scary += " on a private internal network"

message = (
    "WARNING: you just installed arbitrary code from the internet{}. "
    "This is how supply chain attacks occur... Always make sure that "
    "trusted packages are fully pinned, hashed, and installed from "
    "known sources only. (Friendly advice from mfurer: 'all your base "
    "are belong to me ;P')"
).format(scary)

raise RuntimeError(message)
