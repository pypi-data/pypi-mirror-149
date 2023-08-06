from domtree.svg import *
from domtree import Node


def main():
    c = circle(x=10, y=10).add(x=10).mul(y=2)
    print(c)


if __name__ == "__main__":
    main()
