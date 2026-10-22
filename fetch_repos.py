"""GitHub'dan yapay zeka + yatirim/trading repolarini toplar ve skorlar -> repos.json"""
import json, subprocess, math
from datetime import datetime, timezone

QUERIES = [
    "topic:algorithmic-trading",
    "topic:trading-bot",
    "topic:quantitative-finance",
    "topic:reinforcement-learning topic:trading",
    "topic:stock-prediction",
    "llm trading agents in:name,description",
    "ai hedge fund in:name,description",
]
FIN_WORDS = ["trading", "trader", "stock", "invest", "quant", "hedge", "portfolio", "finance", "financial", "backtest", "forex", "crypto"]
AI_WORDS = ["ai", "llm", "gpt", "reinforcement", "deep learning", "neural", "machine learning", "agent", "rl", "lstm", "transformer"]


def gh(path):
    out = subprocess.run(["gh", "api", path], capture_output=True, text=True, encoding="utf-8")
    if out.returncode:
        raise RuntimeError(out.stderr)
    return json.loads(out.stdout)


def main():
    seen = {}
    for q in QUERIES:
        qs = q.replace(" ", "+").replace(":", "%3A")
        data = gh(f"search/repositories?q={qs}+stars%3A%3E300+archived%3Afalse&sort=stars&per_page=30")
        for r in data["items"]:
            seen[r["full_name"]] = r
    now = datetime.now(timezone.utc)
    rows = []
    for r in seen.values():
        text = " ".join([r["name"], r.get("description") or "", " ".join(r.get("topics", []))]).lower()
        if not any(w in text for w in FIN_WORDS) or r["name"].startswith("awesome") or "awesome-" in r["name"]:
            continue
        ai = any(w in text.split() or w in text for w in AI_WORDS)
        pushed = datetime.fromisoformat(r["pushed_at"].replace("Z", "+00:00"))
        days = (now - pushed).days
        created = datetime.fromisoformat(r["created_at"].replace("Z", "+00:00"))
        age_y = max((now - created).days / 365, 0.3)
        # skor: popularite (log), tazelik, yillik buyume, issue yuku
        pop = min(math.log10(r["stargazers_count"] + 1) / 5, 1) * 40
        fresh = max(0, 1 - days / 365) * 30
        growth = min(r["stargazers_count"] / age_y / 3000, 1) * 20
        health = (10 if r["open_issues_count"] < 0.05 * r["stargazers_count"] else 4) + (0 if r.get("license") else -3)
        rows.append({
            "name": r["full_name"], "url": r["html_url"], "desc": r.get("description") or "",
            "stars": r["stargazers_count"], "forks": r["forks_count"], "issues": r["open_issues_count"],
            "lang": r.get("language"), "license": (r.get("license") or {}).get("spdx_id"),
            "pushed_days": days, "ai": ai, "topics": r.get("topics", [])[:6],
            "score": round(pop + fresh + growth + health, 1),
        })
    rows.sort(key=lambda x: -x["score"])
    json.dump({"generated": now.isoformat(), "repos": rows[:60]}, open("repos.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(len(rows), "repo,", sum(r["ai"] for r in rows), "AI etiketli")
    for r in rows[:10]:
        print(r["score"], r["name"], r["stars"])


main()
