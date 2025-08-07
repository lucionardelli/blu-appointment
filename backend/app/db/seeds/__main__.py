import argparse
from pathlib import Path

from app.db.seeds.seed import seed_specialties, seed_users

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("model", type=str, choices=["specialties", "users", "all"])
    args = parser.parse_args()

    if args.model == "all":
        seed_specialties(Path("app/db/seeds/specialties.csv"))
        seed_users(Path("app/db/seeds/users.csv"))
    elif args.model == "specialties":
        seed_specialties(Path("app/db/seeds/specialties.csv"))
    elif args.model == "users":
        seed_users(Path("app/db/seeds/users.csv"))
