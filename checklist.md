# Feature Development Plan for March 2020 - ver 0.0.1

## Milestones

| Complete           | Task                                                  |
| ------------------ |:-----------------------------------------------------:|
|                    | **Setup**                                             |
| :heavy_check_mark: | Template and Instance settings researched and created |
| :heavy_check_mark: | Repo created, initial readme, ignore files, env       |
|                    | Selenium and Browser packages/docker setup            |
|                    | Basic application structure setup & `/hello` route.   |
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
2020-03-25 23:09:06
<!-- Ctrl-Shift-I to generate timestamp -->

### Setup

- [x] Initial research on Google Cloud Platform - Compute Engine
- [x] Create a VM template with our appropriate settings
- [x] Create a VM instance in our client's region.
- [x] Setup SSH connection through gcloud CLI
- [x] Setup Repo
- [x] Create Readme capturing core knowledge documentation
- [x] Create checklist connected to the Readme
- [x] setup env, gitignore, gcloudignore
- [ ] GCP Compute Structure Questions
  - [ ] Do we want a Docker Container automatically set in Instance & Template
  - [ ] Do we want a startup script to install packages?
  - [ ] Do we just install packages, and know they will be there on load up?
- [ ] Setup initial application structure

### Application

- [x] Have a copy of what worked in other App when running locally.
- [ ] Create proof of life `/hello` route.
- [ ] Refactor local App technique to work in this environment.
- [ ] Can save to a static files bucket that can be used by other application.
- [ ] Can be triggered by other application calling an API route.
- [ ] API can accept parameters for url and storage location.
