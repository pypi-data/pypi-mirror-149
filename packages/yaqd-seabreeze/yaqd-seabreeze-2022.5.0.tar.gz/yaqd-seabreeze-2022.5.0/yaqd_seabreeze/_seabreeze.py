__all__ = ["Seabreeze"]

import asyncio
from typing import Dict, Any, List, Tuple

from seabreeze.spectrometers import Spectrometer  # type: ignore
from yaqd_core import HasMapping, HasMeasureTrigger, IsSensor, IsDaemon


class Seabreeze(HasMapping, HasMeasureTrigger, IsSensor, IsDaemon):
    _kind = "seabreeze"

    def __init__(self, name, config, config_filepath):
        self.spec = Spectrometer.from_serial_number(config.get("serial"))

        super().__init__(name, config, config_filepath)
        self.serial = config["serial"] or self.spec.serial_number
        self.model = config["model"] or self.spec.model

        self._correct_dark_counts = config.get("correct_dark_counts", False)
        self._correct_nonlinearity = config.get("correct_nonlinearity", False)

        self._channel_names = ["intensities"]
        self._channel_units = {"intensities": None}
        self._channel_shapes = {"intensities": (self.spec.pixels,)}
        self._channel_mappings = {"intensities": ["wavelengths"]}
        self._mappings["wavelengths"] = self.spec.wavelengths()
        self._mapping_units = {"wavelengths": "nm"}

        if self._state["integration_time_micros"]:
            self.set_integration_time_micros(self._state["integration_time_micros"])

    async def _measure(self):
        out = {}
        out["intensities"] = self.spec.intensities(
            self._correct_dark_counts, self._correct_nonlinearity
        )
        return out

    def set_integration_time_micros(self, micros: int) -> None:
        """Set the integration time in microseconds"""
        self._state["integration_time_micros"] = micros
        self.spec.integration_time_micros(micros)

    def get_integration_time_micros(self) -> int:
        """Get the integration time in microseconds"""
        return self._state["integration_time_micros"]

    def get_integration_time_units(self) -> str:
        return "us"

    def get_integration_time_limits(self) -> Tuple[int, int]:
        return self.spec.integration_time_micros_limits
