import unittest
from unittest.mock import patch, MagicMock
from app import app
from mock_motor_controller import MockMotorController

class TestMotorControlService(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    @patch('backend_app.motor_controller')
    def test_start_motor_success(self, mock_controller):
        mock_controller.start_motor.return_value = {"status": "success", "message": "Motor started"}
        response = self.app.post('/control/start')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"status": "success", "message": "Motor started"})
        mock_controller.start_motor.assert_called_once()

    @patch('backend_app.motor_controller')
    def test_start_motor_low_battery(self, mock_controller):
        mock_controller.start_motor.return_value = {"status": "error", "message": "Battery too low to start motor."}
        response = self.app.post('/control/start')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {"status": "error", "message": "Battery too low to start motor."})
        mock_controller.start_motor.assert_called_once()

    @patch('backend_app.motor_controller')
    def test_set_speed_success(self, mock_controller):
        mock_controller.set_speed.return_value = {"status": "success", "message": "Speed set to 30 km/h"}
        response = self.app.post('/control/speed', json={"speed": 30})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"status": "success", "message": "Speed set to 30 km/h"})
        mock_controller.set_speed.assert_called_once_with(30)

    @patch('backend_app.motor_controller')
    def test_set_speed_invalid(self, mock_controller):
        mock_controller.set_speed.return_value = {"status": "error", "message": "Speed out of range (0–50 km/h)."}
        response = self.app.post('/control/speed', json={"speed": 60})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {"status": "error", "message": "Speed out of range (0–50 km/h)."})
        mock_controller.set_speed.assert_called_once_with(60)

    @patch('backend_app.motor_controller')
    def test_get_status(self, mock_controller):
        mock_controller.get_status.return_value = {
            "is_running": True,
            "current_speed": 30,
            "battery_level": 80,
            "odometer": 100,
            "last_error": None
        }
        response = self.app.get('/control/status')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["current_speed"], 30)
        mock_controller.get_status.assert_called_once()

if __name__ == '__main__':
    unittest.main()