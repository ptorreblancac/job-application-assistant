
# Job Application Assistant

A full-stack web application designed to help job seekers discover relevant job opportunities and evaluate how well each position matches their professional profile.

Users can define their career preferences, including target roles, location, seniority, preferred skills and work arrangements. The application retrieves job listings from the Adzuna API and uses semantic similarity combined with multiple profile-based criteria to calculate a relevance score for each opportunity.

The goal is to make job searching more structured and efficient by helping users identify opportunities that align with their skills and career objectives.

## Features

- **Job discovery:** Retrieve job listings from the Adzuna API based on the user's target role and location.
- **Profile management:** Define and update job-search preferences, including target role, location, seniority, skills and preferred work arrangements.
- **Semantic job matching:** Compare job titles using sentence embeddings to identify relevant positions, even when their wording differs.
- **Multi-criteria scoring:** Evaluate opportunities based on role relevance, skills, seniority, location and work arrangements.
- **Job dashboard:** View available opportunities and their relevance scores.
- **Job filtering:** Filter job listings by company and job type.
- **Match recalculation:** Automatically recalculate existing job relevance scores when the search profile is updated.

## Technology Stack

| Area | Technologies |
|---|---|
| Frontend | React, JavaScript, HTML, CSS |
| Frontend tooling | Vite, npm |
| Backend | Python, Django |
| Database | SQLite |
| Machine learning / NLP | Sentence Transformers, BAAI/bge-small-en-v1.5 |
| External API | Adzuna Jobs API |
| Testing | Django Test Framework, Vitest, React Testing Library |
| Version control | Git, GitHub |

## Application Architecture

The application follows a frontend-backend architecture.

- **Frontend:** A React single-page application responsible for navigation, displaying job opportunities and managing search preferences.
- **Backend:** A Django application that exposes JSON endpoints, manages database operations, retrieves job listings and calculates relevance scores.
- **Database:** SQLite stores job listings, search profiles and profile-specific job matches.
- **External integration:** The Adzuna API provides job listings that are transformed and stored in the application's database.

### Main Components

| Component | Responsibility |
|---|---|
| `jobs/models.py` | Defines the database models and relationships. |
| `jobs/views.py` | Implements the JSON API endpoints. |
| `jobs/services.py` | Handles Adzuna integration, data transformation, persistence and match recalculation. |
| `jobs/matching.py` | Implements semantic similarity and the job matching algorithm. |
| `jobs/management/commands/` | Contains the custom Django management command for importing jobs. |
| `frontend/src/components/` | Contains the React interface components. |

### Database Design

The backend uses three main models:

**Job**

Stores job listing information, including:
- Job title and company
- Location and country
- Salary and job type
- Description, requirements and qualifications
- Posting date and expected start date
- Original job posting URL

The posting URL is unique to prevent duplicate job listings.

**SearchProfile**

Stores the user's job-search preferences:
- Target role
- Location and country
- Seniority
- Preferred skills
- Preferred work arrangements

**ProfileJobMatch**

Connects search profiles with job listings through a many-to-many relationship.

It stores the relevance score and the date on which the match was created. A unique database constraint ensures that each profile-job combination is stored only once.

This structure allows the same job to have different relevance scores depending on the search profile.

## Job Matching Algorithm

The application uses a multi-criteria scoring system to evaluate how relevant a job opportunity is to a search profile.

Each job receives a score between 0 and 100 points.

| Criterion | Maximum points |
|---|---:|
| Role relevance | 30 |
| Skills | 35 |
| Seniority | 15 |
| Location | 10 |
| Work arrangement | 10 |
| **Total** | **100** |

### 1. Role Relevance — 30 points

Semantic similarity is calculated using the `BAAI/bge-small-en-v1.5` sentence-transformer model.

Job titles are converted into numerical embeddings, which are compared using cosine similarity.

Before comparing titles, seniority-related terms such as *Junior*, *Senior*, *Graduate* and *Intern* are removed. This allows role relevance to be evaluated independently of seniority.

The similarity score is transformed into a relevance score using a calibrated linear function:

```python
score = (-3.7103 + 9.1598 * similarity) * 6
```

The resulting score is constrained to the interval [0, 30].

### 2. Skills — 35 points

The algorithm checks whether the user's preferred skills appear in the job description, requirements or qualifications.

The score is proportional to the number of matching skills:

```python
score = (matching_skills / preferred_skills) * 35
```

### 3. Seniority — 15 points

The algorithm identifies seniority indicators in the job title, description and requirements.

A job receives 15 points when its detected seniority matches the user's selected seniority. An explicit mismatch or the absence of a detected seniority results in zero points.

### 4. Location — 10 points

A job receives 10 points when its location exactly matches the location specified in the search profile.

### 5. Work Arrangement — 10 points

The algorithm checks whether at least one of the user's preferred work arrangements appears in the job description or requirements.

If a preferred arrangement is found, the job receives 10 points.

## Project Structure

