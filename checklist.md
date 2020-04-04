# Feature Development Plan for March 2020 - ver 0.0.1

## Milestones

| Complete           | Task                                                  |
| ------------------ |:-----------------------------------------------------:|
|                    | **Setup**                                             |
| :heavy_check_mark: | Template and Instance settings researched and created |
| :heavy_check_mark: | Repo created, initial readme, ignore files, env       |
| :heavy_check_mark: | Selenium and Browser packages/docker setup            |
| :heavy_check_mark: | Basic application structure setup & `/hello` route.   |
|                    | **Milestone 1 Completion**                            |
| :heavy_check_mark: | Can visit a given url and save a screenshot           |
| :heavy_check_mark: | Can navigate and capture each desired image           |
| :heavy_check_mark: | Can be triggered via an API route                     |
|                    | API usage is limited to authorized use                |
| :heavy_check_mark: | Continuously runs, app starts on server re-start      |
|                    | Captured images saved to bucket for other app use     |
|                    | API can accept url and storage location parameters    |
|                    | **March 2020 Features Completed**                     |

## Checklist

### Key

- [x] Completed.
- [n] No: does not work or decided against.
- [ ] Still needs to be done.
- [c] Needs to be confirmed.
- [?] Unsure if needed.
- [s] Stretch Goal. Not for current feature plan.

Current Status:
2020-04-03 15:18:11
<!-- Ctrl-Shift-I to generate timestamp -->

### Structure & Resources

- [x] Initial research on Google Cloud Platform - Compute Engine.
- [x] Create a VM template with our appropriate settings.
- [x] Create a VM instance in our client's region.
- [x] Setup SSH connection through gcloud CLI.
- [x] Setup Repo.
- [x] Create Readme capturing core knowledge documentation.
- [x] Create checklist connected to the Readme.
- [x] setup env, gitignore, gcloudignore.
- [ ] ? Use Tasks or a queue system as entry point trigger to start task?
- [n] Use Cloud Functions?
  - [n] Can Chrome run on Cloud Functions.
  - [n] Used as trigger or interface to Engine.
- [n] Use Cloud Run?
  - [x] filesystem writes not persisted. Must save to Bucket.
  - [?] No Chrome? "a container instance does not have any CPU available if it is not processing a request."
- [x] App Engine - Flex Environment
  - [x] Can it install and run Chrome?
  - [x] Custom Dockerfile: determine version & install chromedriver.
  - [x] run as a service (capture), and connect to other services (default, dev).
- [n] GCP Compute Structure Questions.
  - [n] Do we want a Docker Container automatically set in Instance & Template.
    - [x] VM instance: `capture-content-2`
    - [x] Start with selenium and standalone chrome.
    - [n] Add container for our specific code.
    - [n] can get it connected and exposed route running on GCP.
    - [?] Create and use a startup script, if needed.
  - [n] Do we want a startup script to install packages and start process?
  - [n] Do we just install packages, and know they will be there on load up?
    - [x] VM instance: `capture-content-1` .
    - [x] Seems complicated in maintaining the code up to date.
    - [x] Get an exposed route for other apps.
- [x] App always running.
  - [x] Install screen.
  - [X] screen works to keep process running after logout.
  - [n] Startup script to start app works on server restart.
- [x] Setup initial application structure.
- [ ] Can be called by the platform application.
  - [x] as an open route for an API call.
  - [ ] through GCP using a service agent (more secure).

### Application

- [x] Have a copy of what worked in other App when running locally.
- [x] Create proof of life `/hello` route.
- [x] Install (not as packages) chrome browser in this application.
- [x] Install needed packages: Flask, Selenium, bs4 (Beautiful Soup), etc.
- [x] Determine and install the appropriate chromedriver.
- [x] Design for API.
  - [x] Implement API Exceptions.
  - [x] Give a JSON Response.
  - [x] Document the API in the Readme.
- [x] connect all in VM and get hello world through exposed route.
- [x] Expose a route and test API with known and dummy values.
  - [x] Directly on server when ssh in.
  - [?] As a container.
  - [?] ? As part of a startup script?
- [ ] See if it can be done without Beautiful Soup.
  - [ ] Different techniques to get that same data.
  - [ ] uninstall bs4, update requirements.
- [x] Refactor local App technique to work in this environment.
- [x] Returns a JSON Response with `success` boolean, and other information.
- [x] Returns a JSON Response with `url` string of where the file is stored.
- [ ] After images are stored in accessible location, `url` represents the location.
- [ ] Can save to a static files bucket that can be used by other application.
- [x] Can be triggered by other application calling an API route.
- [ ] URGENT Fix HTTPS self signing error.
  - [ ] See readme link to `Apps to instances`
  - [ ] Also see readme link to `VPC Firewall`
- [ ] API can accept parameters for url and storage location.
- [ ] API usage is limited to authorized use.
  - [?] Only works via backend routes?
  - [?] Utilize authorization set up via Google Cloud Platform.
  - [?] Set up authorization API keys
