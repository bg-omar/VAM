import os
import re
import sys
import pathlib
import requests
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup

TARGET_EXTS = {".fseries", ".short", ".scad", ".stl", ".jpeg", ".jpg", ".png"}
TIMEOUT = 20

def same_dir_or_below(url, base_dir_url):
    u, b = urlparse(url), urlparse(base_dir_url)
    return (u.netloc == b.netloc) and u.path.startswith(b.path)

def page_stem(url):
    name = pathlib.PurePosixPath(urlparse(url).path).name
    stem = os.path.splitext(name)[0]
    return stem or "index"

def fetch_soup(session, url):
    r = session.get(url, timeout=TIMEOUT)
    r.raise_for_status()
    return BeautifulSoup(r.text, "html.parser")

def download(session, file_url, dest_path):
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    if dest_path.exists():
        return
    with session.get(file_url, stream=True, timeout=TIMEOUT) as r:
        r.raise_for_status()
        with open(dest_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=1 << 15):
                if chunk:
                    f.write(chunk)

def crawl(parent_url="https://david.fremlin.de/knots/index.htm", out_root="downloads"):
    session = requests.Session()
    session.headers.update({"User-Agent": "knots-downloader/1.0"})
    base_dir = parent_url if parent_url.endswith("/") else parent_url.rsplit("/", 1)[0] + "/"

    visited_pages = set()
    to_visit = [parent_url]
    downloaded = set()

    while to_visit:
        url = to_visit.pop(0)
        if url in visited_pages:
            continue
        visited_pages.add(url)

        try:
            soup = fetch_soup(session, url)
        except Exception as e:
            print(f"[WARN] Could not fetch {url}: {e}")
            continue

        stem = page_stem(url)
        # collect downloadable file links
        for a in soup.find_all("a", href=True):
            href = a["href"].strip()
            full = urljoin(url, href)
            ext = os.path.splitext(urlparse(full).path)[1].lower()
            if ext in TARGET_EXTS and same_dir_or_below(full, base_dir):
                if full in downloaded:
                    continue
                filename = os.path.basename(urlparse(full).path)
                # put into a folder matching the owning page
                dest = pathlib.Path(out_root) / stem / filename
                try:
                    print(f"[GET] {full} -> {dest}")
                    download(session, full, dest)
                    downloaded.add(full)
                except Exception as e:
                    print(f"[WARN] Could not download {full}: {e}")

        # enqueue child knot pages (.htm) within the same directory tree
        for a in soup.find_all("a", href=True):
            href = a["href"].strip()
            if not href.lower().endswith(".htm"):
                continue
            full = urljoin(url, href)
            if same_dir_or_below(full, base_dir) and full not in visited_pages:
                to_visit.append(full)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python download_knots.py <PARENT_URL>")
        print("Example: python download_knots.py  https://david.fremlin.de/knots/index.htm")
        sys.exit(1)
    crawl(sys.argv[1])
