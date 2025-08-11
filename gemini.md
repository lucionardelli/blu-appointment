## 1. Project Overview

Blu is a web-based application for managing medical appointments. It consists of a Vue.js frontend and a FastAPI backend. The application allows users to manage patients, specialties, and appointments.

Key features:
- User authentication
- Patient management
- Medical specialties management
- Appointments scheduling and management
- Internationalization (i18n) support

## 2. Development Environment

The project is containerized using Docker and managed with `docker-compose`. The backend is a Python/FastAPI application, and the frontend is a Vue.js application.

To run the development environment:
```bash
make run
```

The services will be available at:
- Frontend: `http://localhost:5173`
- Backend API: `http://localhost:8000`

The backend uses a SQLite database, but the database file lives inside the Docker container.
To access the database, you can use the following command to open a shell in the backend container:

```bash
make db
```

## 3. Codebase

### 3.1. File and Directory Structure

The project is organized into two main directories: `backend` and `frontend`.

```
/
├── backend/
│   ├── alembic/             # Alembic migrations
│   ├── app/                 # Main application code
│   │   ├── appointments/    # Appointments feature module
│   │   ├── auth/            # Authentication module
│   │   ├── core/            # Core components (config, security)
│   │   ├── db/              # Database setup and models
│   │   ├── patients/        # Patients feature module
│   │   ├── specialties/     # Specialties feature module
│   │   └── users/           # Users module
│   ├── tests/               # Backend tests
│   ├── alembic.ini          # Alembic configuration
│   ├── Dockerfile           # Dockerfile for the backend
│   ├── pyproject.toml       # Project metadata and dependencies
│   └── requirements.txt     # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── assets/          # Static assets
│   │   ├── components/      # Vue components
│   │   ├── layouts/         # Vue layouts
│   │   ├── locales/         # i18n locales
│   │   ├── router/          # Vue router configuration
│   │   ├── services/        # API services
│   │   ├── stores/          # Pinia stores
│   │   ├── utils/           # Utility functions
│   │   └── views/           # Vue views (pages)
│   ├── Dockerfile           # Dockerfile for the frontend
│   ├── index.html           # Main HTML file
│   ├── package.json         # NPM dependencies and scripts
│   └── vite.config.js       # Vite configuration
├── .dockerignore            # Docker ignore file
├── .gitignore               # Git ignore file
├── docker-compose.yml       # Docker Compose configuration
├── Makefile                 # Makefile with useful commands
└── README.md                # Project README
```

### 3.2. Key Technologies and Libraries

**Backend:**
- **Python 3.12**
- **FastAPI**: Web framework
- **SQLAlchemy**: ORM for database interaction
- **Alembic**: Database migrations
- **Pydantic**: Data validation
- **Uvicorn**: ASGI server
- **Pytest**: Testing framework
- **Ruff**: Linter and formatter

**Frontend:**
- **Vue.js 3**: JavaScript framework
- **Vite**: Build tool
- **Vue Router**: Routing
- **Pinia**: State management
- **Axios**: HTTP client
- **Tailwind CSS**: CSS framework
- **FullCalendar**: For appointment scheduling
- **Vue I18n**: Internationalization
- **ESLint**: Linter
- **Prettier**: Formatter

**DevOps:**
- **Docker**: Containerization
- **Docker Compose**: Multi-container application management

## 4. Commands

The following commands are available in the root `Makefile`:

- `make run`: Start the development environment in detached mode.
- `make down`: Stop the development environment.
- `make backend-logs`: View the backend service logs.
- `make backend-bash`: Access the backend container's shell.
- `make backend-test`: Run the backend tests.
- `make frontend-bash`: Access the frontend container's shell.
- `make frontend-logs`: View the frontend service logs.
- `make lint`: Run the linters for both backend and frontend.

The frontend has the following npm scripts (defined in `frontend/package.json`):
But they are meant to be run inside the frontend container, so you can use `make frontend-bash` to access the container and then run them:

- `npm run dev`: Start the development server.
- `npm run build`: Build the application for production.
- `npm run preview`: Preview the production build.
- `npm run lint`: Run the linter.
- `npm run format`: Format the code.
