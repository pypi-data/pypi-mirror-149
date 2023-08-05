import re


HEADER_PROCESS_TIME = "x-process-time"
UNDERSCORE_RE = re.compile(r"([^\-_\s])[\-_\s]+([^\-_\s])")
