# Global program step time in seconds
STEP_TIME = 0.004
# Left Motor pins
PINS_MOTOR_LEFT = [2, 3, 4, 17]
# Right Motor pins
PINS_MOTOR_RIGHT = [27, 22, 10, 9]
# IR Sensor Pins
PINS_SENSOR = [14, 15, 18]
# Button pin
PIN_BUTTON = 26
# Led Pins
PINS_FRONT_LED = [12, 16, 20, 21]
# Left indicatior led
PINS_LEFT_LED = 13
# Right indicator led
PINS_RIGHT_LED = 19
# Degrees the wheel turns per motor step
MOTOR_DEG_PER_STEP = 5.625 / 64
# Url to get new delivers
DELIVERY_URL = "http://rutgeruijtendaal.com/PiRiders/api.php?function=deliveryInfo"
# Url to say a delivery is done
DELIVERED_URL = "http://rutgeruijtendaal.com/PiRiders/api.php?function=deliveryUpdate"
