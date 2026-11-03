#!/usr/bin/env python3
"""Fetch and verify the manifest-pinned Unicode 17.0.0 input files.

Only GitHub's API is used. Source bytes are written under the ignored
research/data/.cache/unicode17/ directory after all manifest identities
are checked. A compact verification log is written to research/data/.
"""
from __future__ import annotations

import base64
import hashlib
import json
import os
import sys
import tempfile
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "research/data/phase-01-source-manifest.json"
CACHE = ROOT / "research/data/.cache/unicode17"
LOG = ROOT / "research/data/phase-01-unicode-verification.json"
USER_AGENT = "ZEMA-Phase1-UnicodeVerifier/1.0"


def git_blob_sha1(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode("ascii") + b"\0" + data).hexdigest()


def fetch_blob(repo: str, blob_sha: str) -> bytes:
    url = f"https://api.github.com/repos/{repo}/git/blobs/{blob_sha}"
    request = urllib.request.Request(
        url,
        headers={"Accept": "application/vnd.github+json", "User-Agent": USER_AGENT},
    )
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            payload = json.load(response)
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"GitHub API fetch failed for {blob_sha}: {exc}") from exc
    if payload.get("encoding") != "base64" or "content" not in payload:
        raise RuntimeError(f"Unexpected GitHub blob response for {blob_sha}")
    try:
        return base64.b64decode(payload["content"], validate=False)
    except (ValueError, TypeError) as exc:
        raise RuntimeError(f"Invalid base64 for blob {blob_sha}: {exc}") from exc


def verify(source: dict, data: bytes) -> dict:
    expected_bytes = int(source["bytes"])
    actual_blob = git_blob_sha1(data)
    actual_sha256 = hashlib.sha256(data).hexdigest()
    problems = []
    if len(data) != expected_bytes:
        problems.append(f"bytes {len(data)} != {expected_bytes}")
    if actual_blob != source["git_blob_sha"]:
        problems.append(f"git blob {actual_blob} != {source['git_blob_sha']}")
    if actual_sha256 != source["sha256"]:
        problems.append(f"sha256 {actual_sha256} != {source['sha256']}")
    if problems:
        raise RuntimeError(f"{source['id']} verification failed: " + "; ".join(problems))
    return {
        "id": source["id"],
        "path": source["path"],
        "bytes": len(data),
        "git_blob_sha": actual_blob,
        "sha256": actual_sha256,
        "verified": True,
    }


def atomic_write(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=path.parent, delete=False) as handle:
        handle.write(data)
        temp_path = Path(handle.name)
    os.replace(temp_path, path)


def main() -> int:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    pinned_commit = "3ff0e2bb2ff8253831cb243d2d8e26a7f9534b1c"
    sources = [
        source for source in manifest["sources"]
        if source.get("version") == "Unicode 17.0.0"
    ]
    if len(sources) != 16:
        raise RuntimeError(f"Expected 16 pinned Unicode 17 inputs; manifest has {len(sources)}")
    if any(source.get("commit") != pinned_commit for source in sources):
        raise RuntimeError("Unicode 17 manifest inputs do not all use the pinned commit")

    verified = []
    pending = []
    for index, source in enumerate(sources, start=1):
        print(f"[{index}/{len(sources)}] fetching {source['id']} ...", flush=True)
        destination = CACHE / source["id"] / Path(source["path"]).name
        if destination.is_file():
            data = destination.read_bytes()
            try:
                result = verify(source, data)
                result["retrieved_now"] = False
                verified.append(result)
                print(f"  cache verified ({len(data)} bytes)", flush=True)
                continue
            except RuntimeError:
                print("  cached copy mismatched; refetching pinned blob", flush=True)
        data = fetch_blob(source["repo"], source["git_blob_sha"])
        result = verify(source, data)
        result["retrieved_now"] = True
        verified.append(result)
        pending.append((destination, data))
        print(f"  verified ({len(data)} bytes)", flush=True)

    # Write cache only after every input has passed all identity checks.
    for destination, data in pending:
        atomic_write(destination, data)

    log = {
        "verified_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "manifest": "research/data/phase-01-source-manifest.json",
        "repository": "unicode-org/unicodetools",
        "commit": pinned_commit,
        "source_count": len(verified),
        "all_verified": all(item["verified"] for item in verified),
        "cache_policy": "source bytes live only under ignored research/data/.cache/unicode17/",
        "files": verified,
    }
    atomic_write(LOG, (json.dumps(log, indent=2, ensure_ascii=False) + "\n").encode("utf-8"))
    print(f"PASS: {len(verified)} Unicode 17.0.0 inputs verified")
    print(f"Verification log: {LOG.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
