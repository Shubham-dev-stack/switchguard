import subprocess
import os
from typing import Dict, Any, List, Optional

class GitBlameInspector:
    """
    Inspects git commit history and blame metadata to correlate stack traces with recent deployments.
    """

    def __init__(self, repo_root: str):
        self.repo_root = repo_root

    def get_recent_commits(self, file_path: str, max_count: int = 5) -> List[Dict[str, str]]:
        if not os.path.exists(self.repo_root):
            return []

        try:
            cmd = ["git", "log", f"-n{max_count}", "--pretty=format:%h|%an|%s|%cI", "--", file_path]
            res = subprocess.run(cmd, cwd=self.repo_root, capture_output=True, text=True, check=True)
            commits = []
            for line in res.stdout.strip().split("\n"):
                if not line.strip():
                    continue
                parts = line.split("|")
                if len(parts) == 4:
                    commits.append({
                        "commit_hash": parts[0],
                        "author": parts[1],
                        "message": parts[2],
                        "timestamp": parts[3]
                    })
            return commits
        except Exception:
            return []
