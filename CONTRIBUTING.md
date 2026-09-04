# Contributing

Contributions are welcome when they improve correctness, portability, documentation or test coverage.

## Local setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
python -m unittest discover -s tests -v
```

On Windows, activate the environment with `.venv\Scripts\activate`.

## Pull requests

Keep utilities predictable and focused. Add tests for parsing, validation and edge cases whenever behavior changes. Avoid hidden network calls or surprising side effects.

JWT support must remain inspection-only unless cryptographic verification is implemented explicitly and safely.

## Credits

Project identity and examples are maintained by [meduuv](https://guns.lol/meduu).
