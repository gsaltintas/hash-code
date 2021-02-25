class Car:
    def __init__(self, streets_no, first_street, simulation_time):
        self.streets_no = streets_no
        self.path = []
        self.current_street = first_street
        self.current_street.light.add_to_queue(self)
        self.to_node = 0
        self.path_index = 0
        self.path_completed = False
        self.moved = [False for i in range(simulation_time)]

    def at_node(self):
        return self.to_node == 0

    def add_to_path(self, street):
        self.path.append(street)

    def move_to_next_street(self, current_time):
        if self.path_index == self.streets_no - 1:
            self.path_completed = True
        if not self.path_completed and not self.moved[current_time]:
            self.path_index += 1
            self.current_street = self.path[self.path_index]
            self.to_node = self.current_street.L
            self.moved[current_time] = True

    def move(self, current_time):
        self.to_node -= 1
        self.moved[current_time] = True