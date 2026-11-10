"""Подводная лодка «Жемчужина»: контракт SPEC.md, стандартная библиотека."""

from math import isfinite


class SubmarineError(Exception):
    """Общая ошибка состояния подводной лодки."""


class NotSubmergedError(SubmarineError):
    """Плавание невозможно на поверхности."""


class PropellerDamagedError(SubmarineError):
    """Плавание невозможно с повреждённым винтом."""


class NotEnoughEnergyError(SubmarineError):
    """Запаса энергии недостаточно для плавания."""


def _number(value: float, parameter: str) -> float:
    """Проверить числовой вход и вернуть конечный float."""
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"{parameter} must be int or float, not bool")
    try:
        number = float(value)
    except OverflowError as error:
        raise ValueError(f"{parameter} must fit in a finite float") from error
    if not isfinite(number):
        raise ValueError(f"{parameter} must be finite")
    return number


class Submarine:
    """Лодка с винтом, запасом энергии и атрибутами только для чтения."""

    def __init__(
        self, name: str, propeller_diameter_m: float, energy: float = 100.0
    ) -> None:
        """Создать лодку на поверхности с исправным винтом и нулевым путём."""
        if not isinstance(name, str):
            raise TypeError("name must be str")
        if not name.strip():
            raise ValueError("name must contain a non-whitespace character")
        propeller_diameter_m = _number(propeller_diameter_m, "propeller_diameter_m")
        if propeller_diameter_m <= 0:
            raise ValueError("propeller_diameter_m must be positive")
        energy = _number(energy, "energy")
        if not 0 <= energy <= 100:
            raise ValueError("energy must be between 0 and 100")

        self._name = name
        self._propeller_diameter_m = propeller_diameter_m
        self._energy = energy
        self._depth_m = 0.0
        self._distance_km = 0.0
        self._propeller_intact = True

    @property
    def name(self) -> str:
        """Имя лодки без преобразования исходной строки."""
        return self._name

    @property
    def propeller_diameter_m(self) -> float:
        """Диаметр гребного винта в метрах."""
        return self._propeller_diameter_m

    @property
    def energy(self) -> float:
        """Текущий запас энергии от 0 до 100."""
        return self._energy

    @property
    def depth_m(self) -> float:
        """Абсолютная глубина в метрах от 0 до 50."""
        return self._depth_m

    @property
    def distance_km(self) -> float:
        """Суммарный пройденный путь в километрах."""
        return self._distance_km

    @property
    def propeller_intact(self) -> bool:
        """Исправен ли гребной винт."""
        return self._propeller_intact

    def swim(self, distance_km: float) -> float:
        """Проплыть дистанцию под водой; вернуть время в часах."""
        distance_km = _number(distance_km, "distance_km")
        if distance_km <= 0:
            raise ValueError("distance_km must be positive")
        if self._depth_m == 0:
            raise NotSubmergedError("submarine must be submerged")
        if not self._propeller_intact:
            raise PropellerDamagedError("propeller is damaged")
        required_energy = distance_km * 2
        if self._energy < required_energy:
            raise NotEnoughEnergyError("not enough energy")

        self._energy -= required_energy
        self._distance_km += distance_km
        return distance_km / 10

    def dive(self, depth_m: float) -> None:
        """Установить глубину от 0 до 50 м без расхода энергии."""
        depth_m = _number(depth_m, "depth_m")
        if not 0 <= depth_m <= 50:
            raise ValueError("depth_m must be between 0 and 50")
        self._depth_m = depth_m

    def recharge(self, amount: float) -> None:
        """Добавить положительное количество энергии, не превышая 100."""
        amount = _number(amount, "amount")
        if amount <= 0:
            raise ValueError("amount must be positive")
        self._energy = min(100.0, self._energy + amount)

    def damage_propeller(self) -> None:
        """Повредить винт; повторное повреждение допустимо."""
        self._propeller_intact = False

    def repair_propeller(self) -> None:
        """Восстановить винт; повторный ремонт допустим."""
        self._propeller_intact = True

    def get_status(self) -> dict[str, object]:
        """Вернуть независимый снимок всех шести публичных атрибутов."""
        return {
            "name": self._name,
            "propeller_diameter_m": self._propeller_diameter_m,
            "energy": self._energy,
            "depth_m": self._depth_m,
            "distance_km": self._distance_km,
            "propeller_intact": self._propeller_intact,
        }
