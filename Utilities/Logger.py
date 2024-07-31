from Utilities.Date import get_date
import os

class Logger:
    def __init__(self) -> None:
        self.logDir = "Logs"
        os.makedirs(self.logDir, exist_ok=True)
    
    def logLine(self, message, logFile):
        line = f"[{get_date(add_minutes=True)}]]: {message}\n"
        with open(os.path.join(self.logDir, logFile), "a", encoding="utf-8") as f:
            f.write(line)