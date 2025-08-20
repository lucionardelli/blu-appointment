import argparse
from pathlib import Path

from app.db.seeds.seed import (
    seed_payment_methods,
    seed_specialties,
    seed_users,
    seed_working_hours,
)

MODEL_IMPORT_FUNCTIONS_PATHS = {
    "specialties": (seed_specialties, "app/db/seeds/specialties.csv"),
    "users": (seed_users, "app/db/seeds/users.csv"),
    "working_hours": (seed_working_hours, "app/db/seeds/working_hours.csv"),
    "payment_methods": (seed_payment_methods, "app/db/seeds/payment_methods.csv"),
}

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "model", type=str, choices=[*MODEL_IMPORT_FUNCTIONS_PATHS.keys(), "all"], help="The model to seed"
    )
    args = parser.parse_args()

    if args.model == "all":
        for func, path in MODEL_IMPORT_FUNCTIONS_PATHS.values():
            func(Path(path))
    else:
        func, path = MODEL_IMPORT_FUNCTIONS_PATHS[args.model]
        func(Path(path))
