from src.Node import Node


class Street:
    def __init__(self, name, start: Node, end: Node, L, simulation_time):
        self.name = name
        self.start = start
        self.end = end
        start.add_outgoing_street(self)
        end.add_incoming_street(self)
        self.L = L
        self.light = Light(self, simulation_time=simulation_time)

    # def check_lights(self):
    #     greens = [l.state for l in self.lights]
    #     return greens <= 1


class Light:
    def __init__(self, street, simulation_time, state=0):
        self.state = state
        self.street = street
        self.queue = []

    def is_red(self, current_time):
        # return self.state == 0
        return not self.is_green(current_time)

    def is_green(self, current_time):
        # return self.state == 1
        return self.green_times[current_time % len(self.green_times)]

    def add_to_queue(self, car):
        self.queue.append(car)

    def set_cycle(self, one_cycle_time, green_start, weight):
        self.one_cycle_time = one_cycle_time
        self.green_times = [green_start <= i < green_start + weight for i in range(one_cycle_time)]

    def release_car(self, current_time):
        car = None
        if self.is_green(current_time) and len(self.queue)>0:
            car = self.queue[0]
            if not car.moved[current_time]:
                car.move_to_next_street(current_time)
                self.queue.remove(car)
        return car
