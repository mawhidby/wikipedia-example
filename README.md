# braid wikipedia example

This example webapp uses [braid](https://github.com/braidery/braid) to explore the links in wikipedia articles.

## Getting started

* Make sure you have python 3 installed.
* Make sure you have braid installed, and that the applications are available in your `PATH`.
* Clone the repo.
* Get a copy of the [latest wikipedia data](https://dumps.wikimedia.org/enwiki/latest/enwiki-latest-pages-articles.xml.bz2) and download it into the root directory of the repo.
* Run `make init`.
* Run `make explorer`. The run will take a long time, as several GB worth of wikipedia data needs to be indexed in braid. But subsequent invocations of `make explorer` will be snappy.
