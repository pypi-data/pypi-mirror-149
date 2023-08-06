# Core Library modules
import time
from typing import Union

# Third party modules
import RPi.GPIO as GPIO

# GPIO Mode: BOARD - Ue raspberry Pi Board pin numbers
#            BCM   - Use Broadcom GPIO pin numbers

GPIO.setwarnings(False)


class HC595:
    def __init__(
        self,
        mode: str = "BCM",
        data: int = 17,
        clock: int = 27,
        latch: int = 18,
        ics: int = 1,
    ):
        self._DATA = data
        self._CLOCK = clock
        self._LATCH = latch
        if len({self._DATA, self._LATCH, self._CLOCK}) != 3:
            raise Exception("Pins must be Unique")

        self._ICS = ics
        self._mode = mode
        self._current_storage_register = 0
        self._mask = 0x80 << (8 * (self._ICS - 1))
        self._bits = self._ICS * 8
        if self._mode == "BCM":
            GPIO.setmode(GPIO.BCM)
        else:
            GPIO.setmode(GPIO.BOARD)

        GPIO.setup(self._DATA, GPIO.OUT)
        GPIO.setup(self._CLOCK, GPIO.OUT)
        GPIO.setup(self._LATCH, GPIO.OUT)
        GPIO.output(self._DATA, GPIO.LOW)
        GPIO.output(self._CLOCK, GPIO.LOW)
        GPIO.output(self._LATCH, GPIO.LOW)

    def _shift_register(self, value: int) -> None:
        for bit in range(self._bits):
            data_bit = self._mask & (value << bit)
            GPIO.output(self._DATA, data_bit)
            GPIO.output(self._CLOCK, GPIO.HIGH)
            time.sleep(0.001)
            GPIO.output(self._CLOCK, GPIO.LOW)

    def _storage_register(self) -> None:
        GPIO.output(self._LATCH, GPIO.HIGH)
        time.sleep(0.001)
        GPIO.output(self._LATCH, GPIO.LOW)

    def clear(self) -> None:
        self._shift_register(0)
        self._storage_register()
        self._current_storage_register = 0

    def test(self, repeat: int = 1, speed: str = "medium") -> None:
        pause: Union[int, float]
        if speed not in ["slow", "medium", "fast"]:
            speed = "medium"
        if speed == "slow":
            pause = 1
        elif speed == "medium":
            pause = 0.1
        else:
            pause = 0.01
        try:
            for _ in range(repeat):
                for i in range(self._ICS * 8):
                    self._shift_register(2**i)
                    self._storage_register()
                    time.sleep(pause)
        except KeyboardInterrupt:
            pass

        self._shift_register(self._current_storage_register)
        self._storage_register()

    def set_output(self, output: int, mask: int) -> None:
        if output.bit_length() > self._bits or mask.bit_length() > self._bits:
            raise ValueError(f"Value is out of range of {self._bits} bits")

        if output > mask:
            raise ValueError("Output Value Exceeds Mask Value")

        self._current_storage_register = (
            self._current_storage_register - (self._current_storage_register & mask)
        ) + output
        self._shift_register(self._current_storage_register)
        self._storage_register()

    def set_pattern(self, chip_pattern: list) -> None:
        dec_repr: int = 0
        mask: int = (2**self._bits) - 1

        if all(isinstance(element, int) for element in chip_pattern):
            if len(chip_pattern) != self._bits:
                raise ValueError("Length of Pattern is incorrect")
            led_pattern = chip_pattern
        elif all(isinstance(element, list) for element in chip_pattern):
            if len(chip_pattern) != self._ICS:
                raise ValueError("Length of Pattern is incorrect")
            led_pattern = [led for chip in chip_pattern for led in chip]
        else:
            raise ValueError("The pattern in incorrectly formatted")

        for bit in range(self._bits):
            dec_repr += led_pattern[bit] * (2**bit)

        self.set_output(dec_repr, mask)
