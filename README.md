# DevVault

DevVault puts a set of small developer utilities behind one predictable command. It is meant for the repetitive transformations that usually send you searching for a website or opening a Python shell.

## Tools

* Base64 encode and decode
* Text hashing with common algorithms
* JSON formatting and key sorting
* UUID v4 generation
* Unix timestamp conversion
* JWT header and payload inspection without signature verification

## Install

```bash
git clone https://github.com/meduuv/devvault.git
cd devvault
pip install -e .
```

## Examples

```bash
devvault b64encode "hello world"
devvault hash "hello world"
devvault json '{"online":true,"port":8080}'
devvault uuid
devvault timestamp 0
devvault jwt "header.payload.signature"
```

JWT inspection only decodes the visible header and payload. It does not validate signatures and should not be used as an authentication decision.

## Development

```bash
python -m unittest discover -s tests -v
```

## Credits

Built by [meduuv](https://guns.lol/meduu).

## License

MIT
