import os
import time
import requests

HANDLE = "Rihanah_101_r"
README_PATH = "README.md"
START = "<!-- CODEFORCES_STATS_START -->"
END = "<!-- CODEFORCES_STATS_END -->"
API = "https://codeforces.com/api/user.status"

def get_solved_count():
    solved = set()
    start = 1
    batch_size = 5000

    while True:
        response = requests.get(
            API,
            params={"handle": HANDLE, "from": start, "count": batch_size},
            timeout=30,
            headers={"User-Agent": "GitHub-Profile-Stats/1.0"},
        )
        response.raise_for_status()
        payload = response.json()
        if payload.get("status") != "OK":
            raise RuntimeError(payload.get("comment", "Codeforces API returned an error"))

        submissions = payload.get("result", [])
        for submission in submissions:
            if submission.get("verdict") == "OK":
                problem = submission.get("problem", {})
                contest_id = problem.get("contestId")
                index = problem.get("index")
                if contest_id is not None and index:
                    solved.add((contest_id, index))

        if len(submissions) < batch_size:
            break

        start += len(submissions)
        time.sleep(2)

    return len(solved)

def main():
    count = get_solved_count()
    with open(README_PATH, "r", encoding="utf-8") as file:
        content = file.read()

    start_index = content.find(START)
    end_index = content.find(END)
    if start_index == -1 or end_index == -1 or end_index < start_index:
        raise RuntimeError("Codeforces stats markers were not found in README.md")

    replacement = f"{START}\n**Problems Solved:** {count:,}\n{END}"
    end_index += len(END)
    content = content[:start_index] + replacement + content[end_index:]

    with open(README_PATH, "w", encoding="utf-8") as file:
        file.write(content)

    print(f"Updated Codeforces solved-problem count: {count}")

if __name__ == "__main__":
    main()
