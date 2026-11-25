from collections import defaultdict
from datetime import datetime, timezone, timedelta
from pathlib import Path
import time
import requests

HANDLE = "Rihanah_101_r"
API = "https://codeforces.com/api/user.status"
OUTPUT = Path("assets/codeforces-stats.svg")
COUNT_OUTPUT = Path("assets/codeforces-problems-count.svg")
COLORS = {
    "background": "#171B22",
    "border": "#526B8A",
    "text": "#E6EDF3",
    "muted": "#9AA8B8",
    "empty": "#293442",
    "levels": ["#293442", "#344B63", "#4F7094", "#789BC2", "#B7D0EA"],
}

def fetch_submissions():
    all_submissions = []
    start = 1
    batch_size = 5000
    while True:
        response = requests.get(
            API,
            params={"handle": HANDLE, "from": start, "count": batch_size},
            timeout=30,
            headers={"User-Agent": "Rihanah-GitHub-Profile/1.0"},
        )
        response.raise_for_status()
        payload = response.json()
        if payload.get("status") != "OK":
            raise RuntimeError(payload.get("comment", "Codeforces API returned an error"))
        batch = payload.get("result", [])
        all_submissions.extend(batch)
        if len(batch) < batch_size:
            break
        start += len(batch)
        time.sleep(2)
    return all_submissions

def collect_stats(submissions):
    solved = set()
    solved_dates = defaultdict(set)
    for item in submissions:
        if item.get("verdict") != "OK":
            continue
        problem = item.get("problem", {})
        contest_id, index = problem.get("contestId"), problem.get("index")
        timestamp = item.get("creationTimeSeconds")
        if contest_id is None or not index or timestamp is None:
            continue
        key = (contest_id, index)
        day = datetime.fromtimestamp(timestamp, timezone.utc).date()
        solved.add(key)
        solved_dates[day].add(key)

    today = datetime.now(timezone.utc).date()
    year_start = today - timedelta(days=364)
    month_start = today - timedelta(days=29)
    all_time = len(solved)
    last_year = len({p for d, problems in solved_dates.items() if d >= year_start for p in problems})
    last_month = len({p for d, problems in solved_dates.items() if d >= month_start for p in problems})

    active = sorted(d for d, problems in solved_dates.items() if problems)
    max_streak = current_streak = 0
    previous = None
    streak = 0
    for day in active:
        streak = streak + 1 if previous and day == previous + timedelta(days=1) else 1
        max_streak = max(max_streak, streak)
        previous = day

    if today in solved_dates:
        cursor = today
    elif today - timedelta(days=1) in solved_dates:
        cursor = today - timedelta(days=1)
    else:
        cursor = None
    if cursor:
        current_streak = 1
        while cursor - timedelta(days=1) in solved_dates:
            cursor -= timedelta(days=1)
            current_streak += 1

    return solved_dates, {
        "all_time": all_time,
        "last_year": last_year,
        "last_month": last_month,
        "max_streak": max_streak,
        "current_streak": current_streak,
        "active_days": sum(1 for d in active if d >= year_start),
    }

def svg_card(daily, stats):
    today = datetime.now(timezone.utc).date()
    start = today - timedelta(days=363)
    # Align the first column to Sunday, like a contribution calendar.
    grid_start = start - timedelta(days=(start.weekday() + 1) % 7)
    cell, gap = 23, 6
    left, top = 150, 150
    width, height = 2048, 740
    plot = []
    max_daily = max((len(v) for d, v in daily.items() if d >= start), default=1)
    for week in range(53):
        for row in range(7):
            day = grid_start + timedelta(days=week * 7 + row)
            if day < start or day > today:
                continue
            count = len(daily.get(day, set()))
            level = 0 if count == 0 else min(4, max(1, (count * 4 + max_daily - 1) // max_daily))
            color = COLORS["levels"][level]
            x, y = left + week * (cell + gap), top + row * (cell + gap)
            plot.append(f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" rx="3" fill="{color}"><title>{day.isoformat()}: {count} distinct problems solved</title></rect>')

    months = []
    previous_month = None
    for week in range(53):
        day = grid_start + timedelta(days=week * 7)
        if day.month != previous_month:
            x = left + week * (cell + gap)
            months.append(f'<text x="{x}" y="118" class="month">{day.strftime("%b")}</text>')
            previous_month = day.month

    day_labels = []
    for row, label in [(1, "Mon"), (3, "Wed"), (5, "Fri")]:
        y = top + row * (cell + gap) + 17
        day_labels.append(f'<text x="92" y="{y}" class="day">{label}</text>')

    def metric(x, y, value, label):
        return f'<text x="{x}" y="{y}" class="number">{value:,}</text><text x="{x}" y="{y+42}" class="label">{label}</text>'

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<defs><style>text{font-family:Inter,Segoe UI,Arial,sans-serif}.month{font-size:28px;fill:#AFC7E8}.day{font-size:25px;fill:#9AA8B8}.number{font-size:48px;font-weight:600;fill:#E6EDF3}.label{font-size:23px;fill:#9AA8B8}.heading{font-size:31px;font-weight:600;fill:#E6EDF3}.sub{font-size:19px;fill:#9AA8B8}</style></defs>',
        f'<rect x="12" y="12" width="2024" height="716" rx="18" fill="{COLORS["background"]}" stroke="{COLORS["border"]}" stroke-width="2"/>',
        '<text x="92" y="72" class="heading">CODEFORCES ACTIVITY</text>',
        '<text x="1950" y="72" text-anchor="end" class="sub">LIVE FROM CODEFORCES API · UPDATED AUTOMATICALLY</text>',
        *months, *day_labels, *plot,
        metric(92, 520, stats["all_time"], "problems solved · all time"),
        metric(730, 520, stats["last_year"], "problems solved · last 365 days"),
        metric(1368, 520, stats["last_month"], "problems solved · last 30 days"),
        metric(92, 650, stats["max_streak"], "longest solving streak · days"),
        metric(730, 650, stats["active_days"], "active days · last 365 days"),
        metric(1368, 650, stats["current_streak"], "current solving streak · days"),
        '<text x="1950" y="700" text-anchor="end" class="sub">Each square represents one day · brighter squares mean more accepted problems</text>',
        '</svg>',
    ]
    return "\n".join(parts)

def problems_count_card(count):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="900" height="300" viewBox="0 0 900 300">
<defs><style>text{{font-family:Inter,Segoe UI,Arial,sans-serif}}.eyebrow{{font-size:23px;letter-spacing:2px;fill:#AFC7E8}}.number{{font-size:92px;font-weight:700;fill:#E6EDF3}}.label{{font-size:29px;fill:#9AA8B8}}.foot{{font-size:19px;fill:#7E9BBF}}</style></defs>
<rect x="8" y="8" width="884" height="284" rx="18" fill="#171B22" stroke="#526B8A" stroke-width="2"/>
<text x="52" y="68" class="eyebrow">CODEFORCES</text>
<text x="52" y="176" class="number">{count:,}</text>
<text x="52" y="222" class="label">Problems Solved</text>
<text x="52" y="260" class="foot">Rihanah_101_r · Live API count</text>
</svg>'''
 
def main():
    submissions = fetch_submissions()
    daily, stats = collect_stats(submissions)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(svg_card(daily, stats), encoding="utf-8")
    COUNT_OUTPUT.write_text(problems_count_card(stats["all_time"]), encoding="utf-8")
    print("Codeforces profile card updated:", stats)

if __name__ == "__main__":
    main()
