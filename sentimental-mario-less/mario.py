import cs50

# TODO


def main():
    height = get_height()
    for i in range(height):
        print(" " * (height - i), end='')
        print("#" * (i+1))


def get_height():
    while True:
        try:
            n = int(input("Height: "))   # propmting user for an integer
            if n > 0 and n < 9:  # number have to be bigger than 0 and less than 9
                break
        except ValueError:   # printing a message if height dont passes the coniditons
            print("That's not an integer!")
    return n  # returning a value


main()