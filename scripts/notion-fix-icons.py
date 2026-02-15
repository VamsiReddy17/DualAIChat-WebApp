"""Fix missing Notion icons by using reliable emoji icons instead of external URLs."""
import json, os, time, urllib.request, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

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

def set_emoji(page_id, emoji):
    api("PATCH", f"https://api.notion.com/v1/pages/{page_id}", {
        "icon": {"type": "emoji", "emoji": emoji}
    })

# Get all subpages
resp = api("GET", f"https://api.notion.com/v1/blocks/{PARENT}/children?page_size=50", None)
subpages = [(b["id"], b["child_page"]["title"]) for b in resp["results"] if b["type"] == "child_page"]

# Emoji mapping for subpages (reliable, always renders)
PAGE_EMOJI = {
    "Tech Stack":     "\u2699\uFE0F",    # gear
    "Architecture":   "\U0001F3D7\uFE0F", # building construction
    "Backend":        "\u26A1",           # lightning
    "Frontend":       "\U0001F3A8",       # palette
    "AI Models":      "\U0001F9E0",       # brain
    "DevOps":         "\U0001F433",       # whale (docker)
    "API Reference":  "\U0001F4E1",       # satellite
    "Phase 1":        "\u2705",           # green check
    "Phase 2":        "\U0001F680",       # rocket
}

# Sub-subpage emoji mapping
SUB_EMOJI = {
    "Python & FastAPI":    "\U0001F40D",  # snake
    "React & TypeScript":  "\u269B\uFE0F", # atom
    "Tailwind":            "\U0001F3A8",  # palette
    "SSE Streaming":       "\u26A1",      # lightning
    "Error Handling":      "\U0001F6E1\uFE0F", # shield
    "LLM Services":        "\U0001F916",  # robot
    "Configuration":       "\U0001F511",  # key
    "Middleware":           "\U0001F4DD",  # memo
    "useChat Hook":        "\U0001FA9D",  # hook
    "Component":           "\U0001F9E9",  # puzzle
    "GPT-4o":              "\u2728",      # sparkles
    "DeepSeek":            "\U0001F9E0",  # brain
    "Docker":              "\U0001F4E6",  # package
    "CI/CD":               "\U0001F504",  # cycle arrows
    "Chat Completions":    "\U0001F4AC",  # speech bubble
    "Streaming Endpoint":  "\U0001F4A8",  # dash/wind
}

print("Updating main page icon...")
set_emoji(PARENT, "\U0001F916")  # robot face
print("  [OK] Main page")

print("\nUpdating subpage icons...")
for pid, title in subpages:
    for key, emoji in PAGE_EMOJI.items():
        if key.lower() in title.lower():
            set_emoji(pid, emoji)
            print(f"  [OK] {emoji} {title}")
            break

print("\nUpdating sub-subpage icons...")
for pid, title in subpages:
    try:
        children = api("GET", f"https://api.notion.com/v1/blocks/{pid}/children?page_size=50", None)
        sub_sub = [(b["id"], b["child_page"]["title"]) for b in children["results"] if b["type"] == "child_page"]
        for spid, stitle in sub_sub:
            for key, emoji in SUB_EMOJI.items():
                if key.lower() in stitle.lower():
                    set_emoji(spid, emoji)
                    print(f"  [OK] {emoji} {stitle}")
                    break
    except Exception as e:
        print(f"  [ERR] {title}: {e}")

print("\n" + "=" * 40)
print("ALL ICONS FIXED!")
print("=" * 40)
