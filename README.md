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

[Deployed Site](https://capture-dot-engaged-builder-257615.appspot.com)
[Development Site](https://35.230.145.5:8080)

We are currently deploying on Google Cloud Platform (GCP), with the Google Compute Engine. This is part of the Facebook Insights App. Based off of the templates below, the compute engine instance is named `capture-content-1` or `capture-content-2`. It is hosted in europe-west2 Region (London) and Zone: europe-west2-a

VM Instance templates named `capture-content` and `capture-content-docker` have the following settings. The machine configuration is set for general-purpose, first generation - N1 (Intel Skylake CPU or predecessors), fi-micro type (shared core: 1vCPU, 614MB memory). The CPU platform is set to automatic, display device is turned on, and the boot disk is a 10GB standard persistent disk running Ubuntu 18.04 LTS Minimal (Debian based Linux). Identity and API access is set to default Compute Engine service account (400949092475-compute@developer.gserviceaccount.com) with a scoop of default access (read-only to Storage & Service Management, write to Stackdriver Logging & Monitoring, read/write to Service Control) The firewall is set to allow HTTPS traffic (but not HTTP).

The development site template(s) and instance(s) allow both 'http' and 'https', and they grant full access privileges for Storage buckets (in addition to the normal access scope). For the deployed site, the templates and instances only allow 'https', and they have normal access scope, meaning they only have read access to Storage.

## Serverless VPC Access

Connecting a Google App Engine (GAE) application to this test-site-content application (on GCE) without a publicly open route, through the Google Cloud Platform. This Serverless VPC Access is based on a resource called a *connector*. The GAE app will use the connector for internal network traffic to the GCE.

[GCP Connector](https://cloud.google.com/appengine/docs/standard/python3/connecting-vpc)

However, we seem to need extra steps to allow the dev site and production site to talk to each other. The [VPC Sharing](https://cloud.google.com/vpc/docs/using-vpc-peering) looks promising for this.

## Development Notes

The GCP Compute Engine platform is for installing and running containers. One solution might be to install a Linux OS container, and then install things on top of that as we are accustomed to doing as if it was a normal local machine. However, a better approach is to instantiate from Docker containers. We can make and host our own Docker Containers as needed. Where possible, it is best to utilize Docker Containers that are maintained by official sources.

A Compute Engine on GCP handles its connections via Firewall Rules. It seems it cannot expose a public url path. They can connect to pull content from publicly available resources. Other connection options include:

1) Communicate within network, to other Compute Engine instances.
2) App Engine Standard. VPC rules do not apply. Only GAE firewall rules apply to ingress.
3) App Engine Flexible. Both GAE and VPC firewall rules apply to ingress. Outbound is VPC.
4) VPC network. But this is aiming for a "private" network.

[Tasks & Checklist](./checklist.md)

### Google Cloud Platform Documentation

If hosting on Compute Engine (GCE):

- [App on Compute](https://cloud.google.com/python/tutorials/getting-started-on-compute-engine)
- [Apps to instances](https://cloud.google.com/compute/docs/tutorials/service-account-ssh)
- [GAE to GCE](https://cloud.google.com/appengine/docs/standard/python3/connecting-vpc)
- [Compute Docs](https://cloud.google.com/compute/docs)
- [LAMP on GCE](https://cloud.google.com/community/tutorials/setting-up-lamp#setting-up-dns)
- [GCE Containers](https://cloud.google.com/compute/docs/containers/deploying-containers)
- [GCE backend buckets](https://cloud.google.com/sdk/gcloud/reference/compute/backend-buckets)
- [Server to Server](https://cloud.google.com/docs/authentication/production#auth-cloud-implicit-python)
- [Connect Bucket](https://cloud.google.com/compute/docs/disks/gcs-buckets)

If hosting as App Engine - Flex environment (which is also GCE under the hood):

- [GAE Flex yaml](https://cloud.google.com/appengine/docs/flexible/python/reference/app-yaml)
- [SSH to GAE-Flex](https://cloud.google.com/appengine/docs/flexible/python/debugging-an-instance)

Other Related Documentation:

- [VPC Firewall](https://cloud.google.com/vpc/docs/using-firewalls)
- [Cloud Functions as Trigger](https://cloud.google.com/functions/docs/how-to)
- [queue ?python2.7?](https://cloud.google.com/appengine/docs/standard/python/config/queueref)

## Potential Resources

- [Chrome in Docker](https://github.com/c0b/chrome-in-docker) from unknown source.
- [Alpine Chrome](https://github.com/Zenika/alpine-chrome) Chrome Headless docker built on official alpine image.
- [Official Selenium w/ Browser](https://github.com/SeleniumHQ/docker-selenium) Standalone server with Node Chrome or FF.
- [Bucket set Docker for GCE](https://github.com/spinnaker/rosco/wiki/Run-Docker-on-a-GCE-Container-optimized-VM)
- [Host site on GCE not GAE](https://www.quora.com/How-do-I-host-my-site-on-Google-Compute-Engine)
  - Installs Apache 2. Answer dated December 2018

## Setup New Server

If not using docker setup.

Install chrome & chromedriver. The [setup_chrome.py](./setup_chrome.py) script may achieve this automatically. The manual process is described below.

```Bash
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
apt install ./google-chrome-stable_current_amd64.deb
google-chrome --version
which google-chrome
```

First, find out which version of Chrome you are using. Let's say you have Chrome 72.0.3626.81.
Take the Chrome version number, remove the last part, and append the result to URL `https://chromedriver.storage.googleapis.com/LATEST_RELEASE_`. For example, with Chrome version 72.0.3626.81, you'd get a URL `https://chromedriver.storage.googleapis.com/LATEST_RELEASE_72.0.3626`.

Use the URL created in the last step to retrieve a small file containing the version of ChromeDriver to use. For example, the above URL will get your a file containing "72.0.3626.69". (The actual number may change in the future, of course.)

Use the version number retrieved from the previous step to construct the URL to download ChromeDriver. With version 72.0.3626.69, the URL would be `https://chromedriver.storage.googleapis.com/index.html?path=72.0.3626.69/`.
After the initial download, it is recommended that you occasionally go through the above process again to see if there are any bug fix releases.

Install Selenium, bs4 (Beautiful Soup), flask, simplejson, python-dotenv, openssl

## Other Options

We could use the "browswerless" service. Or we can host our own version of their javascript based solution, building on their [docker container](https://hub.docker.com/r/browserless/chrome).
