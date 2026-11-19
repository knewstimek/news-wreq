# news-wreq

Cargo workspace for the wreq HTTP client, wreq-util, and btls. The
workspace resolves these packages from its local source tree. The upstream
package names are retained so callers can use the existing crate names.

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
