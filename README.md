# news-wreq

news-wreq is an independently maintained fork of [wreq](https://github.com/0x676e67/wreq).
It brings wreq, wreq-util, and btls into one Cargo workspace and retains the
existing crate names.

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

Each component retains its upstream license files. BoringSSL is pinned by the
gitlink under btls. Cargo dependency versions are recorded in the root lockfile.

## Local checkout

```sh
git submodule update --init --depth 1
cargo metadata --locked --format-version 1
```
