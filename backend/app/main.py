from fastapi import FastAPI

from .appointments import router as appointments_router
from .patients import router as patients_router
from .specialties import router as specialties_router
from .users import router as users_router

app = FastAPI(
    title="Blu Appointment Manager",
    description="API for managing appointments, patients, and payments.",
    version="0.1.0",
)


@app.get("/")
def read_root() -> dict[str, str]:
    return {"message": "Welcome to the Blu API"}


# Include routers from feature modules
app.include_router(users_router, prefix="/api/v1/users", tags=["users"])
app.include_router(patients_router, prefix="/api/v1/patients", tags=["patients"])
app.include_router(specialties_router, prefix="/api/v1/specialties", tags=["specialties"])
app.include_router(appointments_router, prefix="/api/v1/appointments", tags=["appointments"])
