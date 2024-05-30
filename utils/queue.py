import config


class Queue:
    def __init__(self, trip_duration=10):
        self.amount_of_people = 0
        self.waiting_time = 0
        self.delay_amount = 0
        self.trip_duration = trip_duration
        self.truck_amount = 1

    def update_queue(self, change):
        """Remove or add someone from the queue."""

        self.amount_of_people += change
        self.update_waiting_time()

    def update_truck_amount(self, update):
        self.truck_amount = update

    def update_waiting_time(self):
        """Change the waiting time in the queue."""


        if self.amount_of_people <= config.capacity_truck:
            self.waiting_time = 5

        else:
            people_per_min = config.capacity_truck / self.trip_duration
            people_per_min = people_per_min * self.truck_amount
            queue_time = self.amount_of_people / people_per_min
            self.waiting_time = int(queue_time)

    def add_delay(self, delay=10):
        """Add a delay to the queue measured in minutes, by default the delay is 10 minutes."""

        self.delay_amount += delay * 60

    def reset_delay(self):
        """Reset the delay"""

        self.waiting_time = 0

    def get_waiting_time(self):
        self.update_waiting_time()
        return f"Waiting time is: {self.waiting_time} minutes."
