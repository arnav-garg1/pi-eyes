import RPi.GPIO as GPIO
import time

# Braille dictionary
braille_dict = {
    'a': [1, 0, 0, 0, 0, 0],
    'b': [1, 1, 0, 0, 0, 0],
    'c': [1, 0, 1, 0, 0, 0],
    'd': [1, 0, 1, 1, 0, 0],
    'e': [1, 0, 0, 1, 0, 0],
    'f': [1, 1, 1, 0, 0, 0],
    'g': [1, 1, 1, 1, 0, 0],
    'h': [1, 1, 0, 1, 0, 0],
    'i': [0, 1, 1, 0, 0, 0],
    'j': [0, 1, 1, 1, 0, 0],
    'k': [1, 0, 0, 0, 1, 0],
    'l': [1, 1, 0, 0, 1, 0],
    'm': [1, 0, 1, 0, 1, 0],
    'n': [1, 0, 1, 1, 1, 0],
    'o': [1, 0, 0, 1, 1, 0],
    'p': [1, 1, 1, 0, 1, 0],
    'q': [1, 1, 1, 1, 1, 0],
    'r': [1, 1, 0, 1, 1, 0],
    's': [0, 1, 1, 0, 1, 0],
    't': [0, 1, 1, 1, 1, 0],
    'u': [1, 0, 0, 0, 1, 1],
    'v': [1, 1, 0, 0, 1, 1],
    'w': [0, 1, 1, 1, 0, 1],
    'x': [1, 0, 1, 0, 1, 1],
    'y': [1, 0, 1, 1, 1, 1],
    'z': [1, 0, 0, 1, 1, 1],
    ' ': [0, 0, 0, 0, 0, 0],  # Space
}

# GPIO pin configuration
GPIO.setmode(GPIO.BCM)
pins = [17, 18, 22, 23, 24, 25]  # Example GPIO pins for Braille points
PWM_FREQUENCY = 50  # Frequency for servo motors (Hz)

# Initialize GPIO pins
def setup_pins():
    for pin in pins:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.LOW)
    print("GPIO pins configured.")

# Clean up GPIO pins
def cleanup_pins():
    GPIO.cleanup()
    print("GPIO pins cleaned up.")

# Convert Braille points to servo motor PWM signals
def activate_braille(braille_points):
    pwm_objects = []
    try:
        # Initialize PWM for each pin
        for pin, point in zip(pins, braille_points):
            pwm = GPIO.PWM(pin, PWM_FREQUENCY)
            pwm.start(0)
            pwm_objects.append(pwm)
            if point == 1:
                pwm.ChangeDutyCycle(7.5)  # Move servo to "active" position
            else:
                pwm.ChangeDutyCycle(2.5)  # Move servo to "inactive" position
            time.sleep(0.1)  # Small delay for stabilization

        # Hold the state for a moment to allow tactile reading
        time.sleep(1)

        # Reset servos to inactive state
        for pwm in pwm_objects:
            pwm.ChangeDutyCycle(0)
        time.sleep(0.5)
    finally:
        # Stop PWM signals
        for pwm in pwm_objects:
            pwm.stop()

# Text-to-Braille conversion
def text_to_braille(text):
    braille_output = []
    for char in text.lower():
        if char in braille_dict:
            braille_output.append(braille_dict[char])
        else:
            print(f"Warning: '{char}' is not supported and will be ignored.")
    return braille_output

# Main function
if __name__ == "__main__":
    try:
        print("Starting Text-to-Braille Converter...")
        setup_pins()

        # Get user input and convert to Braille
        user_input = input("Enter the text you want to convert to Braille: ")
        braille_representation = text_to_braille(user_input)

        print("\nActivating Braille points on GPIO...")
        for char, braille_points in zip(user_input, braille_representation):
            print(f"Character: '{char}' -> Braille: {braille_points}")
            activate_braille(braille_points)
            time.sleep(1)  # Delay between characters for readability

        print("Text-to-Braille conversion complete.")
    except KeyboardInterrupt:
        print("\nProgram interrupted by user.")
    finally:
        cleanup_pins()
