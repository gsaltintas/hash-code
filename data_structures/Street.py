from data_structures.Node import Node


class Street:
    def __init__(self, name, start: Node, end: Node, L):
        self.name = name
        self.start = start
        self.end = end
        start.add_outgoing_street(self)
        end.add_incoming_street(self)
        self.L = L
        self.light = Light(self)

    # def check_lights(self):
    #     greens = [l.state for l in self.lights]
    #     return greens <= 1


class Light:
    def __init__(self, street, state=0):
        self.state = state
        self.street = street
        self.queue = []

    def is_red(self):
        return self.state == 0

    def is_green(self):
        return self.state == 1

    def add_to_queue(self, car):
        self.queue.append(car)

    def release_car(self, current_time):
        car = None
        if self.is_green():
            car = self.cars[0]
            if not car.moved[current_time]:
                car.move_to_next_street(current_time)
                self.queue.remove(car)
        return car
