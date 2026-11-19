# news-wreq

news-wreq is an independently maintained fork of [wreq](https://github.com/0x676e67/wreq).
It brings wreq, wreq-util, btls, and the wreq Python bindings into one Cargo
workspace and retains the existing crate and Python import names.

## Why this fork exists

We use this fork to ship updates quickly on our own release schedule. We take
responsibility for reviewing, testing, and supporting the changes we ship,
including AI-assisted work. When we contribute upstream, we follow that
project's contribution guidelines.

## Source revisions

| Component | Upstream commit |
| --- | --- |
| [wreq](https://github.com/0x676e67/wreq/tree/a7029ea84f7e79858da7cde7c9dc6be4903bebbd) | a7029ea84f7e79858da7cde7c9dc6be4903bebbd |
| [wreq-util](https://github.com/0x676e67/wreq-util/tree/917d2581d6761a94db66466caa6c2eb4d4cdbd43) | 917d2581d6761a94db66466caa6c2eb4d4cdbd43 |
| [btls](https://github.com/0x676e67/btls/tree/3c1dd080ba617d78c63cd09285d2ce31abcdcbf9) | 3c1dd080ba617d78c63cd09285d2ce31abcdcbf9 |
| [wreq-python](https://github.com/0x676e67/wreq-python/tree/0e0849338162527721529c0c07cfe8f86d2e04cc) | 0e0849338162527721529c0c07cfe8f86d2e04cc |

Each component retains its upstream license files. BoringSSL is pinned by the
gitlink under btls. Cargo dependency versions are recorded in the root lockfile.

## Local checkout

```sh
git submodule update --init --depth 1
cargo metadata --locked --format-version 1
```

## Python wheel

With Python 3.11 or later and maturin installed, build the wheel from the
workspace root after initializing the BoringSSL submodule.
An x64 Windows source build also needs CMake, MSVC, NASM, and libclang.

```sh
maturin build --locked --release --manifest-path bindings/python/Cargo.toml
```

The wheel retains `import wreq` and uses this checkout's `wreq`, `wreq-util`,
and `btls`. Install the generated wheel from `target/wheels`. The Python
distribution version carries this fork's local version suffix.

`wreq.TlsOptions` accepts `client_hello_padding`, `post_handshake_auth`,
and `sigalgs_list`. For TLS 1.3 cipher ordering, pass
`tls13_cipher_list` with `wreq.Tls13Cipher` values. The upstream Python
binding's AES hardware overrides and `preserve_tls13_cipher_list` are
unavailable in this workspace's TLS API.
