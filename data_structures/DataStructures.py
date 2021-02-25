from data_structures.Node import Node


class City:
    def __init__(self, car_no, street_no, node_no, simulation_time):
        self.car_no = car_no
        self.street_no = street_no
        self.node_no = node_no
        self.simulation_time = simulation_time
        self.streets = {}
        self.nodes = []
        self.set_up()
        self.cars = []

    def set_up(self):
        for i in range(self.node_no):
            self.nodes.append(Node(i, self.simulation_time))

    def add_street(self, street):
        self.streets[street.name] = street

    def get_street(self, street_name):
        return self.streets[street_name]

    def add_car(self, car):
        self.cars.append(car)

    def report(self):
        # todo
        pass

    def simulate(self):
        for sec in range(self.simulation_time):
            self.simulate_one_sec(sec)

    def simulate_one_sec(self, current_time):
        self.check_lights(current_time)
        self.check_cars(current_time)

    def check_cars(self, current_time):
        """ checks cars, if they can move in the street moves them """
        for car in self.cars:
            if car.path_completed:
                continue
            light = car.current_street.light
            if car.to_node > 0:
                # move car 1 step
                car.move(current_time)
                # if car arrived at the light
                if car.to_node == 0:
                    light.add_to_queue(car)

    def check_lights(self, current_time):
        """ checks lights, releases the first car in the queue """
        for street in self.streets.values():
            light = street.light
            if light.is_green():
                light.release_car(current_time)
