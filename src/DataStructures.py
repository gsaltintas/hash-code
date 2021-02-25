from src.Node import Node
from math import log

from src.utils import gcd


class City:
    def __init__(self, car_no, street_no, node_no, simulation_time, score_coef):
        self.car_no = car_no
        self.street_no = street_no
        self.node_no = node_no
        self.simulation_time = simulation_time
        self.score_coef = score_coef
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

    def set_up_always_green_lights(self):
        for node in self.nodes:
            if len(node.incoming_streets) == 1:
                node.incoming_streets[0].light.state = 1

    def report(self):
        # todo
        txt = "%d\n" %self.node_no
        for i in range(self.node_no):
            node = self.nodes[i]
            node_traffic = sum(self.street_traffic[street] for street in node.incoming_streets)
            if node_traffic == 0:
                continue
            txt += "%d\n" % node.no
            txt += "%d\n" % len(node.incoming_streets)
            for street in node.cycle_weights:
                if node.cycle_weights[street] > 0:
                    txt += "%s %d\n" % (street.name, node.cycle_weights[street])
        return txt

    def get_car_traffic(self):
        """ counts total number of cars that will be passing through city's streets """
        street_traffic = {street: 0 for street in self.streets.values()}
        for car in self.cars:
            for street in car.path:
                street_traffic[street] += 1
        self.street_traffic = street_traffic
        return street_traffic

    def simulate(self):
        # set cycle
        # select time for each light
        # todo: select lights order
        self.setup_cycles()
        for sec in range(self.simulation_time):
            self.simulate_one_sec(sec)

    def setup_cycles(self):
        street_traffic = self.get_car_traffic()
        one_cycle_time = int(log(self.simulation_time, 2)) + 1
        for node in self.nodes:
            current_cycle_time = 0
            node_traffic = sum(street_traffic[street] for street in node.incoming_streets)
            if node_traffic == 0:
                for street in node.incoming_streets:
                    street.light.set_cycle(1, 0, 0)
                continue
            node_weights = {street: 0 for street in node.incoming_streets}
            # todo: may divide by street length
            for street in node.incoming_streets:
                node_weights[street] = int(street_traffic[street] / node_traffic * one_cycle_time)
            normalizer = gcd(list(node_weights.values()))
            if normalizer==0:
                normalizer=1
            node.one_cycle_time = int(sum(node_weights.values()) / normalizer)
            node.cycle_weights = node_weights
            for street in node.incoming_streets:
                weight = node_weights[street] / normalizer
                node_weights[street] = weight
                street.light.set_cycle(node.one_cycle_time, current_cycle_time, weight)
                current_cycle_time += weight

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
            if light.is_green(current_time):
                light.release_car(current_time)

    def score(self):
        s = sum([(self.simulation_time - car.finish_time) + self.score_coef for car in self.cars])
        return s
