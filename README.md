## Repository for the Future City Hackathon

Link to the competition: https://www.hs-heilbronn.de/de/hackathon

## Installation

### Backend

1. Install [uv](https://docs.astral.sh/uv/) (Python package manager)
2. Follow the instructions in [backend/README.md](backend/README.md)

### Frontend

1. Install [npm](https://www.npmjs.com/get-npm) (Node.js package manager)
2. Follow the instructions in [frontend/README.md](frontend/README.md)

## Tech

- Backend 
  - FastAPI / Flask (Python)
  - Deps: [pyproject.toml](backend/pyproject.toml)
- Frontend
  - React (TypeScript)
  - Deps: [package.json](frontend/package.json)
- API sends only JSON no HTML
- API if necessary REST
- DB if necessary sqlite3
- Containerization via Docker not necessary
- ORM sqlalchemy if necessary
- coding conventions
  - python code: snake_case
  - js/ts: camelCase
  - files/folders: kebab-case

## Timeplan

### Fr

- 16:15 check-in
- 17.00 welcome
- 17:30 challenges presented - Select challenge fast and discuss challenge
- 18:30 food and select challenge - discuss challenge
- 19:30 *Start*
- 21:00 go home - continue

Time 
19:30 - 22:00 (3.5 hours + [1.5 hours])

Tasks
- Select Challenge
- Software Architecture#
- DB Schema
- (UI Design)
- Define Requirements
- Setup Repositories
- Select Technologies

**Actual**: 19:00 - 00:00 (4 hour)

### Sa

Tasks
- Programming

Time
09:00 - 22:00 (13 hours)

**Actual**: 09:00 - 00:00 (15:00 hours)

### So

- 12:00 *internal Stop*
- 14:00 *Stop*
- 15:00 Presentation
- 16:00 Food
- 16:30 Results & Awards

Tasks
- Programming
- Manual E2E test
- Presentation

Time
09:00 - 12:00 (3 hours)

**Actual**: 09:00 - 12:30 (3.5 hours)

## Version controll

- branching strategy: single branch only
- **!Attention!**: Workpackets seperation very importand, features at best isolated from each other developable

## TODO

- what if non Relational DB is asked -> MongoDB but how (Lukas)

## Lessons Learned
- Color Pallete very useful, Pre Style Guide to just build pages with predefined components
- Early low fidelity Mockups very useful to get everyone on the same page -> UI
- Early DB Schema very useful, to get everyone on the same page -> Data
- Early Adaption of API endpoints for database, to see early issues in DB Schema
- structure of project (folders, ...) good, but more detailed better
- Good naming importand and did that aswell - very happy :)
- 13 Hours Max per Day (Human limit)
- Good Management is essential, communication
- Independent working, good work package seperation - constant communication
- SQLalchemy good, better than expected
- FastAPI very good can use again. Espeically /docs endpoint
- uv (python venv manager) - very good, use again
- Component based JS frontend framework very good (React rather than Angular), good statement management, good integration of API's
- TS good keep (if experience is there) else fallback to JS
- 