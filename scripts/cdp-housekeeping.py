#!/usr/bin/env python3
import json
import sys
import urllib.parse
import urllib.request


def fetch_json(url: str):
    with urllib.request.urlopen(url, timeout=10) as resp:
        return json.load(resp)


def request(url: str, method: str = "GET"):
    req = urllib.request.Request(url, method=method)
    with urllib.request.urlopen(req, timeout=10) as resp:
        data = resp.read().decode("utf-8", errors="replace")
        if not data:
            return None
        try:
            return json.loads(data)
        except Exception:
            return data


def main():
    if len(sys.argv) < 2 or sys.argv[1] != "cleanup":
        print("usage: cdp-housekeeping.py cleanup <port> [keep_blank=true|false]", file=sys.stderr)
        sys.exit(2)

    port = sys.argv[2] if len(sys.argv) >= 3 else "9223"
    keep_blank = (sys.argv[3].lower() if len(sys.argv) >= 4 else "true") == "true"
    base = f"http://127.0.0.1:{port}"

    tabs = fetch_json(f"{base}/json/list")
    page_tabs = [t for t in tabs if t.get("type") == "page"]

    keep_target = None
    if keep_blank:
        for tab in page_tabs:
            if tab.get("url") == "about:blank":
                keep_target = tab.get("id") or tab.get("targetId")
                break
        if not keep_target:
            created = request(f"{base}/json/new?{urllib.parse.quote('about:blank', safe='')}", method="PUT")
            if isinstance(created, dict):
                keep_target = created.get("id") or created.get("targetId")

    closed = []
    for tab in page_tabs:
        tid = tab.get("id") or tab.get("targetId")
        if not tid or tid == keep_target:
            continue
        request(f"{base}/json/close/{tid}")
        closed.append(tid)

    result = {
        "port": port,
        "keep_blank": keep_blank,
        "kept": keep_target,
        "closedCount": len(closed),
        "closed": closed,
    }
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
