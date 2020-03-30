# test-site-content

Used to confirm the expected content was published and available online at a given time. This is useful for sites that expire the content after a certain time frame.

**Author**: Chris L Chapman
**Version**: 0.0.1

## Architecture

Designed to be deployed on Google Cloud App Engine, using:

Core packages required for this application:

- Flask
- Selenium
- ? bs4 and Beautiful Soup

Infrastructure and Installed Programs (not as packages):

- Linux (currently Ubuntu 18.04 LTS)
- Chrome (ver 80.0.3987.149)
- Chromedriver (ver 2.41.578700, for Chrome 80.0.3987.??)

Possibly needed:

- pyopenssl
- python-dotenv
- simplejson
- gunicorn
- requests (for dev only)

## API

The deployed site (see below) will accept the following routes and return an appropriate JSON response.

API Route: /api/v1/post/[id]/[media_type]/[media_id]/?url=[url-to-test-for-images]

Where [id] is a unique integer approved for associating for this specific post being analyzed for this job. The [id], [media_type] and [media_id] all correspond to the properties of the associated post, as understood in the client's application.

JSON Response has the following properties:

- `success`: True or False, if all the targeted images were found and recorded.
- `url`: a string for where the files are saved, currently a local file directory.
- `file_list`: a list of strings representing the saved images for this job.
- `message`: a string with additional information about this job.
- `saved_media`: reserved, but not present in the response.
- `post_model`: reserved, but not present in the response.

## Deployment Settings

[Deployed Site](https://www.bacchusinfluencerplatform.com)

We are currently deploying on Google Cloud Platform (GCP), with the Google Compute Engine. This is part of the Facebook Insights App. Based off of the templates below, the compute engine instance is named `capture-content-1` or `capture-content-2`. It is hosted in europe-west2 Region (London) and Zone: europe-west2-a

VM Instance templates named `capture-content` and `capture-content-docker` have the following settings. The machine configuration is set for general-purpose, first generation - N1 (Intel Skylake CPU or predecessors), fi-micro type (shared core: 1vCPU, 614MB memory). The CPU platform is set to automatic, display device is turned on, and the boot disk is a 10GB standard persistent disk running Ubuntu 18.04 LTS Minimal (Debian based Linux). Identity and API access is set to default Compute Engine service account (400949092475-compute@developer.gserviceaccount.com) with a scoop of default access (read-only to Storage & Service Management, write to Stackdriver Logging & Monitoring, read/write to Service Control) The firewall is set to allow HTTPS traffic (but not HTTP).

## Development Notes

The GCP Compute Engine platform is for installing and running containers. One solution might be to install a Linux OS container, and then install things on top of that as we are accustomed to doing as if it was a normal local machine. However, a better approach is to instantiate from Docker containers. We can make and host our own Docker Containers as needed. Where possible, it is best to utilize Docker Containers that are maintained by official sources.

A Compute Engine on GCP handles its connections via Firewall Rules. It seems it cannot expose a public url path. They can connect to pull content from publically available resources. Other connection options include:

1) Communicate within network, to other Compute Engine instances.
2) App Engine Standard. VPC rules do not apply. Only GAE firewall rules apply to ingress.
3) App Engine Flexible. Both GAE and VPC firewall rules apply to ingress. Outbound is VPC.
4) VPC network. But this is aiming for a "private" network.

[Tasks & Checklist](./checklist.md)

Google Cloud Platform Documentation:

- [App on Compute](https://cloud.google.com/python/tutorials/getting-started-on-compute-engine)
- [Compute Docs](https://cloud.google.com/compute/docs)
- [LAMP on GCE](https://cloud.google.com/community/tutorials/setting-up-lamp#setting-up-dns)
- [GCE Containers](https://cloud.google.com/compute/docs/containers/deploying-containers)
- [GCE backend buckets](https://cloud.google.com/sdk/gcloud/reference/compute/backend-buckets)
- [Cloud Functions as Trigger](https://cloud.google.com/functions/docs/how-to)

## Potential Resources

- [Chrome in Docker](https://github.com/c0b/chrome-in-docker) from unknown source.
- [Alpine Chrome](https://github.com/Zenika/alpine-chrome) Chrome Headless docker built on official alpine image.
- [Official Selenium w/ Browser](https://github.com/SeleniumHQ/docker-selenium) Standalone server with Node Chrome or FF.
- [Bucket set Docker for GCE](https://github.com/spinnaker/rosco/wiki/Run-Docker-on-a-GCE-Container-optimized-VM)
- [Host site on GCE not GAE](https://www.quora.com/How-do-I-host-my-site-on-Google-Compute-Engine)
  - Installs Apache 2. Answer dated December 2018

## Other Options

We could use the "browswerless" service. Or we can host our own version of their javascript based solution, building on their [docker container](https://hub.docker.com/r/browserless/chrome).
