import sys, hashlib, json, datetime
import httpx

UA = "Mozilla/5.0 (FlwuResearch; official-source review) AppleWebKit/537.36"

def main():
    url = sys.argv[1]
    out_path = sys.argv[2]
    t_start = datetime.datetime.now(datetime.timezone.utc)
    started_iso = t_start.isoformat()
    resp = httpx.get(url, follow_redirects=True, headers={"User-Agent": UA}, timeout=30.0)
    t_end = datetime.datetime.now(datetime.timezone.utc)
    retrieved_iso = t_end.isoformat()
    body = resp.content
    sha = hashlib.sha256(body).hexdigest()
    with open(out_path, "wb") as f:
        f.write(body)
    receipt = {
        "url": url,
        "resolved_url": str(resp.url),
        "http_status": resp.status_code,
        "content_type": resp.headers.get("content-type"),
        "request_started_at": started_iso,
        "retrieved_at": retrieved_iso,
        "sha256": sha,
        "bytes": len(body),
        "path": out_path,
    }
    print(json.dumps(receipt, indent=2))

if __name__ == "__main__":
    main()
