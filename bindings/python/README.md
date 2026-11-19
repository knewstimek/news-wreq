# wreq

Python bindings adapted from [wreq-python](https://github.com/0x676e67/wreq-python).

An ergonomic and modular Python HTTP Client for high-fidelity protocol matching, featuring customizable TLS, JA3/JA4, and HTTP/2 signature capabilities, powered by [wreq](https://github.com/0x676e67/wreq).

## Features

- Async and Blocking `Client`s
- Plain bodies, JSON, urlencoded, multipart
- HTTP Trailer
- Cookie Store
- Redirect Policy
- Original Header
- Rotating Proxies
- Connection Pooling
- Streaming Transfers
- Zero-Copy Transfers
- WebSocket Upgrade
- HTTPS via BoringSSL
- Free-Threaded Safety
- Automatic Decompression
- Certificate Store (CAs & mTLS)

## Example

The following example uses the `asyncio` runtime. Build this fork's wheel
from the workspace root and install the wheel from `target/wheels`.

```bash
maturin build --locked --release --manifest-path bindings/python/Cargo.toml
```

And then the code:

```python
import asyncio
from wreq import Client, Emulation


async def main():
    async with Client(emulation=Emulation.Chrome154) as c:
        async with c.get("https://pingly.us.kg/api/all") as r:
            r.raise_for_status()
            print(await r.text())


if __name__ == "__main__":
    asyncio.run(main())
```

Additional learning resources include:

- [Examples](https://github.com/0x676e67/wreq-python/tree/main/examples)
- [DeepWiki](https://deepwiki.com/0x676e67/wreq-python)
- [Documentation](https://python.wreq.org)

## Behavior

1. **HTTP/2 over TLS**

Due to the complexity of TLS encryption and the widespread adoption of HTTP/2, browser fingerprints such as **JA3**, **JA4**, and **Akamai** cannot be reliably emulated using simple fingerprint strings. Instead of parsing and emulating these string-based fingerprints, `wreq` provides fine-grained control over TLS and HTTP/2 extensions and settings for precise browser behavior emulation.

2. **Device Emulation**

**TLS** and **HTTP/2** fingerprints are often identical across various browser models because these underlying protocols evolve slower than browser release cycles. **100+ browser device emulation [profiles](https://python.wreq.org/en/latest/api/emulation/#wreq.emulation.Profile)** are maintained in **wreq**.

## Building

1. Platforms

- Linux(**glibc**/**musl**): `x86_64`, `aarch64`, `armv7`, `i686`
- macOS: `x86_64`,`aarch64`
- Windows: `x86_64`,`i686`,`aarch64`
- Android: `aarch64`, `x86_64`

2. Development

Install the BoringSSL build environment by referring to [boringssl](https://github.com/google/boringssl/blob/main/BUILDING.md).

```bash
# on ubuntu or debian
sudo apt install -y build-essential cmake perl pkg-config libclang-dev musl-tools git
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
pip install uv maturin

uv venv
source .venv/bin/activate

# development
git submodule update --init --depth 1
maturin develop --uv --locked --manifest-path bindings/python/Cargo.toml

# build wheels
maturin build --locked --release --manifest-path bindings/python/Cargo.toml
```

## Benchmark

Our [benchmark suite](https://github.com/0x676e67/wreq-python/tree/main/bench) compares Python HTTP clients over HTTPS HTTP/1.1 and HTTP/2. It tests complete and streamed uploads, reading every response to the end. The results include client versions and machine details so you can check the conditions behind each measurement. Performance varies by workload and environment.

## License

Licensed under either of Apache License, Version 2.0 ([LICENSE](./LICENSE) or http://www.apache.org/licenses/LICENSE-2.0).

## Contribution

Unless you explicitly state otherwise, any contribution intentionally submitted for inclusion in the work by you, as defined in the [Apache-2.0](./LICENSE) license, shall be licensed as above, without any additional terms or conditions.
