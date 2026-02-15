"""Update Notion page icons and cover images for a polished, branded look."""
import json, os, time, urllib.request

TOKEN = os.environ.get("NOTION_TOKEN", "")
HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json",
}
PARENT = "3086efb9-58c3-8036-a0a2-f772f5e59158"

def api(method, url, body=None):
    data = json.dumps(body).encode() if body else None
    req = urllib.request.Request(url, data=data, headers=HEADERS, method=method)
    time.sleep(0.35)
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())

# ── 1. Main page already updated (icon + cover) ───────────
print("[1/4] Main page icon & cover already set.")

# ── 2. Get all subpages ────────────────────────────────────
print("\n[2/3] Fetching subpages...")
resp = api("GET", f"https://api.notion.com/v1/blocks/{PARENT}/children?page_size=50", None)
subpages = [(b["id"], b["child_page"]["title"]) for b in resp["results"] if b["type"] == "child_page"]

# Icon mapping for each subpage (more professional & distinct)
ICONS = {
    "Tech Stack":     "https://img.icons8.com/3d-fluency/94/artificial-intelligence.png",
    "Architecture":   "https://img.icons8.com/3d-fluency/94/mind-map.png",
    "Backend":        "https://img.icons8.com/3d-fluency/94/api-settings.png",
    "Frontend":       "https://img.icons8.com/3d-fluency/94/web-design.png",
    "AI Models":      "https://img.icons8.com/3d-fluency/94/brain.png",
    "DevOps":         "https://img.icons8.com/3d-fluency/94/docker.png",
    "API Reference":  "https://img.icons8.com/3d-fluency/94/code.png",
    "Phase 1":        "https://img.icons8.com/3d-fluency/94/checkmark.png",
    "Phase 2":        "https://img.icons8.com/3d-fluency/94/rocket.png",
}

# ── 3. Update each subpage icon ────────────────────────────
print("\n[3/3] Updating subpage icons...")
for pid, title in subpages:
    icon_url = None
    for key, url in ICONS.items():
        if key.lower() in title.lower():
            icon_url = url
            break

    if icon_url:
        api("PATCH", f"https://api.notion.com/v1/pages/{pid}", {
            "icon": {
                "type": "external",
                "external": {"url": icon_url}
            }
        })
        print(f"    [OK] {title}")
    else:
        print(f"    [-] {title} (kept existing)")

# ── 4. Now update sub-subpages too ─────────────────────────
print("\n[4/4] Updating sub-subpage icons...")
SUB_ICONS = {
    "Python & FastAPI":    "https://img.icons8.com/3d-fluency/94/python.png",
    "React & TypeScript":  "https://img.icons8.com/3d-fluency/94/react-native.png",
    "Tailwind":            "https://img.icons8.com/3d-fluency/94/paint-palette.png",
    "SSE Streaming":       "https://img.icons8.com/3d-fluency/94/lightning-bolt.png",
    "Error Handling":      "https://img.icons8.com/3d-fluency/94/shield.png",
    "LLM Services":       "https://img.icons8.com/3d-fluency/94/bot.png",
    "Configuration":       "https://img.icons8.com/3d-fluency/94/key.png",
    "Middleware":           "https://img.icons8.com/3d-fluency/94/cloud-sync.png",
    "useChat Hook":        "https://img.icons8.com/3d-fluency/94/webhook.png",
    "Component":           "https://img.icons8.com/3d-fluency/94/puzzle.png",
    "GPT-4o":              "https://img.icons8.com/3d-fluency/94/sparkling.png",
    "DeepSeek":            "https://img.icons8.com/3d-fluency/94/processor.png",
    "Docker":              "https://img.icons8.com/3d-fluency/94/docker.png",
    "CI/CD":               "https://img.icons8.com/3d-fluency/94/infinity.png",
    "Chat Completions":    "https://img.icons8.com/3d-fluency/94/chat.png",
    "Streaming Endpoint":  "https://img.icons8.com/3d-fluency/94/lightning-bolt.png",
}

for pid, title in subpages:
    try:
        children = api("GET", f"https://api.notion.com/v1/blocks/{pid}/children?page_size=50", None)
        sub_sub = [(b["id"], b["child_page"]["title"]) for b in children["results"] if b["type"] == "child_page"]
        for spid, stitle in sub_sub:
            icon_url = None
            for key, url in SUB_ICONS.items():
                if key.lower() in stitle.lower():
                    icon_url = url
                    break
            if icon_url:
                api("PATCH", f"https://api.notion.com/v1/pages/{spid}", {
                    "icon": {"type": "external", "external": {"url": icon_url}}
                })
                print(f"    [OK] {title} > {stitle}")
    except Exception as e:
        print(f"    [ERR] Error in {title}: {e}")

print("\n" + "=" * 50)
print("ALL ICONS UPDATED!")
print("=" * 50)
