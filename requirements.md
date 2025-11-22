Personas: 
    - Planer: people who order a to be delivered to b (and so on)
    - Deliverers: people who deliver goods from a to b
    - (Consumers): use items which got sent

Requirements:
    - As a planer, I want to send items to places

    - plane

External API's
- GoogleMaps, Google Street view

- API

- Structure
Frontend:
- pages:
    - every page has component in the corresponding component folder
(react router)

backend:
- db service 
- app 
- api (aufglieder unterschiedliche Dateinen)

- Pages:
    "/" - Dashboard (planer)
        - New Auftrag
    "/auftrag/{auftragId} - Auftrag Page (planer)

- API Endpoints:
  - **Planner**
    - "createJob" input: jobId -> [POST] Creates a Job
    - "updateJob" input: jobId -> [PUT] Updates a Job
    - "deleteJob" input: jobId -> [DELETE] Deletes a Job
    - "getJobs" -> [GET] Get all jobs
    - "getJobByJobId" input: jobId -> [GET] Get single Job
    - "filterJobs" input: { where } -> [GET] Get filtered Jobs

  - **Worker**
    - "getJobByWorkerId" input: workerId -> [GET] Get current job