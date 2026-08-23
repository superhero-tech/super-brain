import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional


def find_config_dir() -> Path:
    """Finds or determines the script configuration directory."""
    return Path(__file__).resolve().parent


def find_config_file() -> Path:
    """Returns path to reel_config.json."""
    return find_config_dir() / "reel_config.json"


def find_env_file() -> Path:
    """Finds or determines the location of the .env file."""
    script_dir = Path(__file__).resolve().parent
    vault_root = script_dir.parents[2] if len(script_dir.parents) >= 3 else script_dir

    candidates = [
        Path.cwd() / ".env",
        script_dir / ".env",
        vault_root / ".env"
    ]
    for c in candidates:
        if c.exists():
            return c
    return script_dir / ".env"


def load_env():
    """Loads environment variables from .env if present."""
    env_file = find_env_file()
    if env_file.exists():
        try:
            with open(env_file, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#") or "=" not in line:
                        continue
                    key, val = line.split("=", 1)
                    key = key.strip()
                    val = val.strip().strip("\"'")
                    if key and key not in os.environ:
                        os.environ[key] = val
        except Exception:
            pass


def load_user_preferences() -> Dict[str, Any]:
    """Loads user preferences for content filtering and topics."""
    cfg_file = find_config_file()
    default_prefs = {
        "accepted_topics": [
            "technology & AI",
            "coding & development",
            "photography & camera recipes",
            "cooking & recipes",
            "fitness & workout techniques",
            "productivity & workflows",
            "business & marketing",
            "design & architecture",
            "books & summaries",
            "educational tutorials & how-to"
        ],
        "rejected_topics": [
            "personal selfies & friend vacations",
            "fashion/lingerie modeling poses without actionable guides",
            "pure music/party/festival video clips without substance",
            "general memes and shitposts without educational value"
        ],
        "custom_instructions": ""
    }
    if cfg_file.exists():
        try:
            data = json.loads(cfg_file.read_text(encoding="utf-8"))
            default_prefs.update(data)
        except Exception:
            pass
    return default_prefs


def save_user_preferences(prefs: Dict[str, Any]):
    """Saves user preferences to reel_config.json."""
    cfg_file = find_config_file()
    cfg_file.write_text(json.dumps(prefs, indent=2, ensure_ascii=False), encoding="utf-8")


def get_gemini_api_key(interactive: bool = True) -> Optional[str]:
    """Retrieves GEMINI_API_KEY, prompting the user if interactive and missing."""
    load_env()
    key = os.environ.get("GEMINI_API_KEY")
    if key and key.strip():
        return key.strip()

    if not interactive:
        return None

    print("\n" + "=" * 60)
    print("🔑 GEMINI API KEY SETUP")
    print("=" * 60)
    print("No GEMINI_API_KEY found in the environment or .env file.")
    print("A Gemini API key is required for video, audio, and OCR analysis.")
    print("You can generate a free key in 30 seconds here:")
    print("👉 https://aistudio.google.com/app/apikey\n")

    try:
        user_key = input("Paste your GEMINI_API_KEY (or press Enter to cancel): ").strip()
    except (EOFError, KeyboardInterrupt):
        return None

    if not user_key:
        return None

    env_file = find_env_file()
    try:
        env_lines = []
        if env_file.exists():
            env_lines = env_file.read_text(encoding="utf-8").splitlines()
        
        updated = False
        new_lines = []
        for line in env_lines:
            if line.strip().startswith("GEMINI_API_KEY="):
                new_lines.append(f"GEMINI_API_KEY={user_key}")
                updated = True
            else:
                new_lines.append(line)
        if not updated:
            new_lines.append(f"GEMINI_API_KEY={user_key}")

        env_file.write_text("\n".join(new_lines) + "\n", encoding="utf-8")
        os.environ["GEMINI_API_KEY"] = user_key
        print(f"✅ Saved API key securely to: {env_file.resolve()}\n")
        return user_key
    except Exception as e:
        print(f"⚠️ Warning: Could not write to .env: {e}")
        os.environ["GEMINI_API_KEY"] = user_key
        return user_key
