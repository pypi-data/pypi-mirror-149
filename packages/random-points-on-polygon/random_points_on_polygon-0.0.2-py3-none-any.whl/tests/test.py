import unittest
from random_points_on_polygon import PointsGenerator
from random_points_on_polygon.samples import *
from shapely.geometry import MultiPolygon, Polygon
from typing import List, Union


class TestPointsGenerator(unittest.TestCase):
    def setUp(self):
        self.surfaces: List[Union[Polygon, MultiPolygon]] = [
            POLYGON_SAMPLE_1,
            POLYGON_SAMPLE_2,
            MULTIPOLYGON_SAMPLE,
        ]

    def test_init(self) -> None:
        for surface in self.surfaces:
            self.assertIsInstance(
                surface,
                (Polygon, MultiPolygon),
                "surface should be a Polygon or MultiPolygon",
            )

            pg: PointsGenerator = PointsGenerator(surface)
            self.assertIsInstance(
                pg, PointsGenerator, "pg should be a PointsGenerator instance"
            )

    def test_generation(self) -> None:
        for surface in self.surfaces:
            pg: PointsGenerator = PointsGenerator(surface)

            pg.generate(10)
            self.assertEqual(len(pg.points), 10)

            pg.generate(5)
            self.assertEqual(len(pg.points), 15)

            pg.reset()
            self.assertEqual(len(pg.points), 0)

            pg.generate(25)
            self.assertEqual(len(pg.points), 25)

    def test_points_on_surface(self) -> None:
        for surface in self.surfaces:
            pg: PointsGenerator = PointsGenerator(surface)

            for i in range(1, 10):
                pg.generate(10 * i)
                for point in pg.points:
                    self.assertTrue(point.within(pg.surface))
                pg.reset()


if __name__ == "__main__":
    unittest.main()
