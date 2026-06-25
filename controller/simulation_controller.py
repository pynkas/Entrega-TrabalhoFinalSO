"""
Camada de orquestração do simulador de escalonamento de processos.

Define SimulationController, responsável por conectar processos,
scheduler, engine de simulação e cálculo de métricas, sem implementar
lógica própria de escalonamento ou temporização.
"""

from models.process import Process
from models.metrics import Metrics, SimulationMetrics
from schedulers.base_scheduler import BaseScheduler
from engine.simulation_engine import SimulationEngine, GanttEntry


class SimulationController:
    """
    Coordena a execução de uma simulação de escalonamento.

    Recebe processos e um scheduler, cria a SimulationEngine e expõe
    operações de alto nível para executar, reiniciar e consultar resultados.

    Args:
        processes: Processos a serem simulados.
        scheduler: Algoritmo de escalonamento utilizado.
    """

    def __init__(
        self,
        processes: list[Process],
        scheduler: BaseScheduler,
    ) -> None:
        self._processes: list[Process]    = processes
        self._scheduler: BaseScheduler    = scheduler
        self._engine:    SimulationEngine = SimulationEngine(
            processes = processes,
            scheduler = scheduler,
        )


    # ------------------------------------------------------------------
    # Operações principais
    # ------------------------------------------------------------------
    def run(self) -> SimulationMetrics:
        """                       
        Executa a simulação até o fim e retorna suas métricas.

        Returns:
            Métricas calculadas ao final da simulação.

        Raises:
            RuntimeError: Se a simulação já tiver sido concluída.
        """
        if self._engine.is_finished:
            raise RuntimeError(
                "A simulação já foi concluída. "
                "Chame reset() antes de executar novamente."
            )

        while not self._engine.is_finished:
            self._engine.tick()

        return self.calculate_metrics()

    def reset(self) -> None:
        """
        Prepara o controller para uma nova execução com os mesmos dados.

        Cada processo é restaurado, o scheduler é resetado e uma nova
        SimulationEngine é criada para evitar estado residual da execução
        anterior.
        """
        for process in self._processes:
            process.reset()

        self._scheduler.reset()

        self._engine = SimulationEngine(
            processes = self._processes,
            scheduler = self._scheduler,
        )

    def calculate_metrics(self) -> SimulationMetrics:
        """                      
            Calcula as métricas da simulação com base nos processos finalizados.

            Returns:
                Métricas individuais e médias da simulação.

            Raises:
                ValueError: Se não houver processos finalizados.
        """
        return Metrics(self._engine.finished_processes).calculate()


    # ------------------------------------------------------------------
    # Propriedades somente leitura
    # ------------------------------------------------------------------
    @property
    def scheduler(self) -> BaseScheduler:
        """
        Scheduler atualmente configurado.
        """
        return self._scheduler

    @property
    def engine(self) -> SimulationEngine:
        """
        Engine de simulação atualmente associada ao controller.
        """
        return self._engine

    @property
    def gantt_timeline(self) -> list[GanttEntry]:
        """
        Timeline de Gantt acumulada pela engine.
        """
        return self._engine.gantt_timeline

    @property
    def finished_processes(self) -> list[Process]:
        """
        Processos finalizados, na ordem em que foram concluídos.
        """
        return self._engine.finished_processes