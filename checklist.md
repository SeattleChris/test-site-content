# Feature Development Plan for March 2020 - ver 0.0.4

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
| :heavy_check_mark: | Continuously runs, app starts on server re-start      |
| :heavy_check_mark: | Captured images saved to bucket for other app use     |
| :heavy_check_mark: | Delete excess files after copies saved to Storage.    |
|                    | API usage is limited to authorized use.               |
|                    | **March 2020 Features Completed**                     |
|                    | Extra browser navigation for Story Posts is resolved. |
|                    | Instagram Login as needed for viewing Story Posts.    |
|                    | Using GCP Tasks, digesting queue and updating DB      |
| :heavy_check_mark: | DB records media file assoc, after files in Storage   |
| :white_check_mark: | API can accept url and storage location parameters    |

## Checklist

### Key

- [x] Completed.
- [n] No: does not work or decided against.
- [ ] Still needs to be done.
- [c] Needs to be confirmed.
- [?] Unsure if needed.
- [s] Stretch Goal. Not for current feature plan.

Current Status:
2020-04-10 02:23:40
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
  - [ ] Can it connect and digest the Task queue.
  - [ ] Does it record what Task queues have been processed.
  - [ ] How does the DB update the Post record to associate the media files?
    - [ ] Output another Task queue and have the Platform application process it.
    - [ ] Have this application connect and update the DB directly?
  - [ ] Take a warmup request or other technique to allow server to go to 0 live versions?
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
  - [?] with auth on an open route.
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
- [x] Update API: remove `url`, now returns `url_list` as a list of strings for urls for each file.
- [x] Update API: `url` directs to the summary.txt file that also has the `url_list` content.
- [x] Overwrite protection for Storage blob name, using a timestamp string prepended to file.
- [x] Can save to a static files bucket that can be used by other application.
- [x] Delete file copies on server after files are saved to Storage bucket.
- [x] Returned urls in url_list accurately link to view the image files.
- [x] Can be triggered by other application calling an API route.
- [?] URGENT Fix HTTPS self signing error.
  - [?] See readme development notes link to `Apps to instances`
  - [?] Also see readme development link to `VPC Firewall`
- [s] API can accept parameters for url and storage location.
- [ ] API usage is limited to authorized use.
  - [?] Only works via backend routes?
  - [?] Utilize authorization set up via Google Cloud Platform.
  - [?] Set up authorization API keys
- [ ] Confirm it works for Story Posts and for regular Posts.
