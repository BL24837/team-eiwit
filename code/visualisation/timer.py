import time

class Timer:
    """
    A simple Timer class to measure elapsed time.
    """
    
    def __init__(self) -> None:
        """
        Initializes the Timer instance with start and end time as None.
        """
        self.start_time: float | None = None
        self.end_time: float | None = None

    def start(self) -> None:
        """
        Starts the timer.
        """
        self.start_time = time.time()

    def stop(self) -> None:
        """
        Stops the timer.
        """
        self.end_time = time.time()

    def elapsed_time(self) -> float:
        """
        Returns the elapsed time in seconds.
        
        Raises:
            ValueError: If the timer was not started or stopped properly.
        
        Returns:
            float: The elapsed time in seconds.
        """
        if self.start_time is None or self.end_time is None:
            raise ValueError("Timer has not been properly started or stopped.")
        return self.end_time - self.start_time
