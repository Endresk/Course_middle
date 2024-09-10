from abc import ABC, abstractmethod
from typing import Any


class Client:
    def __init__(self, id, name):
        self.id = id
        self.name = name


class Car:
    def __init__(self, id, model, client_id):
        self.id = id
        self.model = model
        self.client_id = client_id


class IClientRepository(ABC):
    @abstractmethod
    def add(self, client: Client) -> None:
        pass

    @abstractmethod
    def get_by_id(self, client_id: int) -> Client:
        pass


class ICarRepository(ABC):
    @abstractmethod
    def add(self, car: Car) -> None:
        pass

    @abstractmethod
    def get_by_client_id(self, client_id: int) -> list:
        pass


class ClientRepository(IClientRepository):
    def __init__(self):
        self.clients = []

    def add(self, client: Client) -> None:
        self.clients.append(client)

    def get_by_id(self, client_id: int) -> Any | None:
        for client in self.clients:
            if client.id == client_id:
                return client
        return None


class CarRepository(ICarRepository):
    def __init__(self):
        self.cars = []

    def add(self, car: Car) -> None:
        self.cars.append(car)

    def get_by_client_id(self, client_id: int) -> list:
        return [car for car in self.cars if car.client_id == client_id]
