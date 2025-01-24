import time

class Timer:
    def __init__(self):
        self.start_time = None
        self.end_time = None

    def start(self):
        """Start de timer."""
        self.start_time = time.time()

    def stop(self):
        """Stop de timer."""
        self.end_time = time.time()

    def elapsed_time(self):
        """Retourneer de verstreken tijd in seconden."""
        if self.start_time is None or self.end_time is None:
            raise ValueError("Timer is niet correct gestart of gestopt.")
        return self.end_time - self.start_time