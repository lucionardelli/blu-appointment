from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.patients.models import Patient

UNDERAGE_SESSION_DURATION = 3  # Underage session duration in minutes
ADULT_FIRST_3_SESSIONS_DURATION = 3  # First three sessions for adults
ADULT_NEXT_3_SESSIONS_DURATION = 6  # Next three sessions for adults
ADULT_FOLLOWING_SESSIONS_DURATION = 9  # After six sessions for adults


def calculate_age_and_session_based_duration(patient: "Patient", session_count: int) -> int:
    """Calculates treatment duration based on patient's age and session count.
    - Underage: 3 mins
    - Adults: First 3 sessions, 3 minutes. Next three sesisones, 6 minutes. Then on, 9 minutes
    """
    # The session_count is the number of *past* appointments.
    # The current appointment is the next session.
    current_session_number = session_count + 1

    if patient.is_underage:  # We are assuming that all patients without a DOB are adults.
        return 3
    if current_session_number <= 3:  # noqa: PLR2004
        return ADULT_FIRST_3_SESSIONS_DURATION
    if current_session_number <= 6:  # noqa: PLR2004
        return ADULT_NEXT_3_SESSIONS_DURATION
    return ADULT_FOLLOWING_SESSIONS_DURATION


LOGIC_REGISTRY = {
    "age_and_session_based_v1": calculate_age_and_session_based_duration,
}


def get_treatment_duration(logic_key: str | None, patient: "Patient", session_count: int) -> int | None:
    """Looks up the logic key in the registry and returns the calculated duration."""
    if not logic_key or logic_key not in LOGIC_REGISTRY:
        return None

    calculation_func = LOGIC_REGISTRY[logic_key]
    return calculation_func(patient, session_count)
