import argparse
import json
import time

from . import core


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="devvault",
        description="Compact developer conversion and inspection toolbox.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    encode_parser = subparsers.add_parser("b64encode", help="Encode UTF-8 text as Base64")
    encode_parser.add_argument("value")

    decode_parser = subparsers.add_parser("b64decode", help="Decode Base64 into UTF-8 text")
    decode_parser.add_argument("value")

    hash_parser = subparsers.add_parser("hash", help="Hash text")
    hash_parser.add_argument("value")
    hash_parser.add_argument(
        "-a",
        "--algorithm",
        default="sha256",
        choices=sorted(core.SUPPORTED_HASHES),
    )

    json_parser = subparsers.add_parser("json", help="Pretty-print JSON")
    json_parser.add_argument("value")

    jwt_parser = subparsers.add_parser("jwt", help="Inspect a JWT without verifying it")
    jwt_parser.add_argument("value")

    subparsers.add_parser("uuid", help="Generate a UUID v4")

    timestamp_parser = subparsers.add_parser("timestamp", help="Work with UTC timestamps")
    timestamp_parser.add_argument("value", nargs="?")
    timestamp_parser.add_argument(
        "--from-iso",
        action="store_true",
        help="Convert an ISO-8601 value to Unix time",
    )

    return parser


def main() -> None:
    args = build_parser().parse_args()

    try:
        if args.command == "b64encode":
            print(core.b64encode(args.value))
        elif args.command == "b64decode":
            print(core.b64decode(args.value))
        elif args.command == "hash":
            print(core.hash_text(args.value, args.algorithm))
        elif args.command == "json":
            print(core.pretty_json(args.value))
        elif args.command == "jwt":
            print(json.dumps(core.decode_jwt(args.value), indent=2))
        elif args.command == "uuid":
            print(core.uuid4())
        elif args.command == "timestamp":
            if args.from_iso:
                if args.value is None:
                    raise ValueError("timestamp --from-iso requires a value")
                print(core.iso_to_unix(args.value))
            elif args.value is None:
                print(int(time.time()))
            else:
                print(core.unix_to_iso(float(args.value)))
    except ValueError as exc:
        raise SystemExit(f"error: {exc}") from exc


if __name__ == "__main__":
    main()
