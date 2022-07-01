from typing import List

import drawSvg as draw
from visual_field_mapper import Colors, Dimensions, Position
from visual_field_mapper.components import rem
from visual_field_mapper.components.base_component import BaseComponent
from visual_field_mapper.components.visual_field_map import CELL_DIMENSIONS
from visual_field_mapper.garway_heath import SECTORS, GarwayHeathSectorization
from visual_field_mapper.visual_field import Point


class GarwayHeathView(BaseComponent):
    def __init__(
        self, garway_heath: GarwayHeathSectorization, limits_by_sector, *args, **kwargs
    ):
        self.garway_heath = garway_heath
        self.limits_by_sector = limits_by_sector
        super().__init__(*args, margin=rem(2), **kwargs)

    def __draw_point(self, dimensions: Dimensions, position: Position) -> draw.Circle:
        return draw.Circle(
            position.x + dimensions.width / 2,
            position.y + dimensions.height / 2,
            3,
            fill=Colors.black.value,
        )

    def __get_fill_opacity(self, sector):
        fill_opacity = 0.0

        sector_limit = self.limits_by_sector[sector.abbreviation]
        sector_mean = self.garway_heath.get_means_by_sector()[sector.abbreviation]

        range = sector_limit - -35

        if sector_mean <= sector_limit:
            fill_opacity = 1 - round((sector_mean + 35) / range, 2)

        return fill_opacity

    def __draw_sectors(
        self, cell_dimensions: Dimensions, position: Position
    ) -> draw.Group:
        fill = Colors.red.value
        stroke = Colors.gray.value
        stroke_width = 5

        in_sector = draw.Lines(
            0,
            0,
            2 * cell_dimensions.width,
            2 * cell_dimensions.height,
            6 * cell_dimensions.width,
            2 * cell_dimensions.height,
            7 * cell_dimensions.width,
            1 * cell_dimensions.height,
            7 * cell_dimensions.width,
            -1 * cell_dimensions.height,
            6 * cell_dimensions.width,
            -1 * cell_dimensions.height,
            6 * cell_dimensions.width,
            1 * cell_dimensions.height,
            2 * cell_dimensions.width,
            1 * cell_dimensions.height,
            2 * cell_dimensions.width,
            0 * cell_dimensions.height,
            close=True,
            fill=fill,
            fill_opacity=self.__get_fill_opacity(SECTORS["IN"]),
            stroke=stroke,
            stroke_width=stroke_width,
            transform=f"translate({1 * cell_dimensions.width},{2 * cell_dimensions.height})",
        )

        it_sector = draw.Lines(
            0,
            0,
            0 * cell_dimensions.width,
            1 * cell_dimensions.height,
            1 * cell_dimensions.width,
            2 * cell_dimensions.height,
            3 * cell_dimensions.width,
            2 * cell_dimensions.height,
            3 * cell_dimensions.width,
            3 * cell_dimensions.height,
            7 * cell_dimensions.width,
            3 * cell_dimensions.height,
            7 * cell_dimensions.width,
            1 * cell_dimensions.height,
            4 * cell_dimensions.width,
            1 * cell_dimensions.height,
            4 * cell_dimensions.width,
            0 * cell_dimensions.height,
            0 * cell_dimensions.width,
            0 * cell_dimensions.height,
            close=True,
            fill=fill,
            fill_opacity=self.__get_fill_opacity(SECTORS["IT"]),
            stroke=stroke,
            stroke_width=stroke_width,
            transform=f"translate(0,{4 * cell_dimensions.height})",
        )

        t_sector = draw.Rectangle(
            4 * cell_dimensions.width,
            5 * -cell_dimensions.height,
            3 * cell_dimensions.width,
            2 * cell_dimensions.height,
            fill=fill,
            fill_opacity=self.__get_fill_opacity(SECTORS["T"]),
            stroke=stroke,
            stroke_width=stroke_width,
        )

        n_sector = draw.Lines(
            0,
            0,
            0 * cell_dimensions.width,
            6 * cell_dimensions.height,
            1 * cell_dimensions.width,
            5 * cell_dimensions.height,
            1 * cell_dimensions.width,
            1 * cell_dimensions.height,
            close=True,
            fill=fill,
            fill_opacity=self.__get_fill_opacity(SECTORS["N"]),
            stroke=stroke,
            stroke_width=stroke_width,
            transform=f"translate({8 * cell_dimensions.width},{7 * cell_dimensions.height})",
        )

        st_sector = draw.Lines(
            0,
            0,
            0 * cell_dimensions.width,
            1 * cell_dimensions.height,
            3 * cell_dimensions.width,
            1 * cell_dimensions.height,
            3 * cell_dimensions.width,
            0 * cell_dimensions.height,
            6 * cell_dimensions.width,
            0 * cell_dimensions.height,
            6 * cell_dimensions.width,
            -1 * cell_dimensions.height,
            5 * cell_dimensions.width,
            -1 * cell_dimensions.height,
            5 * cell_dimensions.width,
            -2 * cell_dimensions.height,
            3 * cell_dimensions.width,
            -2 * cell_dimensions.height,
            3 * cell_dimensions.width,
            -1 * cell_dimensions.height,
            1 * cell_dimensions.width,
            -1 * cell_dimensions.height,
            1 * cell_dimensions.width,
            0 * cell_dimensions.height,
            0 * cell_dimensions.width,
            0 * cell_dimensions.height,
            close=True,
            fill=fill,
            fill_opacity=self.__get_fill_opacity(SECTORS["ST"]),
            stroke=stroke,
            stroke_width=stroke_width,
            transform=f"translate({1 * cell_dimensions.width},{5 * cell_dimensions.height})",
        )

        sn_sector = draw.Lines(
            0,
            0,
            -3 * cell_dimensions.width,
            3 * cell_dimensions.height,
            -3 * cell_dimensions.width,
            4 * cell_dimensions.height,
            -2 * cell_dimensions.width,
            4 * cell_dimensions.height,
            -2 * cell_dimensions.width,
            3 * cell_dimensions.height,
            -1 * cell_dimensions.width,
            3 * cell_dimensions.height,
            -1 * cell_dimensions.width,
            2 * cell_dimensions.height,
            1 * cell_dimensions.width,
            2 * cell_dimensions.height,
            1 * cell_dimensions.width,
            1 * cell_dimensions.height,
            3 * cell_dimensions.width,
            1 * cell_dimensions.height,
            3 * cell_dimensions.width,
            2 * cell_dimensions.height,
            4 * cell_dimensions.width,
            2 * cell_dimensions.height,
            4 * cell_dimensions.width,
            3 * cell_dimensions.height,
            5 * cell_dimensions.width,
            3 * cell_dimensions.height,
            5 * cell_dimensions.width,
            1 * cell_dimensions.height,
            4 * cell_dimensions.width,
            0 * cell_dimensions.height,
            close=True,
            fill=fill,
            fill_opacity=self.__get_fill_opacity(SECTORS["SN"]),
            stroke=stroke,
            stroke_width=stroke_width,
            transform=f"translate({3 * cell_dimensions.width},{8 * cell_dimensions.height})",
        )

        blind_spot = draw.Rectangle(
            7 * cell_dimensions.width,
            5 * -cell_dimensions.height,
            1 * cell_dimensions.width,
            2 * cell_dimensions.height,
            fill=Colors.black.value,
            stroke=stroke,
            stroke_width=stroke_width,
        )
        return draw.Group(
            [in_sector, it_sector, t_sector, n_sector, st_sector, sn_sector, blind_spot]
        )

    def __draw_row(
        self,
        points: List[Point],
        position: Position = None,
    ) -> draw.Group:
        return draw.Group(
            [
                self.__draw_point(
                    CELL_DIMENSIONS,
                    Position(i * CELL_DIMENSIONS.width, -CELL_DIMENSIONS.height),
                )
                for i, point in enumerate(points)
                if point
            ],
            transform=f"translate({position.x},{position.y})" if position else None,
        )

    def __draw_outline(self, position: Position = None) -> draw.Lines:
        return draw.Lines(
            0,
            0,
            3 * CELL_DIMENSIONS.width,
            3 * CELL_DIMENSIONS.height,
            7 * CELL_DIMENSIONS.width,
            3 * CELL_DIMENSIONS.height,
            9 * CELL_DIMENSIONS.width,
            1 * CELL_DIMENSIONS.height,
            9 * CELL_DIMENSIONS.width,
            -3 * CELL_DIMENSIONS.height,
            7 * CELL_DIMENSIONS.width,
            -5 * CELL_DIMENSIONS.height,
            3 * CELL_DIMENSIONS.width,
            -5 * CELL_DIMENSIONS.height,
            0 * CELL_DIMENSIONS.width,
            -2 * CELL_DIMENSIONS.height,
            close=True,
            fill_opacity=0.0,
            stroke=Colors.black.value,
            stroke_width=4,
            transform=f"translate({position.x},{position.y})" if position else None,
        )

    def render(self) -> draw.Group:
        position = self.get_position()
        matrix = self.garway_heath.visual_field.to_matrix()
        children = []
        children.append(self.__draw_sectors(CELL_DIMENSIONS, position))
        children.extend(
            [
                self.__draw_row(row, Position(0, i * CELL_DIMENSIONS.height))
                for i, row in enumerate(matrix)
            ]
        )
        outline = self.__draw_outline(Position(0, 3 * CELL_DIMENSIONS.height))
        children.append(outline)
        return draw.Group(
            children,
            transform=f"translate({position.x},{position.y})" if position else None,
        )
