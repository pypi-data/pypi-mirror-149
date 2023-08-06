# Copyright (C) 2022 twyleg
from serial import Serial


class InvalidChannelError(Exception):
    def __init__(self, channel: int):
        super().__init__('Invalid channel: {} (use 1..8)'.format(channel))


class InvalidRawValueError(Exception):
    def __init__(self, value: int):
        super().__init__('Invalid value: {}'.format(value))


class InvalidPercentageValueError(Exception):
    def __init__(self, value: int):
        super().__init__('Invalid value: {}'.format(value))


class PPMEncoder:

    def __init__(self, serial: Serial):
        self.serial = serial

    @staticmethod
    def bound(value: int, min_value: int, max_value: int):
        return min(max(value, min_value), max_value)

    def set_channel_raw(self, channel: int, raw_value: int):
        if not 1 <= channel <= 8:
            raise InvalidChannelError(channel)
        elif not 1000 <= raw_value <= 2000:
            raise InvalidRawValueError(raw_value)
        else:
            command = '{}={:04d}'.format(channel, raw_value)
            self.serial.write(command.encode())

    def set_channel_raw_bounded(self, channel: int, raw_value: int):
        bounded_raw_value = self.bound(raw_value, 1000, 2000)
        self.set_channel_raw(channel, bounded_raw_value)

    def set_channel_percentage(self, channel: int, percent_value: int):
        if not -100 <= percent_value <= 100:
            raise InvalidPercentageValueError(percent_value)
        else:
            raw_value = int(1500 + (percent_value / 100.0) * 500)
            self.set_channel_raw(channel, raw_value)

    def set_channel_percentage_bounded(self, channel: int, percent_value: int):
        bounded_percentage_value = self.bound(percent_value, -100, +100)
        self.set_channel_percentage(channel, bounded_percentage_value)


if __name__ == '__main__':
    ppm_encoder = PPMEncoder(None)
    ppm_encoder.set_channel_raw(1, 1500)
    ppm_encoder.set_channel_raw(1, 500)
