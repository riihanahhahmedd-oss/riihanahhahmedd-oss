from collections import defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path
import time
import requests

HANDLE = "Rihanah_101_r"
API = "https://codeforces.com/api/user.status"
OUTPUT = Path("assets/codeforces-heatmap-only.svg")

BG = "#171B22"
EMPTY = "#293442"
GREENS = ["#293442", "#0E4429", "#006D32", "#26A641", "#39D353"]


def fetch_submissions():
    """Fetch all public submissions for the configured Codeforces handle."""
    submissions = []
    offset = 1
    page_size = 10000

    while True:
        response = requests.get(
            API,
            params={"handle": HANDLE, "from": offset, "count": page_size},
            timeout=45,
            headers={"User-Agent": "Rihanah-GitHub-Profile/1.0"},
        )
        response.raise_for_status()
        payload = response.json()

        if payload.get("status") != "OK":
            raise RuntimeError(
                f"Codeforces API error for {HANDLE}: "
                f"{payload.get('comment', 'unknown error')}"
            )

        page = payload.get("result", [])
        submissions.extend(page)
        if len(page) < page_size:
            break

        offset += len(page)
        time.sleep(2)

    if not submissions:
        raise RuntimeError("Codeforces returned no submissions; keeping the previous heatmap.")

    print(f"Loaded {len(submissions)} public submissions for {HANDLE}.")
    return submissions


def accepted_activity_by_day(submissions):
    # Count distinct problems accepted on each UTC day, avoiding repeat submissions.
    activity = defaultdict(set)
    for item in submissions:
        if item.get("verdict") != "OK":
            continue

        problem = item.get("problem", {})
        contest_id = problem.get("contestId")
        index = problem.get("index")
        timestamp = item.get("creationTimeSeconds")

        if contest_id is None or not index or timestamp is None:
            continue

        day = datetime.fromtimestamp(timestamp, timezone.utc).date()
        activity[day].add((contest_id, index))

    return activity


def build_svg(activity):
    today = datetime.now(timezone.utc).date()
    start = today - timedelta(days=363)
    grid_start = start - timedelta(days=(start.weekday() + 1) % 7)

    width, height = 1800, 410
    left, top = 120, 105
    cell, gap = 20, 5
    step = cell + gap

    max_daily = max(
        (len(problems) for day, problems in activity.items()
         if start <= day <= today),
        default=1,
    )

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<defs><style>text{font-family:Inter,Segoe UI,Arial,sans-serif}.month{font-size:25px;fill:#AFC7E8}.day{font-size:21px;fill:#9AA8B8}</style></defs>',
        f'<rect x="12" y="12" width="{width-24}" height="{height-24}" rx="20" fill="{BG}" stroke="#526B8A" stroke-width="2"/>',
    ]

    # Month labels
    previous_month = None
    for week in range(53):
        day = grid_start + timedelta(days=week * 7)
        if day.month != previous_month:
            x = left + week * step
            parts.append(f'<text x="{x}" y="70" class="month">{day.strftime("%b")}</text>')
            previous_month = day.month

    # Weekday labels
    for row, label in [(1, "Mon"), (3, "Wed"), (5, "Fri")]:
        y = top + row * step + 16
        parts.append(f'<text x="35" y="{y}" class="day">{label}</text>')

    # Activity squares only: no totals, counts, streaks, or numeric labels.
    for week in range(53):
        for row in range(7):
            day = grid_start + timedelta(days=week * 7 + row)
            if day < start or day > today:
                continue

            count = len(activity.get(day, set()))
            if count == 0:
                level = 0
            else:
                level = min(4, max(1, (count * 4 + max_daily - 1) // max_daily))

            x = left + week * step
            y = top + row * step
            color = GREENS[level]
            parts.append(
                f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" '
                f'rx="3" fill="{color}"><title>{day.isoformat()}</title></rect>'
            )

    parts.append("</svg>")
    return "\n".join(parts)


def main():
    submissions = fetch_submissions()
    activity = accepted_activity_by_day(submissions)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(build_svg(activity), encoding="utf-8")
    print("Codeforces activity heatmap updated successfully.")


if __name__ == "__main__":
    main()
