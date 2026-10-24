import argparse
import json
import os
import sys
from datetime import date

DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data.json")


def load():
    """Read saved goals and reviews. Missing or bad files start empty."""
    try:
        with open(DATA_FILE) as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {}
    data.setdefault("goals", [])
    data.setdefault("reviews", [])
    return data


def save(data):
    """Write goals and reviews to the JSON file."""
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=2)


def cmd_goals(args, data):
    """Set or show the 3 semester goals."""
    if args.set:
        data["goals"] = [g.strip() for g in args.set]
        print("Goals saved.")
    if not data["goals"]:
        print("No goals yet. Set them with: goals --set 'goal 1' 'goal 2' 'goal 3'")
        return
    print("\nSEMESTER GOALS")
    for number, goal in enumerate(data["goals"], start=1):
        print(f"{number}. {goal}")
    print("\nMy why: I'm here to graduate and build my future.")


def cmd_add(args, data):
    """Save this week's Friday review."""
    for text in (args.finished, args.proud, args.next_week):
        if not text.strip():
            raise ValueError("Every field needs some text.")
    data["reviews"].append({
        "date": date.today().isoformat(),
        "finished": args.finished.strip(),
        "proud": args.proud.strip(),
        "next": args.next_week.strip(),
    })
    print(f"Review saved. That is {len(data['reviews'])} week(s) logged. Keep going!")


def cmd_list(args, data):
    """Show all reviews, newest last."""
    if not data["reviews"]:
        print("No reviews yet.")
        return
    for review in data["reviews"]:
        print(f"\n--- {review['date']} ---")
        print(f"Finished: {review['finished']}")
        print(f"Proud of: {review['proud']}")
        print(f"Next week: {review['next']}")


def build_parser():
    parser = argparse.ArgumentParser(description="Friday review tracker")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("goals", help="Set or show your 3 goals")
    p.add_argument("--set", nargs=3, metavar="GOAL")
    p.set_defaults(func=cmd_goals)

    p = sub.add_parser("add", help="Add this week's review")
    p.add_argument("--finished", required=True)
    p.add_argument("--proud", required=True)
    p.add_argument("--next-week", dest="next_week", required=True)
    p.set_defaults(func=cmd_add)

    p = sub.add_parser("list", help="List all reviews")
    p.set_defaults(func=cmd_list)
    return parser


def main(argv=None):
    """Run one command. Returns 0 on success, 1 on a user error."""
    args = build_parser().parse_args(argv)
    data = load()
    try:
        args.func(args, data)
    except ValueError as error:
        print(f"Error: {error}")
        return 1
    save(data)
    return 0


if __name__ == "__main__":
    sys.exit(main())
