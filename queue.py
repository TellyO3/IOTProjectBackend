import config


class Queue:
    def __init__(self):
        self.length = 0
        self.waiting_time = 0
        self.delay_amount = 0

    def modify_queue(self, change):
        """Remove or add someone from the queue."""

        self.length += change
        self.waiting_time += change * config.time_added_per_person

    def add_delay(self, delay=10):
        """Add a delay to the queue measured in minutes, by default the delay is 10 minutes."""

        self.delay_amount += delay * 60

    def reset_delay(self):
        """Reset the delay"""

        self.waiting_time = 0
