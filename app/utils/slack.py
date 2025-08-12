import os, json, urllib.request
def post_slack(text: str):
    url = os.getenv("SLACK_WEBHOOK_URL")
    if not url:
        print("[SLACK] (noop) " + text)
        return
    payload = {"text": text}
    req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers={"Content-Type":"application/json"})
    with urllib.request.urlopen(req) as resp:
        resp.read()
