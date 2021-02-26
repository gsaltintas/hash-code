from src.City import City
from src.Car import Car
from src.Street import Street
import os


def main():
    for txt in ["a", "b", "c", "d", "e", "f"]:
        D, F, city = parse_data(os.path.abspath(os.path.join("..", "files", "%s.txt" % txt)))
        city.setup_cycles()
        city.simulate()
        # print(city.score())
        city.report(os.path.abspath(os.path.join("..", "output_files", "%s.txt" % txt)))
        print("saved for %s" % txt)


def write_data(path, data):
    with open(path, "w") as file:
        file.write(data)


def parse_data(path):
    """ given the txt file representing simulation, return a city"""
    with open(path, "r") as data:
        line_num = 0
        for line in data:
            line = line.strip("\n")
            if line_num == 0:
                D, I, S, V, F = [int(i) for i in line.split(" ")]
                city = City(node_no=I, street_no=S, car_no=V, simulation_time=D, score_coef=F)
            elif line_num <= S:
                B, E, street_name, L = line.split(" ")
                street = Street(name=street_name, start=city.nodes[int(B)], end=city.nodes[int(E)],
                                L=int(L), simulation_time=D)
                city.add_street(street)
            elif line_num <= S + V:
                P, names = line.split(" ")[0], line.split(" ")[1:]
                car = Car(streets_no=int(P), first_street=city.streets[names[0]], simulation_time=D)
                for i in names:
                    car.add_to_path(city.get_street(i))
                city.add_car(car)
            line_num += 1
    city.set_up_always_green_lights()
    return D, F, city


if __name__ == "__main__":
    main()
