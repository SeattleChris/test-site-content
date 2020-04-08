# Development Notes

Notes and documentation resources considered in developing this application.

## Serverless VPC Access

Connecting a Google App Engine (GAE) application to this test-site-content application (on GAE-Flex) without a publicly open route, through the Google Cloud Platform. This Serverless VPC Access is based on a resource called a *connector*. The GAE app will use the connector for internal network traffic to the GCE.

[GCP Connector](https://cloud.google.com/appengine/docs/standard/python3/connecting-vpc)

However, we seem to need extra steps to allow the dev site and production site to talk to each other. The [VPC Sharing](https://cloud.google.com/vpc/docs/using-vpc-peering) looks promising for this.

## Google Compute Engine notes

A Google Compute Engine handles its connections via Firewall Rules. They can connect to pull content from publicly available resources. Other connection options include:

1) Communicate within network, to other Compute Engine instances.
2) App Engine Standard. VPC rules do not apply. Only GAE firewall rules apply to ingress.
3) App Engine Flexible. Both GAE and VPC firewall rules apply to ingress. Outbound is VPC.
4) VPC network. But this is aiming for a "private" network.

## Google Cloud Platform Documentation

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
- [GAE Flex setup](https://cloud.google.com/appengine/docs/flexible/python/runtime)
- [SSH to GAE-Flex](https://cloud.google.com/appengine/docs/flexible/python/debugging-an-instance)
- [Warmup Requests](https://cloud.google.com/appengine/docs/standard/python3/configuring-warmup-requests)

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
