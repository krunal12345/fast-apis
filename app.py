import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "apis" / "ipl-apis"))

from main import app as app  # noqa: F401
