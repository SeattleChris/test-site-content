# test-site-content

Used to confirm the expected content was published and available online at a given time. This is useful for sites that expire the content after a certain time frame.

**Author**: Chris L Chapman
**Version**: 0.0.1

## Architecture

Designed to be deployed on Google Cloud App Engine, using:

- TBA
- TBA

Core packages required for this application:

- Selenium
- Chrome
- Chromedriver
- ? bs4 and Beautiful Soup

Possibly needed:

- ? flask
- ? gunicorn
- ? google-api-python-client
- ? google-auth-httplib2
- ? google-auth
- ? requests-oauthlib

## API

The deployed site (see below) will accept the following routes and return an appropriate JSON response.

| Route              | Feature                                      | Response Example
|:------------------:|:--------------------------------------------:|:------------------:|
| /hello             | Proof of life response                       | {'success': true } |

## Deployment Settings

[Deployed Site](https://www.bacchusinfluencerplatform.com)

We are currently deploying on Google Cloud Platform (GCP), with the Google Compute Engine. The machine configuration is set for general-purpose, first generation - N1 (Intel Skylake CPU or predecessors), fi-micro type (shared core: 1vCPU, 614MB memory). The CPU platform is set to automatic, display device is turned on, and the boot disk is running the stable Container-Optimized OS (80-12739.104.0.stable), standard persistent disk of 10GB).

## Development Notes

The GCP Compute Engine platform is for intalling and running containers. One solution might be to install a Linux OS container, and then install things on top of that as we are accustomed to doing as if it was a normal local machine. However, a better approach is to instantiate from Docker containers. We can make and host our own Docker Containers as needed. Where possible, it is best to utilize Docker Containers that are maintained by official sources.



## Potential Resources

- [Chrome in Docker](https://github.com/c0b/chrome-in-docker) from unknown source.
- [Alpine Chrome](https://github.com/Zenika/alpine-chrome) Chrome Headless docker built on official alpine image.
- [Official Selenium w/ Browser](https://github.com/SeleniumHQ/docker-selenium) Standalone server with Node Chrome or FF.
- [Official Selenium](https://github.com/SeleniumHQ/docker-selenium) Docker images for Standalone, Hub, and Nodes.

## Other Options

We could use the "browswerless" service. Or we can host our own version of their javascript based solution, building on their [docker container](https://hub.docker.com/r/browserless/chrome).
