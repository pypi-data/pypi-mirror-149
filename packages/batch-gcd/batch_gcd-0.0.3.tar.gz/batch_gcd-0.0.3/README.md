# Batch GCD

## Overview

A pure Python implementation of DJB's Batch GCD algorithm.

## Installation

Download and install with `pip`.

Or, download from source and install with `make install` (standard, user) or `make install_dev` (editable, system).

## Usage

This is a library and cannot be invoked directly.

Test with `make test`.

The `batch_gcd` module exposes a `batch_gcd` function which takes integers and returns a list of their GCDs at the corresponding index.

```python
>>> # Example batch_gcd usage
>>> from batch_gcd import batch_gcd
>>> batch_gcd(1909, 2923, 291, 205, 989, 62, 451, 1943, 1079, 2419)
[1909, 1, 1, 41, 23, 1, 41, 1, 83, 41]
```

This calculation involves two intermediate steps: creating a product tree and creating a remainder tree.
These functions are also exposed, as `products` and `remainders`.
`products` take integers and returns a product tree, `remainders` takes an integer and a product tree and returns a list of remainders.

## Resources

* [How to Find Smooth Parts of Integers](https://cr.yp.to/factorization/smoothparts-20040510.pdf)
* [FactHacks: Batch GCD](https://facthacks.cr.yp.to/batchgcd.html)
* [FactHacks: RSA Factorization in the Real World](https://www.hyperelliptic.org/tanja/vortraege/facthacks-29C3.pdf)
