import re
from pathlib import Path

def home_path(log_path):
    home = re.compile("^~")
    log_path = str(log_path)
    if home.search(log_path):
        home_path = str(Path(".").home())
        log_path = log_path.replace("~", home_path)
    return log_path
