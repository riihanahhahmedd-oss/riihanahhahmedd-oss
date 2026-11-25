from collections import defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path
import time
import requests

HANDLE = "Rihanah_101_r"
API = "https://codeforces.com/api/user.status"
OUTPUT = Path("assets/codeforces-stats.svg")

COLORS = {
    "background": "#171B22",
    "border": "#526B8A",
    "text": "#E6EDF3",
    "muted": "#9AA8B8",
    "levels": ["#293442", "#344B63", "#4F7094", "#789BC2", "#B7D0EA"],
}


def fetch_submissions():
    """Fetch every public submission, using Codeforces API pagination."""
    all_submissions = []
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
        all_submissions.extend(page)
        print(
            f"Fetched {len(page)} submissions from offset {offset}; "
            f"total fetched: {len(all_submissions)}"
        )

        if len(page) < page_size:
            break

        offset += len(page)
        time.sleep(2)

    if not all_submissions:
        raise RuntimeError(
            "Codeforces returned no submissions. Refusing to publish zero stats."
        )

    accepted = [
        item for item in all_submissions
        if item.get("verdict") == "OK"
        and item.get("problem", {}).get("contestId") is not None
        and item.get("problem", {}).get("index")
    ]
    unique_solved = {
        (item["problem"]["contestId"], item["problem"]["index"])
        for item in accepted
    }

    print(f"Verified handle: {HANDLE}")
    print(f"Total submissions: {len(all_submissions)}")
    print(f"Accepted submissions: {len(accepted)}")
    print(f"Distinct solved problems (all time): {len(unique_solved)}")

    return all_submissions


def collect_stats(submissions):
    solved_by_day = defaultdict(set)
    all_solved = set()

    for submission in submissions:
        if submission.get("verdict") != "OK":
            continue

        problem = submission.get("problem", {})
        contest_id = problem.get("contestId")
        index = problem.get("index")
        timestamp = submission.get("creationTimeSeconds")

        if contest_id is None or not index or timestamp is None:
            continue

        problem_key = (contest_id, index)
        solved_day = datetime.fromtimestamp(
            timestamp, timezone.utc
        ).date()

        all_solved.add(problem_key)
        solved_by_day[solved_day].add(problem_key)

    today = datetime.now(timezone.utc).date()
    year_start = today - timedelta(days=364)
    month_start = today - timedelta(days=29)

    def unique_in_period(start_date):
        return len({
            problem
            for day, problems in solved_by_day.items()
            if start_date <= day <= today
            for problem in problems
        })

    active_days = sorted(
        day for day, problems in solved_by_day.items() if problems
    )

    longest_streak = 0
    streak = 0
    previous_day = None

    for day in active_days:
        if previous_day is not None and day == previous_day + timedelta(days=1):
            streak += 1
        else:
            streak = 1
        longest_streak = max(longest_streak, streak)
        previous_day = day

    current_streak = 0
    latest_active_day = (
        today if today in solved_by_day
        else today - timedelta(days=1)
        if today - timedelta(days=1) in solved_by_day
        else None
    )

    if latest_active_day:
        cursor = latest_active_day
        current_streak = 1
        while cursor - timedelta(days=1) in solved_by_day:
            cursor -= timedelta(days=1)
            current_streak += 1

    stats = {
        "all_time": len(all_solved),
        "last_year": unique_in_period(year_start),
        "last_month": unique_in_period(month_start),
        "max_streak": longest_streak,
        "current_streak": current_streak,
        "active_days": sum(1 for day in active_days if year_start <= day <= today),
    }

    return solved_by_day, stats


def svg_card(daily, stats):
    today = datetime.now(timezone.utc).date()
    start = today - timedelta(days=363)
    grid_start = start - timedelta(days=(start.weekday() + 1) % 7)

    width, height = 1800, 690
    cell, gap = 20, 5
    left, top = 145, 150
    column_step = cell + gap
    row_step = cell + gap

    max_daily = max(
        (len(problems) for day, problems in daily.items()
         if start <= day <= today),
        default=1,
    )

    cells = []
    for week in range(53):
        for row in range(7):
            day = grid_start + timedelta(days=week * 7 + row)
            if day < start or day > today:
                continue

            count = len(daily.get(day, set()))
            if count == 0:
                level = 0
            else:
                level = min(4, max(1, (count * 4 + max_daily - 1) // max_daily))

            x = left + week * column_step
            y = top + row * row_step
            color = COLORS["levels"][level]
            cells.append(
                f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" '
                f'rx="4" fill="{color}">'
                f'<title>{day.isoformat()}: {count} distinct problems solved</title>'
                f'</rect>'
            )

    months = []
    previous_month = None
    for week in range(53):
        day = grid_start + timedelta(days=week * 7)
        if day.month != previous_month:
            x = left + week * column_step
            months.append(
                f'<text x="{x}" y="118" class="month">{day.strftime("%b")}</text>'
            )
            previous_month = day.month

    weekdays = []
    for row, label in [(1, "Mon"), (3, "Wed"), (5, "Fri")]:
        y = top + row * row_step + 16
        weekdays.append(f'<text x="75" y="{y}" class="day">{label}</text>')

    def metric(x, y, value, label):
        return (
            f'<text x="{x}" y="{y}" class="number">{value:,}</text>'
            f'<text x="{x}" y="{y + 36}" class="label">{label}</text>'
        )

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" '
        f'height="{height}" viewBox="0 0 {width} {height}">',
        '<defs><style>'
        'text{font-family:Inter,Segoe UI,Arial,sans-serif}'
        '.month{font-size:25px;fill:#AFC7E8}'
        '.day{font-size:21px;fill:#9AA8B8}'
        '.number{font-size:43px;font-weight:700;fill:#E6EDF3}'
        '.label{font-size:20px;fill:#9AA8B8}'
        '.heading{font-size:29px;font-weight:700;fill:#E6EDF3}'
        '.sub{font-size:17px;fill:#9AA8B8}'
        '</style></defs>',
        f'<rect x="12" y="12" width="{width - 24}" height="{height - 24}" '
        f'rx="20" fill="{COLORS["background"]}" '
        f'stroke="{COLORS["border"]}" stroke-width="2"/>',
        '<text x="75" y="68" class="heading">CODEFORCES ACTIVITY</text>',
        '<text x="1725" y="68" text-anchor="end" class="sub">'
        'LIVE FROM CODEFORCES API · UPDATED AUTOMATICALLY</text>',
        *months,
        *weekdays,
        *cells,
        metric(75, 455, stats["all_time"], "distinct problems solved · all time"),
        metric(665, 455, stats["last_year"], "distinct problems · last 365 days"),
        metric(1255, 455, stats["last_month"], "distinct problems · last 30 days"),
        metric(75, 565, stats["max_streak"], "longest solving streak · days"),
        metric(665, 565, stats["active_days"], "active days · last 365 days"),
        metric(1255, 565, stats["current_streak"], "current solving streak · days"),
        '<text x="1725" y="655" text-anchor="end" class="sub">'
        'Each square = one day · brighter squares = more distinct accepted problems'
        '</text>',
        '</svg>',
    ]

    return "\n".join(parts)


def main():
    submissions = fetch_submissions()
    daily, stats = collect_stats(submissions)

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(svg_card(daily, stats), encoding="utf-8")

    print("Codeforces dashboard generated successfully.")
    print(f"Final verified statistics: {stats}")


if __name__ == "__main__":
    main()
