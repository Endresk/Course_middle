from pattern_repository import ClientRepository, CarRepository, Client, Car
from pattern_strategy import AutoService, MaintenanceService, EngineRepairService, OilChange, ChangingPads


def main() -> None:
    """

    :return:
    """

    """
    
    Паттерн репозитория
    
    """

    client_repo = ClientRepository()
    car_repo = CarRepository()

    # Добавляем клиентов
    client_repo.add(Client(1, "Иван"))
    client_repo.add(Client(2, "Екатерина"))
    client_repo.add(Client(3, "Сергей"))

    # Добавляем автомобили
    car_repo.add(Car(1, "Toyota", 1))
    car_repo.add(Car(2, "Honda", 2))
    car_repo.add(Car(3, "Ford", 3))

    # Получаем данные
    client = client_repo.get_by_id(3)
    cars = car_repo.get_by_client_id(client.id)

    print(f"Клиент: {client.name}, Автомобили: {[car.model for car in cars]}")

    """

    Паттерн стратегия

    """

    # Создаем контекст автосервиса
    service = AutoService(MaintenanceService())

    # Выполняем техническое обслуживание
    print(service.perform_service())

    # Меняем стратегию на ремонт двигателя
    service.set_strategy(EngineRepairService())
    print(service.perform_service())

    # Меняем стратегию на замену масла
    service.set_strategy(OilChange())
    print(service.perform_service())

    # Меняем стратегию на замену колодок
    service.set_strategy(ChangingPads())
    print(service.perform_service())


if __name__ == '__main__':
    main()
