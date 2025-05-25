from datetime import datetime

def parse_srt_timestamp(ts: str) -> datetime:
    """Parse an SRT timestamp string into a datetime object."""
    return datetime.strptime(ts, "%H:%M:%S,%f")
