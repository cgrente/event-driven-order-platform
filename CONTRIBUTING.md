# Contributing

Thanks for taking the time to contribute.

This repository is intentionally small, so the contribution model is also intentionally simple.

## Goals for contributions

Changes should keep the project:

- easy to run locally
- easy to understand quickly
- focused on event-driven architecture fundamentals
- clean enough to be used as a portfolio / interview discussion repo

## Development workflow

1. Create a virtual environment
2. Install dependencies
3. Start Kafka with Docker Compose
4. Create the required topics
5. Run consumer and producer locally
6. Validate that documentation still matches actual behavior

## Local setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r services/order_service/requirements.txt
pip install -r services/tracker_service/requirements.txt
make up
make topics
```

### Style guidelines

Python
- prefer small, focused functions
- prefer explicit names over short names
- keep configuration in environment variables where practical
- comments should explain intent, tradeoffs, or non-obvious behavior
- avoid noisy comments that simply restate the code

Docker / Compose
- keep Docker Compose readable
- use comments only where Kafka networking or local development behavior is non-obvious
- prefer stable, local-dev-friendly defaults

Documentation
- update README.md when setup or commands change
- update docs/architecture.md when service responsibilities or event flow changes
- update schemas/ if the message payload changes

What not to commit

Do not commit:
- .venv/
- .idea/
- local editor files
- generated cache directories
- machine-specific secrets

Commit message guidance

Prefer messages like:
- add tracker consumer service
- document dual-listener kafka setup
- add JSON schema for order-created event

Avoid vague messages like:
- fix stuff
- update files
- changes

Pull requests

A good pull request should explain:
- what changed
- why it changed
- how it was tested locally
- whether documentation was updated