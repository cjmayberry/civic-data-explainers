#!/usr/bin/env python3
"""
Model caller adapter for civic-data-pipeline.
Calls the Nous inference API (OpenAI-compatible) or OpenRouter as fallback.

NOTE: This script must be run with the environment sourced:
    set -a && source /opt/data/.env && set +a && python3 call_model.py
Or ensure /opt/data/.env is loaded before running.
"""

import os
import sys
import json
import urllib.request
import urllib.error

# Load API keys from environment. If the process wasn't launched with
# /opt/data/.env sourced (e.g. redraft.py importing this module directly),
# parse the file ourselves so the pipeline works however it's invoked.
_ENV_PATH = "/opt/data/.env"
if not (os.environ.get("OPENROUTER_API_KEY") or os.environ.get("NOUS_API_KEY")):
    try:
        with open(_ENV_PATH) as _f:
            for _line in _f:
                _line = _line.strip()
                if _line and not _line.startswith("#") and "=" in _line:
                    _k, _v = _line.split("=", 1)
                    os.environ.setdefault(_k.strip(), _v.strip().strip('"').strip("'"))
    except FileNotFoundError:
        pass

NOUS_API_KEY = os.environ.get("NOUS_API_KEY") or os.environ.get("NVIDIA_API_KEY")
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")

NOUS_BASE_URL = "https://inference-api.nousresearch.com/v1/chat/completions"
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1/chat/completions"

# Default model (Nous free tier, primary)
DEFAULT_MODEL = "upstage/solar-pro4:free"
# OpenRouter fallback — OpenRouter wants the bare slug, no :free suffix
OPENROUTER_MODEL = "upstage/solar-pro4"


def call_nous(messages, model=DEFAULT_MODEL, temperature=0.3, max_tokens=1000):
    """Call Nous inference API."""
    if not NOUS_API_KEY:
        return None, "NOUS_API_KEY not set"

    payload = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
    }

    req = urllib.request.Request(
        NOUS_BASE_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {NOUS_API_KEY}",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            result = json.loads(resp.read())
            return result["choices"][0]["message"]["content"], None
    except urllib.error.HTTPError as e:
        return None, f"Nous HTTP {e.code}: {e.read().decode()}"
    except Exception as e:
        return None, f"Nous error: {e}"


def call_openrouter(messages, model=OPENROUTER_MODEL, temperature=0.3, max_tokens=1000):
    """Call OpenRouter as fallback."""
    if not OPENROUTER_API_KEY:
        return None, "OPENROUTER_API_KEY not set"

    payload = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
    }

    req = urllib.request.Request(
        OPENROUTER_BASE_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "HTTP-Referer": "https://civic-data-pipeline.local",
            "X-Title": "Civic Data Pipeline",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            result = json.loads(resp.read())
            return result["choices"][0]["message"]["content"], None
    except urllib.error.HTTPError as e:
        return None, f"OpenRouter HTTP {e.code}: {e.read().decode()}"
    except Exception as e:
        return None, f"OpenRouter error: {e}"


def call_model(messages, model=None, temperature=0.3, max_tokens=1000, openrouter_model=None):
    """
    Main entry point. Tries Nous (upstage/solar-pro4:free) first,
    falls back to OpenRouter (upstage/solar-pro4:free) if Nous fails.
    Returns (content, error).
    """
    # Try Nous first
    content, error = call_nous(messages, model or DEFAULT_MODEL, temperature, max_tokens)
    if content is not None:
        return content, None

    print(f"Nous failed: {error}, trying OpenRouter fallback...", file=sys.stderr)
    content, error = call_openrouter(messages, openrouter_model or OPENROUTER_MODEL, temperature, max_tokens)
    if content is not None:
        return content, None

    return None, f"Both providers failed. Nous: {error}"


if __name__ == "__main__":
    # Simple test
    test_messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Say hello in one sentence."},
    ]
    content, error = call_model(test_messages)
    if content:
        print(content)
    else:
        print(f"Error: {error}", file=sys.stderr)
        sys.exit(1)
