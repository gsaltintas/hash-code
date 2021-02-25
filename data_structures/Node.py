class Node:
    def __init__(self, no, simulation_time):
        self.no = no
        self.incoming_streets = []
        self.outgoing_streets = []
        self.history = {i: "" for i in range(simulation_time)}

    def add_incoming_street(self, street):
        self.incoming_streets.append(street)

    def add_outgoing_street(self, street):
        self.outgoing_streets.append(street)