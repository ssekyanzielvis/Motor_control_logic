from flask import Flask, jsonify, request
import os
from typing import Dict, Any, Union
from motor_controller_interface import IMotorController

app = Flask(__name__)

# Configure based on environment
def get_motor_controller() -> IMotorController:
    """Factory function to create the appropriate motor controller based on environment."""
    if os.environ.get("USE_MOCK_MOTOR", "").lower() == "true":
        from mock_motor_controller import MockMotorController
        from mock_motor_client import MockMotorClient
        print("Using Mock Motor Controller")
        return MockMotorClient(MockMotorController())
    else:
        from real_motor_client import RealMotorClient
        print("Using Real Motor Controller")
        return RealMotorClient("http://real-motor-api:8080")

motor_controller = get_motor_controller()

@app.route('/control/start', methods=['POST'])
def start_motor_command() -> tuple:
    """
    Start the motor.
    
    Returns:
        tuple: JSON response and HTTP status code
    """
    try:
        response = motor_controller.start_motor()
        status_code = 200 if response.get("status") == "success" else 400
        return jsonify(response), status_code
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Failed to start motor: {str(e)}"
        }), 500

@app.route('/control/stop', methods=['POST'])
def stop_motor_command() -> tuple:
    """
    Stop the motor.
    
    Returns:
        tuple: JSON response and HTTP status code
    """
    try:
        response = motor_controller.stop_motor()
        status_code = 200 if response.get("status") == "success" else 400
        return jsonify(response), status_code
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Failed to stop motor: {str(e)}"
        }), 500

@app.route('/control/speed', methods=['POST'])
def set_speed_command() -> tuple:
    """
    Set motor speed.
    
    Expects JSON payload: {"speed": <float>}
    
    Returns:
        tuple: JSON response and HTTP status code
    """
    try:
        data = request.get_json()
        if not data or 'speed' not in data:
            return jsonify({
                "status": "error",
                "message": "Speed parameter is required"
            }), 400
            
        speed = float(data['speed'])
        response = motor_controller.set_speed(speed)
        status_code = 200 if response.get("status") == "success" else 400
        return jsonify(response), status_code
    except ValueError:
        return jsonify({
            "status": "error",
            "message": "Speed must be a numeric value"
        }), 400
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Failed to set speed: {str(e)}"
        }), 500

@app.route('/control/status', methods=['GET'])
def get_motor_status() -> tuple:
    """
    Get current motor status.
    
    Returns:
        tuple: JSON response and HTTP status code
    """
    try:
        status = motor_controller.get_status()
        return jsonify(status), 200
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Failed to get motor status: {str(e)}"
        }), 500

@app.route('/health', methods=['GET'])
def health_check() -> tuple:
    """
    Health check endpoint for monitoring.
    
    Returns:
        tuple: JSON response and HTTP status code
    """
    return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=os.environ.get('FLASK_DEBUG', 'false').lower() == 'true')