The project is organised into a Django backend and a React frontend.

```text
job-application-assistant/
│
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── jobs/
│   ├── migrations/
│   ├── management/
│   │   └── commands/
│   │       └── import_adzuna_jobs.py
│   ├── models.py
│   ├── views.py
│   ├── services.py
│   ├── matching.py
│   ├── evaluations.py
│   └── tests.py
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Dashboard.jsx
│   │   │   ├── Header.jsx
│   │   │   ├── JobCard.jsx
│   │   │   ├── JobSearch.jsx
│   │   │   ├── Profile.jsx
│   │   │   ├── Sidebar.jsx
│   │   │   └── StatCard.jsx
│   │   ├── test/
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
│
├── .env
├── .gitignore
├── manage.py
├── requirements.txt
└── README.md
```

## Getting Started

### Prerequisites

Make sure you have installed:

- Python 3.10 or later
- Node.js and npm
- Git
- An Adzuna API account with an application ID and API key

### 1. Clone the Repository

```bash
git clone https://github.com/ptorreblancac/job-application-assistant.git

cd job-application-assistant
```

### 2. Backend Setup

Create and activate a Python virtual environment.

**Windows (PowerShell):**

```powershell
python -m venv .venv

.venv\Scripts\Activate.ps1
```

Install the Python dependencies:

```bash
pip install -r requirements.txt
```

The matching engine also requires Sentence Transformers. Ensure `sentence-transformers` is included in `requirements.txt` and install it if it is not already installed:

```bash
pip install sentence-transformers
```

### 3. Environment Variables

Create a `.env` file in the project root and add your Adzuna API credentials:

```env
ADZUNA_APP_ID=your_app_id
ADZUNA_APP_KEY=your_app_key
```

Replace the placeholders with your actual credentials.

**Important:** Never commit your `.env` file or expose API credentials in your repository.

### 4. Database Setup

Apply the Django migrations:

```bash
python manage.py migrate
```

Create a superuser to access the Django admin interface:

```bash
python manage.py createsuperuser
```

Create a search profile through the Django admin interface or another database-management method.

### 5. Frontend Setup

Open a terminal in the frontend directory:

```bash
cd frontend

npm install
```

## Running the Application

The backend and frontend run independently, so two terminals are required.

### Start the Django Backend

From the project root:

```bash
python manage.py runserver
```

The backend will be available at:

`http://127.0.0.1:8000/`

### Start the React Frontend

From the `frontend/` directory:

```bash
npm run dev
```

Vite will provide the local frontend URL, usually:

`http://localhost:5173/`

## Importing Job Listings

Job importing is currently triggered manually through a custom Django management command.

To retrieve and import job listings for a specific search profile:

```bash
python manage.py import_adzuna_jobs --profile-id 1
```

Replace `1` with the ID of the search profile you want to use.

The command:
1. Retrieves the selected search profile.
2. Fetches job listings from the Adzuna API.
3. Transforms the API responses into the application's job format.
4. Saves new jobs while avoiding duplicate posting URLs.
5. Calculates relevance scores for each job.
6. Creates or updates the corresponding profile-job matches.

The command reports how many new jobs were imported and how many were already present in the database.

## API Endpoints

The Django backend exposes the following JSON endpoints:

| Method | Endpoint | Description |
|---|---|---|
| GET | `/jobs/` | Retrieve job listings. |
| GET | `/jobs/?company=CompanyName` | Filter jobs by company. |
| GET | `/jobs/?job_type=full_time` | Filter jobs by job type. |
| GET | `/jobs/<job_id>/` | Retrieve an individual job. |
| GET | `/jobs/profiles/<profile_id>/` | Retrieve a search profile. |
| PUT | `/jobs/profiles/<profile_id>/update/` | Update a profile and recalculate its job matches. |

The endpoints return JSON responses consumed by the React frontend.

## Testing

The project includes backend and frontend tests.

### Backend Tests

From the project root:

```bash
python manage.py test
```

Django's test framework is used to test backend functionality, including models, API endpoints and matching-related behaviour.

### Frontend Tests

From the `frontend/` directory:

```bash
npm test
```

The frontend tests use Vitest and React Testing Library to verify component rendering, user interactions, navigation and API-related behaviour.

### Additional Checks

Run the frontend linter:

```bash
npm run lint
```

Create a production build:

```bash
npm run build
```

## Future Improvements

Potential improvements include:

- Supporting multiple target roles within a single search profile.
- Improving seniority detection and matching accuracy.
- Expanding job retrieval beyond the initial set of Adzuna results.
- Improving skills extraction and matching beyond simple keyword detection.
- Supporting more flexible location matching.
- Adding automatic or scheduled job imports.
- Allowing users to save job opportunities and track applications.
- Improving API validation, error handling and security.
- Deploying the application to a cloud environment.

## Author

Developed as a personal full-stack software engineering project to explore backend development, frontend integration, API consumption, database design and semantic job matching.
