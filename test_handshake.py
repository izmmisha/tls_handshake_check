import pytest
import asyncio

from scapy.layers.tls.record import TLS
from scapy.layers.tls.handshake import TLSServerHello
from scapy.layers.tls.extensions import ServerName

from ja4plus import generate_ja4
from ja4plus.utils.tls_utils import parse_tls_handshake

import secrets

def ja4(client_hello_file):
    with open(client_hello_file, "rb") as client_hello:
        raw_tls_bytes = client_hello.read()
        return generate_ja4(parse_tls_handshake(raw_tls_bytes))

from pathlib import Path
client_hello_files = [str(fn) for fn in Path('client_hello').iterdir() if fn.is_file()]
client_hello_ja4 = [ja4(fn) + '/' + fn for fn in client_hello_files]

@pytest.fixture(params=client_hello_files, ids=client_hello_ja4)
def client_hello_file(request):
    return request.param

@pytest.fixture
def orig_payload(client_hello_file):
    with open(client_hello_file, "rb") as client_hello_file:
        raw_data = client_hello_file.read()
        return raw_data

@pytest.fixture
def payload(orig_payload, fix_sni):
    tls_packet = TLS(orig_payload)
    client_hello = tls_packet.msg[0]
    for ext in client_hello.ext:
        if ext.name == "TLS Extension - Server Name":
            ext.servernames=[ServerName(servername=fix_sni)]
            ext.len = None
            ext.servernameslen = None
    tls_packet.len = None
    client_hello.msglen = None
    client_hello.extlen = None
    return bytes(tls_packet)

@pytest.fixture
def payload_factory(payload):
    tls_packet = TLS(payload)
    client_hello = tls_packet.msg[0]
    sidlen = client_hello.sidlen
    payload = list(payload)
    def _update_session():
        for i,b in enumerate(secrets.token_bytes(sidlen)):
            payload[i + 44] = b
        return bytes(payload)
    return _update_session

async def request(payload, host, port):
    reader, writer = await asyncio.open_connection(host, port)
    try:
        writer.write(payload)
        await writer.drain()
        data = await reader.read(4096)
        tls_packet = TLS(data)
        return tls_packet.haslayer(TLSServerHello)
    finally:
        writer.close()
        await writer.wait_closed()

@pytest.mark.asyncio
async def test_handshake_single(payload_factory, host, port):
    async with asyncio.timeout(10):
        response = await request(payload_factory(), host, port)
        assert response

@pytest.mark.asyncio
async def test_handshake_parallel(payload_factory, host, port):
    async with asyncio.timeout(30):
        tasks = [request(payload_factory(), host, port) for _ in range(5)]
        results = await asyncio.gather(*tasks)
        for response in results:
             assert response
