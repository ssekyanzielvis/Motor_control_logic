class MockMotorController:
    def __init__(self):
        self.is_running = False
        self.speed = 0
        self.battery_level = 100  # Percentage
        self.position = 0  # Simulated odometer in meters
        self.error = None

    def start_motor(self):
        if self.battery_level < 10:
            self.error = "Battery too low to start motor."
            return {"status": "error", "message": self.error}
        print("Mock Motor: Starting...")
        self.is_running = True
        self.error = None
        return {"status": "success", "message": "Motor started"}

    def stop_motor(self):
        print("Mock Motor: Stopping...")
        self.is_running = False
        self.speed = 0
        self.error = None
        return {"status": "success", "message": "Motor stopped"}

    def set_speed(self, speed):
        if not self.is_running:
            self.error = "Motor is not running."
            return {"status": "error", "message": self.error}
        if not isinstance(speed, (int, float)):
            self.error = "Invalid speed format."
            return {"status": "error", "message": self.error}
        if 0 <= speed <= 50:  # Golf cart speed limit: 0–50 km/h
            print(f"Mock Motor: Setting speed to {speed} km/h")
            self.speed = speed
            self.battery_level -= speed * 0.1  # Simulate battery drain
            if self.battery_level < 0:
                self.battery_level = 0
                self.error = "Battery depleted."
                return {"status": "error", "message": self.error}
            self.error = None
            return {"status": "success", "message": f"Speed set to {speed} km/h"}
        else:
            self.error = "Speed out of range (0–50 km/h)."
            return {"status": "error", "message": self.error}

    def get_status(self):
        return {
            "is_running": self.is_running,
            "current_speed": self.speed,
            "battery_level": self.battery_level,
            "odometer": self.position,
            "last_error": self.error
        }