class Node:
    def __init__(self, no, simulation_time):
        self.no = no
        self.incoming_streets = []
        self.outgoing_streets = []
        self.history = {i: "" for i in range(simulation_time)}
        self.cycle = []
        self.one_cycle_time = 0
        self.cycle_weights = {}

    def add_incoming_street(self, street):
        self.incoming_streets.append(street)

    def add_outgoing_street(self, street):
        self.outgoing_streets.append(street)
