import asyncio

import pytest
import wreq
from wreq.emulation import Emulation
from wreq.exceptions import ConnectionError, ConnectionResetError, TlsError
from wreq.tls import CertStore, ExtensionType, Tls13Cipher, TlsOptions, TlsVersion


@pytest.mark.asyncio
@pytest.mark.flaky(reruns=3, reruns_delay=2)
async def test_badssl():
    client = wreq.Client(tls_verify=False)
    resp = await client.get("https://self-signed.badssl.com/")
    async with resp:
        assert resp.status.is_success()


@pytest.mark.asyncio
@pytest.mark.flaky(reruns=3, reruns_delay=2)
async def test_badssl_invalid_cert():
    url = "https://self-signed.badssl.com/"
    client = wreq.Client(tls_verify=False, tls_info=True)
    resp = await client.get(url)
    async with resp:
        assert resp.status.is_success()
        tls_info = resp.tls_info
        assert tls_info is not None

        peer_der_cert = tls_info.peer_certificate()
        assert peer_der_cert is not None

        assert type(peer_der_cert) is memoryview
        assert peer_der_cert.readonly
        assert len(peer_der_cert) > 0

        cert_store = CertStore(der_certs=[bytes(peer_der_cert)])
        assert cert_store is not None

        client = wreq.Client(tls_verify=cert_store)
        resp = await client.get(url)
        async with resp:
            assert resp.status.is_success()


@pytest.mark.asyncio
@pytest.mark.flaky(reruns=3, reruns_delay=2)
async def test_alps_new_endpoint():
    url = "https://google.com"
    client = wreq.Client(emulation=Emulation.Chrome133)
    resp = await client.get(url)
    async with resp:
        text = await resp.text()
        assert text is not None


def test_tls_options_trust_anchors_and_grease_sigalgs():
    opts = TlsOptions(grease_sigalgs_enabled=True, trust_anchors=b"")
    assert opts is not None


def test_extension_type_trust_anchors():
    opts = TlsOptions(extension_permutation=[ExtensionType.TRUST_ANCHORS])
    assert opts is not None


@pytest.mark.asyncio
async def test_local_emulation_profiles_build_clients():
    for profile in (
        Emulation.Chrome155,
        Emulation.Chrome156,
        Emulation.Chrome157,
        Emulation.Firefox152,
        Emulation.Safari26_4,
        Emulation.OkHttp5,
        Emulation.Opera131,
    ):
        async with wreq.Client(emulation=profile):
            pass


@pytest.mark.asyncio
async def test_schannel_client_hello():
    captured = asyncio.get_running_loop().create_future()

    async def read_hello(reader, writer):
        async with asyncio.timeout(5):
            try:
                header = await reader.readexactly(5)
                captured.set_result(await reader.readexactly(int.from_bytes(header[3:], "big")))
            finally:
                writer.close()
                await writer.wait_closed()

    listener = await asyncio.start_server(read_hello, "127.0.0.1", 0)
    port = listener.sockets[0].getsockname()[1]
    options = TlsOptions(
        min_tls_version=TlsVersion.TLS_1_3,
        client_hello_padding=False,
        post_handshake_auth=True,
        sigalgs_list="dsa_sha1:rsa_pss_rsae_sha256",
        tls13_cipher_list=[Tls13Cipher.AES_128_GCM_SHA256],
        extension_permutation=[
            ExtensionType.SUPPORTED_VERSIONS,
            ExtensionType.POST_HANDSHAKE_AUTH,
            ExtensionType.SIGNATURE_ALGORITHMS,
        ],
    )
    async with listener, wreq.Client(tls_options=options, no_proxy=True) as client:
        with pytest.raises((TlsError, ConnectionError, ConnectionResetError)):
            await asyncio.wait_for(client.get(f"https://127.0.0.1:{port}"), 5)
        hello = await asyncio.wait_for(captured, 5)

    def read_u16(offset):
        return int.from_bytes(hello[offset : offset + 2], "big")

    assert hello[0] == 1  # ClientHello handshake message
    offset = 4 + 2 + 32
    offset += 1 + hello[offset]
    assert hello[offset + 2 : offset + 2 + read_u16(offset)] == b"\x13\x01"
    offset += 2 + read_u16(offset)
    offset += 1 + hello[offset]
    end = offset + 2 + read_u16(offset)
    offset += 2
    extensions = {}
    while offset < end:
        extension, length = read_u16(offset), read_u16(offset + 2)
        offset += 4
        extensions[extension] = hello[offset : offset + length]
        offset += length

    assert list(extensions)[:3] == [43, 49, 13]
    assert extensions[49] == b""
    assert 21 not in extensions
    assert extensions[13][2:4] == b"\x02\x02"
