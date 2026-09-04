import unittest

from devvault.core import (
    b64decode,
    b64encode,
    decode_jwt,
    hash_text,
    iso_to_unix,
    pretty_json,
    unix_to_iso,
)


class DevVaultTests(unittest.TestCase):
    def test_base64_round_trip(self):
        self.assertEqual(b64decode(b64encode("medu")), "medu")

    def test_invalid_base64_is_rejected(self):
        with self.assertRaises(ValueError):
            b64decode("%%%")

    def test_hash_is_deterministic(self):
        self.assertEqual(hash_text("hello"), hash_text("hello"))
        self.assertEqual(len(hash_text("hello")), 64)

    def test_json_is_sorted_and_pretty(self):
        output = pretty_json('{"b":1,"a":2}')
        self.assertLess(output.index('"a"'), output.index('"b"'))
        self.assertIn("\n", output)

    def test_timestamp_round_trip(self):
        self.assertEqual(iso_to_unix(unix_to_iso(0)), 0)

    def test_jwt_decode_is_explicitly_unverified(self):
        token = "eyJhbGciOiJub25lIn0.eyJzdWIiOiIxIn0."
        decoded = decode_jwt(token)
        self.assertEqual(decoded["payload"]["sub"], "1")
        self.assertFalse(decoded["verified"])


if __name__ == "__main__":
    unittest.main()
