import unittest
from app import app


class PixelTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_valid_corners_valid_dimensions(self):
        json_data = {
            'image_dimensions': (3, 5),
            'corner_points': [(1, 1), (4, 3), (1, 3), (4, 1)]
        }
        response = self.client.post(json=json_data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('pixels' in response.json.keys())
        self.assertEqual(response.json['pixels'],
            [
                [[1, 3], [1.75, 3], [2.5, 3], [3.25, 3], [4, 3]],
                [[1, 2], [1.75, 2], [2.5, 2], [3.25, 2], [4, 2]],
                [[1, 1], [1.75, 1], [2.5, 1], [3.25, 1], [4, 1]]
            ])

    def test_extra_dimension(self):
        json_data = {
            'image_dimensions': (2, 2, 2),
            'corner_points': [(0, 0), (0, 1), (1, 1), (1, 0)]
        }
        response = self.client.post(json=json_data)
        self.assertEqual(response.status_code, 400)

    def test_extra_dimension_in_corner_points(self):
        json_data = {
            'image_dimensions': (2, 2),
            'corner_points': [(0, 0), (0, 1), (1, 1), (1, 0, 0)]
        }
        response = self.client.post(json=json_data)
        self.assertEqual(response.status_code, 400)

    def test_invalid_data_in_corner_points(self):
        json_data = {
            'image_dimensions': (2, 2),
            'corner_points': [(0, 0), (0, 1), ('x', 1), (1, 0)]
        }
        response = self.client.post(json=json_data)
        self.assertEqual(response.status_code, 400)

    def test_corner_points_dont_form_rectangle(self):
        json_data = {
            'image_dimensions': (2, 2),
            'corner_points': [(0, 0), (0, 1), (1, 1), (1, 0.5)]
        }
        response = self.client.post(json=json_data)
        self.assertEqual(response.status_code, 400)


if __name__ == '__main__':
    unittest.main(verbosity=2)
