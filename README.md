# HealthSurveillanceFramework
This repository contains the reference implementation of our framework for public health surveillance. The framework's architecture is illustrated in architecture.pdf. The API is documented in *APIv1.md*.

# Code
The repository's primary purpose is to illustrate the framework's architecture and API. We are in the process of releasing the code described in [1] that conforms to *HealthSurveillanceFramework*'s API. We will continue to release additional code with new publications.

This repository contains Python abstract classes and example components conforming to the API, and Java classes for reading and writing the API's file formats.

## Python
* *framework*: contains Python abstract classes for implementing the framework's API
* *component/example*: contains simple examples of each component
* *data/example*: contains synthetic data for use with the component examples

## Java
* *java/src/healthSurveillanceFramework/fileFormats*: classes for handling input/output files

# References
1. J. Parker, Y. Wei, A. Yates, N. Goharian, O. Frieder, "A Framework for Detecting Public Health Trends with Twitter", *The 2013 IEEE/ACM International Conference on Advances in Social Network Analysis and Mining*, August 2013.
