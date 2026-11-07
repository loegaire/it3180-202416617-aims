from aims.dvd import DigitalVideoDisc
from aims.cart import Cart


def main():
    dvd1 = DigitalVideoDisc("The Lion King", "Animation", 19.95, "Roger Allers", 87)
    dvd2 = DigitalVideoDisc("Star Wars", "Science Fiction", 24.95, "George Lucas", 124)
    dvd3 = DigitalVideoDisc("Blade Runner", "Science Fiction", 18.99, "Ridley Scott", 117)

    my_cart = Cart()
    for disc in (dvd1, dvd2, dvd3):
        my_cart.add_dvd(disc)

    print(f"Total cost: {my_cart.total_cost():.2f} $")


if __name__ == "__main__":
    main()
