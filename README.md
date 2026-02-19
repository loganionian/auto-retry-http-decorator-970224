# auto-retry-http-decorator

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A decorator library that automatically retries failed HTTP requests with exponential backoff and circuit breaker pattern. This is useful for improving the resilience of microservices in production.

## The Problem

Many developers face issues with flaky APIs that fail intermittently. Current workarounds often involve manual retries, which can clutter code and lead to inconsistent behavior. A library that automates retries with sensible defaults would greatly simplify error handling in HTTP requests.

## How It Works

This library will wrap around popular HTTP clients like requests or httpx, providing a simple decorator to apply retry logic. It will use exponential backoff to avoid hammering a failing service and a circuit breaker pattern to prevent cascading failures.

## Features

- Automatic retries with customizable parameters like max_attempts and delay.
- Circuit breaker support to prevent excessive load on failing services.
- Easy to use and integrate into existing codebases with a simple decorator.
- Detailed logging of retry attempts and eventual failures for easier debugging.

## Installation

```bash
pip install auto-retry-http-decorator
```

Or install from source:

```bash
git clone https://github.com/YOUR_USERNAME/auto-retry-http-decorator.git
cd auto-retry-http-decorator
pip install -e .
```

## Quick Start

```python
import requests
from auto_retry import retry

@retry(max_attempts=5, delay=2)
def fetch_data(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

data = fetch_data('https://api.example.com/data')
```

## Tech Stack

- Primary library/framework: requests for its simplicity and wide usage.
- Supporting library: tenacity for its powerful and flexible retry mechanisms.

## Contributing

Contributions are welcome! Please read our [Contributing Guide](CONTRIBUTING.md) for details.

## License

MIT License - see [LICENSE](LICENSE) for details.
