# test-site-content

Used to confirm the expected content was published and available online at a given time. This is useful for sites that expire the content after a certain time frame.

**Author**: Chris L Chapman
**Version**: 0.2.0

## Architecture

To view and test InstaGram Story posts, login credentials for an Instagram account are needed. This application is designed to be deployed on Google Cloud Platform, using:

Core packages required for this application:

- Flask
- Selenium
- ? bs4 and Beautiful Soup

Infrastructure and Installed Programs (not as packages):

- Linux
- Python 3.7
- Google Chrome
- Chromedriver

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
- `url_list`: a list of strings for each url of images that was saved to Storage buckets.
- `file_list`: a list of strings representing the saved images for this job.
- `error_files`: files that we could not capture, as a list of strings of the intended filename.
- `deleted`: files, and directory, removed from GAE filesystem after saved to Storage bucket.
- `message`: a string with additional information about this job.
- `saved_media`: reserved, but not present in the response.
- `post_model`: reserved, but not present in the response.

## Deployment Settings

[Deployed Site](https://capture-dot-engaged-builder-257615.appspot.com)

We are currently deploying on Google Cloud Platform (GCP), with the Google App Engine (GAE) - Flex environment. We are using a custom runtime that builds off of the GAE python3.7 runtime, as can be found in our Dockerfile. We are using Chrome and Chromedriver to run confirmation of live content and possible tests. Currently our Dockerfile will build with up-to-date stable versions of Chrome, as well as determine and install the correct version of Chromedriver as needed. As our application is running as a GAE - Flex environment, this means that it is essentially running as a Google Compute Engine, but with some additional helpful management features. Our deployment is hosted in `europe-west2` region (London) and in `europe-west2-a` zone.

## Development Notes

The Google App Engine - Flex environment, is essentially running as a Google Compute Engine. As we are running a custom runtime, we are responsible to keep our Dockerfile up to date. This is achieved by building on top of GAE python runtime (using python 3.7), as well as the procedures in the Dockerfile that ensure it uses the up-to-date stable version of Google Chrome and the appropriate Chromedriver. Other packages are installed with `pip` using pinned versions to ensure interoperability. These additional packages will be updated as needed and tracked in the `requirements.txt` file.

[Tasks & Checklist](./checklist.md)

We are also maintaining our [Development Notes](./DEVELOPEMENT_NOTES.md) which includes reference documentation that we have used or think may be useful in continuing to develop this project.
