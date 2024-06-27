import config


class Queue:
    def __init__(self, trip_duration=10):
        self.amount_of_people = 0
        self.waiting_time = 0
        self.delay_amount = 0
        self.trip_duration = trip_duration
        self.truck_count = 1
        self.storing = False

    def update_queue(self, change):
        """Remove or add someone from the queue."""
        self.amount_of_people += change
        self.update_waiting_time()

    def update_truck_amount(self, update):
        if update > 0:
            self.truck_count = update
        self.update_waiting_time()

    def update_waiting_time(self):
        """Change the waiting time in the queue."""

        if self.amount_of_people <= config.capacity_truck:
            self.waiting_time = 5

        else:
            people_per_min = config.capacity_truck / self.trip_duration
            people_per_min = people_per_min * self.truck_count
            queue_time = self.amount_of_people / people_per_min
            actual_time = queue_time + self.delay_amount
            self.waiting_time = int(actual_time)

    def change_delay(self, delay=10):
        """Add a delay to the queue measured in minutes, by default the delay is 10 minutes."""

        self.delay_amount = delay
        self.update_waiting_time()

    def reset_delay(self):
        """Reset the delay"""

        self.delay_amount = 0

    def get_delay(self):
        return self.delay_amount

    def update_storing(self, status):
        if status == True:
            self.storing = True
        else:
            self.storing = False


    def get_waiting_time(self):
        self.update_waiting_time()
        if self.delay_amount == 0:
            return f"De huidige wachttijd is {self.waiting_time} minuten"
        else:
            return f"De huidige wachttijd is {self.waiting_time} minuten. \n Wegens oponthoud is er extra wachttijd van {self.delay_amount} minuten."

    def get_people_amount(self):
        return f"De huidige hoeveelheid wachtende is {self.amount_of_people}."
