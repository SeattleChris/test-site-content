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
|                    | Can visit a given url and save a screenshot           |
|                    | Can navigate and capture each desired image           |
|                    | Captured images saved to bucket for other app use     |
|                    | Can be triggered via an API route                     |
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
2020-03-27 00:22:54
<!-- Ctrl-Shift-I to generate timestamp -->

### Setup

- [x] Initial research on Google Cloud Platform - Compute Engine.
- [x] Create a VM template with our appropriate settings.
- [x] Create a VM instance in our client's region.
- [x] Setup SSH connection through gcloud CLI.
- [x] Setup Repo.
- [x] Create Readme capturing core knowledge documentation.
- [x] Create checklist connected to the Readme.
- [x] setup env, gitignore, gcloudignore.
- [ ] GCP Compute Structure Questions.
  - [ ] Do we want a Docker Container automatically set in Instance & Template.
    - [x] VM instance: `capture-content-2`
    - [x] Start with selenium and standalone chrome
    - [ ] Add container for our specific code.
    - [ ] connect all the code together and get hello world locally
    - [ ] Expose a route to call the function.
    - [ ] connect all in VM and get hello world through exposed route
    - [ ] Create and use a startup script, if needed.
  - [ ] Do we want a startup script to install packages and start process?
  - [ ] Do we just install packages, and know they will be there on load up?
    - [x] VM instance: `capture-content-1`
    - [x] Seems complicated in maintaining the code up to date.
    - [ ] Get an exposed route for other apps
- [x] Setup initial application structure.

### Application

- [x] Have a copy of what worked in other App when running locally.
- [x] Create proof of life `/hello` route.
- [ ] Design for API.
  - [x] Implement API Exceptions
- [ ] Install chrome browser in this application.
  - [x] Directly on server when ssh in.
  - [ ] As a container
  - [ ] ? As part of a startup script?
- [x] Install bs4 (Beautiful Soup)
- [ ] See if it can be done without Beautiful Soup.
  - [ ] Different techniques to get that same data.
  - [ ] uninstall bs4, update requirements.
- [ ] Refactor local App technique to work in this environment.
- [ ] Can save to a static files bucket that can be used by other application.
- [ ] Can be triggered by other application calling an API route.
- [ ] API can accept parameters for url and storage location.
