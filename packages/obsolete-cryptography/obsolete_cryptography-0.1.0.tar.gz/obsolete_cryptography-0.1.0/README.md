# obsolete-cryptography

Toolbox for exploring various obsolete ciphers and hash algorithms. Based on mcrypt and mhash.

**WARNING**: A lot of algorithms provided by this package are no longer considered secure. DO NOT use obsolete ciphers or hash algorithms when designing new secure systems. You might want [cryptography](https://cryptography.io/en/latest/) for a secure, validated and easy to use crypto library that is suitable for new designs.

## Building

Only tested on Linux.

This project uses the new PEP-517 source tree format.

To manually build the wheel, first make sure you have working C compiler, `make` and `libtool` (usually provided by the distro development package group like `build-essential`) and the PEP-517 builder `build` is installed, then run

```sh
python -mbuild --wheel
```

under the project directory. The wheel will be built under the `dist/` directory after it's built successfully.

## Notes on the design

Under the hood, this library is essentially a Cython binding to libmcrypt and mhash. Both libraries are included and are statically linked to the binding to simplify the building and installation process.

The libmcrypt included is based on libmcrypt 2.5.8 and has patches that enable out-of-tree building (required by meson) and enable the original SAFER algorithm that was previously disabled due to a bug. The mhash library is just a stock mhash 0.9.9.9 for now.
