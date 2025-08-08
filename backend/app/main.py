from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.appointments.router import router as appointments_router
from app.db.base import Base, engine
from app.patients.router import router as patients_router
from app.specialties.router import router as specialties_router
from app.users.router import router as users_router
from app.auth.router import router as auth_router


@asynccontextmanager
async def lifespan(_app: FastAPI):  # noqa: ANN201
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="Blu Appointment Manager",
    description="API for managing appointments, patients, and payments.",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root() -> dict[str, str]:
    return {"message": "Welcome to the Blu API"}


# Include routers from feature modules
app.include_router(auth_router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(users_router, prefix="/api/v1/users", tags=["users"])
app.include_router(patients_router, prefix="/api/v1/patients", tags=["patients"])
app.include_router(specialties_router, prefix="/api/v1/specialties", tags=["specialties"])
app.include_router(appointments_router, prefix="/api/v1/appointments", tags=["appointments"])
