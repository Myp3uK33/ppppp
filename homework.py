class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self, training_type: str, duration: float, distance: float,
                 speed: float, calories: float):
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self):
        return (f'Тип тренировки: {self.training_type:}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""
    M_IN_KM = 1000
    LEN_STEP = 0.65
    D_IN_MIN = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        inform = InfoMessage(type(self).__class__.__name__,
                             self.duration, self.get_distance(),
                             self.get_mean_speed(),
                             self.get_spent_calories())
        return inform


class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79

    def get_spent_calories(self):
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                * self.get_mean_speed()
                + self.CALORIES_MEAN_SPEED_SHIFT)
                * self.weight / self.M_IN_KM * self.duration * self.D_IN_MIN)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    COEF_N1 = 0.035
    COEF_N2 = 0.029
    KMH_IN_MS = 0.278
    SM_IN_M = 100

    def __init__(self, action: int, duration: float, weight: float,
                 height: float):
        self.height = height
        super().__init__(action, duration, weight)

    def get_spent_calories(self):
        return ((self.COEF_N1 * self.weight
                + ((self.get_mean_speed() * self.KMH_IN_MS)**2
                 / (self.height / self.SM_IN_M))
                * self.COEF_N2 * self.weight)
                * (self.duration * self.D_IN_MIN))


class Swimming(Training):
    """Тренировка: плавание."""
    SH_SPEED = 1.1
    COEF_SW = 2
    LEN_STEP = 1.38

    def __init__(self, action: int, duration: float, weight: float,
                 length_pool: float, count_pool: float):
        self.length_pool = length_pool
        self.count_pool = count_pool
        super().__init__(action, duration, weight)

    def get_mean_speed(self):
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self):
        return ((self.get_mean_speed() + self.SH_SPEED) * self.COEF_SW
                * self.weight * self.duration)


TRAIN_TYPE = {'SWM': Swimming, 'RUN': Running, 'WLK': SportsWalking}


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    if workout_type not in TRAIN_TYPE:
        raise ValueError(f"Такой тренировки - {workout_type}, не найдено")
    return TRAIN_TYPE[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    InfoMessage = training.show_training_info()
    print(InfoMessage.get_message())
    packages = [('SWM', [720, 1, 80, 25, 40]),
                ('RUN', [15000, 1, 75]),
                ('WLK', [9000, 1, 75, 180])]
    if __name__ == '__main__':
        for workout_type, data in packages:
            Training = read_package(workout_type, data)
    main(Training)
