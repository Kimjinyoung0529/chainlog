# chainlog

해시 사슬로 엮어 변조를 감지하는 로그 라이브러리 (뼈대 단계) · A tiny hash-chained, tamper-evident log library (skeleton stage).

## 한국어
각 줄(JSONL)에 바로 앞 항목의 SHA-256을 넣어 사슬을 만들어요. 줄을 고치거나, 지우거나, 순서를 바꾸면 `verify`가 몇 번째 줄에서 끊겼는지 알려줘요. 표준 라이브러리만 써요.

```bash
python chainlog.py append app.log.jsonl '{"event":"login","user":"jin"}'
python chainlog.py verify app.log.jsonl   # OK 1 entries / TAMPERED at line N
```

**한계(솔직하게):** 서명이나 외부 앵커가 없어서, 파일 전체를 다시 계산해 통째로 바꾸는 공격이나 마지막 줄들을 잘라내는 것은 막지 못해요. 마지막 해시를 따로 보관하면 잘라내기를 알아챌 수 있어요. 성능 수치는 아직 재지 않았어요.

## English
Each JSONL entry stores the SHA-256 of the previous entry. Editing, deleting, or reordering lines makes `verify` report the first broken line. Stdlib only.

**Limitations:** no signatures or external anchoring, so an attacker who rewrites the whole file, or truncates the tail, is not detected unless you keep the latest hash elsewhere. No benchmarks yet.

Tests: `python -m unittest discover -s tests` · License: Apache-2.0 · AETHERION 팀
