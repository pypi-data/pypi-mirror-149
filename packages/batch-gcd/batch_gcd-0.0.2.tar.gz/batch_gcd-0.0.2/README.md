# Batch GCD

## Overview

A pure Python implementation of DJB's Batch GCD algorithm.

## Installation

Install with `make install` (standard) or `make install_dev` (editable).
Or, download and install with `pip` by pointing it at this repository.

## Usage

This is a library and cannot be invoked directly.

Test with `make test`.

The `batch_gcd` module exposes a `batch_gcd` function which takes integers and returns a list of their GCDs at the corresponding index.

This calculation involves two intermediate steps: creating a product tree and creating a remainder tree.
These functions are also exposed, as `products` and `remainders`.
`products` take integers and returns a product tree, `remainders` takes an integer and a product tree.

## Resources

* [How to Find Smooth Parts of Integers](https://cr.yp.to/factorization/smoothparts-20040510.pdf)
* [FactHacks: Batch GCD](https://facthacks.cr.yp.to/batchgcd.html)
* [FactHacks: RSA Factorization in the Real World](https://www.hyperelliptic.org/tanja/vortraege/facthacks-29C3.pdf)
