import RPi.GPIO as GPIO
import keyboard
import time

# Definir els pins GPIO
IN1 = 17  # Entrada 1 del L298N
IN2 = 27  # Entrada 2 del L298N
ENA = 22  # Control de velocitat (PWM)

# Pins dels botons
BTN_CW = 23
BTN_CCW = 24
BTN_STOP = 25

# Configuració dels GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(ENA, GPIO.OUT)  # Sortida PWM

# Configuració dels botons
GPIO.setup(BTN_CW, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BTN_CCW, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BTN_STOP, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Configurar PWM al pin ENA (freqüència 1000Hz)
pwm = GPIO.PWM(ENA, 1000)
pwm.start(50)  # Iniciar PWM amb el 50% de potència


def motor_move_CW():
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)


def motor_move_CCW():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)


def motor_stop():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)


try:
    while True:
        if GPIO.input(BTN_CW) == GPIO.LOW:
            print("Motor move cw")
            motor_move_CW()

        elif GPIO.input(BTN_CCW) == GPIO.LOW:
            print("Motor move ccw")
            motor_move_CCW()

        elif GPIO.input(BTN_STOP) == GPIO.LOW:
            print("Motor stop")
            motor_stop()

        time.sleep(0.1)

except KeyboardInterrupt:
    print("Stoping motor...")

finally:
    pwm.stop()
    GPIO.cleanup()
