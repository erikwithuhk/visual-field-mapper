from .visual_field import VisualField


def main():
    values = [
        1,
        1,
        0,
        1,
        2,
        3,
        1,
        0,
        1,
        0,
        2,
        2,
        4,
        1,
        2,
        1,
        1,
        2,
        5,
        5,
        6,
        3,
        3,
        3,
        3,
        5,
        19,
        21,
        20,
        22,
        21,
        22,
        21,
        22,
        20,
        22,
        22,
        22,
        22,
        22,
        22,
        23,
        22,
        22,
        22,
        22,
        23,
        22,
        22,
        22,
        22,
        22,
    ]

    visual_field = VisualField(values)
    visual_field.print()


if __name__ == "__main__":
    main()
