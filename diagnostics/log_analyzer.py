import re
from typing import Dict, List, Any, Optional

PII_PATTERNS = [
    (r"bearer\s+[A-Za-z0-9\-_\.]+", "Bearer [REDACTED_TOKEN]"),
    (r"password\s*[:=]\s*['\"][^'\"]+['\"]", "password: \"[REDACTED_SECRET]\""),
    (r"\b(?:\d{4}-){3}\d{4}\b", "[REDACTED_CARD_NUMBER]"),
    (r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", "[REDACTED_EMAIL]")
]

class LogAnalyzer:
    """
    Parses application logs, scrubs sensitive PII/secrets, and extracts structured error signatures.
    """

    @classmethod
    def redact_pii(cls, raw_text: str) -> str:
        scrubbed = raw_text
        for pattern, replacement in PII_PATTERNS:
            scrubbed = re.sub(pattern, replacement, scrubbed, flags=re.IGNORECASE)
        return scrubbed

    @classmethod
    def extract_error_signature(cls, stack_trace: str) -> Dict[str, Any]:
        """
        Parses python/standard traceback to extract failing file, line, and exception class.
        """
        clean_trace = cls.redact_pii(stack_trace)
        
        # Look for pattern: File "...", line 123, in func
        file_line_matches = re.findall(r'File\s+["\']([^"\']+)["\'],\s+line\s+(\d+),\s+in\s+([a-zA-Z0-9_]+)', clean_trace)
        
        # Look for trailing exception line: ExceptionName: reason
        exception_match = re.search(r'([A-Za-z0-9_]+Error|[A-Za-z0-9_]+Exception):\s*(.*)', clean_trace)

        failing_frame = None
        if file_line_matches:
            last_file, last_line, last_func = file_line_matches[-1]
            failing_frame = {
                "file": last_file,
                "line": int(last_line),
                "function": last_func
            }

        exception_type = exception_match.group(1) if exception_match else "UnknownError"
        exception_msg = exception_match.group(2).strip() if exception_match else ""

        return {
            "exception_type": exception_type,
            "exception_message": exception_msg,
            "failing_frame": failing_frame,
            "frame_depth": len(file_line_matches),
            "sanitized_trace": clean_trace
        }
