class Point:
    def __init__(self, position, value):
        self.position = position
        self.value = value
        self.central_peripheral_sector = self.__get_central_peripheral_sector()
        self.garway_heath_sector = self.__get_garway_heath_sector()

    def __repr__(self):
        from pprint import pformat

        return "Point: " + pformat(vars(self), indent=2)

    def __is_position_between(self, start: int, end: int):
        return self.position >= start and self.position <= end

    def __get_central_peripheral_sector(self):
        if (
            self.__is_position_between(20, 23)
            or self.__is_position_between(28, 31)
            or self.position in [14, 15, 38, 39]
        ):
            return "central"

        return "peripheral"

    def __get_garway_heath_sector(self):
        if self.__is_position_between(0, 5) or self.position in [10, 12]:
            return "IN"

        if (
            self.__is_position_between(6, 9)
            or self.__is_position_between(13, 18)
            or self.__is_position_between(23, 26)
        ):
            return "IT"

        if self.position in [11, 19, 27, 35]:
            return "N"

        if self.__is_position_between(20, 22) or self.__is_position_between(28, 30):
            return "T"

        if (
            self.__is_position_between(31, 33)
            or self.__is_position_between(37, 41)
            or self.__is_position_between(45, 46)
        ):
            return "ST"

        if (
            self.position in [34, 36]
            or self.__is_position_between(42, 44)
            or self.__is_position_between(47, 52)
        ):
            return "SN"

        return ""
