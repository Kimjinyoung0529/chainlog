"""chainlog: append-only JSONL log where each entry carries the SHA-256 of the previous one.
Editing, deleting or reordering any line breaks the chain and is detected by verify()."""
import hashlib, json, sys, time

GENESIS = "0" * 64

def _digest(prev, ts, data):
    body = json.dumps({"prev": prev, "ts": ts, "data": data}, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    return hashlib.sha256(body.encode("utf-8")).hexdigest()

def _last_hash(path):
    last = GENESIS
    try:
        with open(path, encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    last = json.loads(line)["hash"]
    except FileNotFoundError:
        pass
    return last

def append(path, data, ts=None):
    ts = time.time() if ts is None else ts
    prev = _last_hash(path)
    entry = {"prev": prev, "ts": ts, "data": data, "hash": _digest(prev, ts, data)}
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    return entry

def verify(path):
    """Return (ok, n_entries, first_bad_line_or_None)."""
    prev, n = GENESIS, 0
    with open(path, encoding="utf-8") as f:
        for i, line in enumerate(f, 1):
            if not line.strip():
                continue
            try:
                e = json.loads(line)
                good = e["prev"] == prev and e["hash"] == _digest(e["prev"], e["ts"], e["data"])
            except (ValueError, KeyError):
                good = False
            if not good:
                return False, n, i
            prev, n = e["hash"], n + 1
    return True, n, None

def main(argv=None):
    a = sys.argv[1:] if argv is None else argv
    if len(a) >= 3 and a[0] == "append":
        try:
            data = json.loads(a[2])
        except ValueError:
            data = a[2]
        print(append(a[1], data)["hash"]); return 0
    if len(a) == 2 and a[0] == "verify":
        ok, n, bad = verify(a[1])
        print(f"OK {n} entries" if ok else f"TAMPERED at line {bad} (after {n} good entries)")
        return 0 if ok else 1
    print("usage: chainlog.py append FILE JSON | verify FILE", file=sys.stderr); return 2

if __name__ == "__main__":
    sys.exit(main())
