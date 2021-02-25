from data_structures.DataStructures import City
from data_structures.Car import Car
from data_structures.Street import Street


def main():
    Da, Fa, city_a = parse_data("files/a.txt")
    city_a.simulate()
    Db, Fb, city_b = parse_data("files/b.txt")
    Dc, Fc, city_c = parse_data("files/c.txt")
    Dd, Fd, city_d = parse_data("files/d.txt")
    De, Fe, city_e = parse_data("files/e.txt")


def parse_data(path):
    """ given the txt file representing simulation, return a city"""
    with open(path, "r") as data:
        line_num = 0
        for line in data:
            line = line.strip("\n")
            if line_num == 0:
                D, I, S, V, F = [int(i) for i in line.split(" ")]
                city = City(node_no=I, street_no=S, car_no=V, simulation_time=D)
            elif line_num <= S:
                B, E, street_name, L = line.split(" ")
                street = Street(name=street_name, start=city.nodes[int(B)], end=city.nodes[int(E)], L=int(L))
                city.add_street(street)
            elif line_num <= S + V:
                P, names = line.split(" ")[0], line.split(" ")[1:]
                car = Car(streets_no=P, first_street=city.streets[names[0]], simulation_time=D)
                for i in names:
                    car.add_to_path(city.get_street(i))
                city.add_car(car)
            line_num += 1
    return D, F, city


if __name__ == "__main__":
    main()
