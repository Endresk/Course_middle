from abc import ABC, abstractmethod


class ServiceStrategy(ABC):
    @abstractmethod
    def perform_service(self) -> str:
        pass


class OilChange(ServiceStrategy):
    def perform_service(self) -> str:
        return "Замена масла"


class ChangingPads(ServiceStrategy):
    def perform_service(self) -> str:
        return "Замена колодок"


class MaintenanceService(ServiceStrategy):
    def perform_service(self) -> str:
        return "Выполняется техническое обслуживание автомобиля."


class EngineRepairService(ServiceStrategy):
    def perform_service(self) -> str:
        return "Выполняется ремонт двигателя."


class AutoService:
    def __init__(self, strategy: ServiceStrategy):
        self.strategy = strategy

    def set_strategy(self, strategy: ServiceStrategy) -> None:
        self.strategy = strategy

    def perform_service(self) -> str:
        return self.strategy.perform_service()
