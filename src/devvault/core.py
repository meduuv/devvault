from __future__ import annotations

import base64
import hashlib
import json
import uuid
from datetime import datetime, timezone

SUPPORTED_HASHES = {"md5", "sha1", "sha256", "sha512", "blake2b"}


def b64encode(text: str) -> str:
    return base64.b64encode(text.encode("utf-8")).decode("ascii")


def b64decode(text: str) -> str:
    try:
        decoded = base64.b64decode(text, validate=True)
    except Exception as exc:
        raise ValueError("invalid Base64 input") from exc
    try:
        return decoded.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("decoded data is not valid UTF-8") from exc


def hash_text(text: str, algorithm: str = "sha256") -> str:
    if algorithm not in SUPPORTED_HASHES:
        raise ValueError(f"unsupported hash algorithm: {algorithm}")
    hasher = hashlib.new(algorithm)
    hasher.update(text.encode("utf-8"))
    return hasher.hexdigest()


def pretty_json(text: str) -> str:
    try:
        value = json.loads(text)
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid JSON: {exc.msg}") from exc
    return json.dumps(value, indent=2, ensure_ascii=False, sort_keys=True)


def uuid4() -> str:
    return str(uuid.uuid4())


def unix_to_iso(value: float) -> str:
    return datetime.fromtimestamp(value, tz=timezone.utc).isoformat()


def iso_to_unix(value: str) -> int:
    normalized = value.strip().replace("Z", "+00:00")
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError as exc:
        raise ValueError("invalid ISO-8601 timestamp") from exc
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return int(parsed.timestamp())


def _decode_jwt_segment(segment: str) -> dict:
    padded = segment + "=" * ((4 - len(segment) % 4) % 4)
    try:
        raw = base64.urlsafe_b64decode(padded.encode("ascii"))
        value = json.loads(raw.decode("utf-8"))
    except Exception as exc:
        raise ValueError("invalid JWT segment") from exc
    if not isinstance(value, dict):
        raise ValueError("JWT segment must decode to a JSON object")
    return value


def decode_jwt(token: str) -> dict:
    parts = token.split(".")
    if len(parts) != 3:
        raise ValueError("JWT must contain exactly three segments")
    return {
        "header": _decode_jwt_segment(parts[0]),
        "payload": _decode_jwt_segment(parts[1]),
        "signature": parts[2],
        "verified": False,
    }
