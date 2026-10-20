import sys, hashlib, json
from bs4 import BeautifulSoup

def main():
    path = sys.argv[1]
    mode = sys.argv[2]  # text, links, both
    with open(path, "rb") as f:
        raw = f.read()
    soup = BeautifulSoup(raw, "html.parser")
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()
    if mode in ("text", "both"):
        txt = soup.get_text("\n")
        txt = "\n".join(line.strip() for line in txt.splitlines() if line.strip())
        with open(path.replace("-original.html", "-extracted.txt"), "w", encoding="utf-8") as f:
            f.write(txt)
        print("SAVED_TEXT", path.replace("-original.html", "-extracted.txt"))
    if mode in ("links", "both"):
        out = []
        for a in soup.find_all("a", href=True):
            out.append({"text": " ".join(a.get_text(" ", strip=True).split()), "href": a["href"]})
        with open(path.replace("-original.html", "-links.json"), "w", encoding="utf-8") as f:
            json.dump(out, f, indent=2, ensure_ascii=False)
        print("SAVED_LINKS", path.replace("-original.html", "-links.json"))

if __name__ == "__main__":
    main()
