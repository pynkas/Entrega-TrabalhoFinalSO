"""
    Cálculo de métricas de desempenho da simulação.

    Define estruturas imutáveis para métricas individuais e agregadas,
    além da classe Metrics, responsável por calcular turnaround time,
    waiting time e médias gerais a partir de processos finalizados.
"""

from dataclasses import dataclass
from models.process import Process


# ---------------------------------------------------------------------------
# Estruturas de resultado
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class ProcessMetrics:
    """
    Métricas individuais de um processo finalizado.

    Inclui tempos de chegada, execução, início, término, turnaround e
    espera. A estrutura é imutável para preservar os resultados calculados (frozen=true).
    """

    pid:             int
    name:            str
    arrival_time:    int
    burst_time:      int
    start_time:      int
    finish_time:     int
    turnaround_time: int
    waiting_time:    int

@dataclass(frozen=True)
class SimulationMetrics:
    """
    Métricas agregadas de uma simulação.

    Armazena as métricas individuais dos processos e as médias gerais
    de turnaround e waiting time. A estrutura é imutável para preservar 
    os resultados calculados (frozen=true).
    """

    process_metrics:     tuple[ProcessMetrics, ...]
    avg_turnaround_time: float
    avg_waiting_time:    float


# ---------------------------------------------------------------------------
# Calculadora de métricas
# ---------------------------------------------------------------------------
class Metrics:
    """
    Calcula métricas de desempenho a partir de processos finalizados.

    A classe apenas lê os atributos dos processos recebidos e retorna um
    SimulationMetrics com métricas individuais e médias gerais.
    """

    def __init__(self, finished_processes: list[Process]) -> None:
        self._processes: list[Process] = finished_processes


    # ------------------------------------------------------------------
    # Método principal
    # ------------------------------------------------------------------
    def calculate(self) -> SimulationMetrics:
        """            
        Calcula as métricas individuais e médias da simulação.

        Returns:
            Resultado completo com métricas por processo e médias gerais.

        Raises:
            ValueError: Se a lista estiver vazia ou algum processo não tiver
                start_time ou finish_time definidos.
        """

        self._validate()

        individual = tuple(
            self._calculate_process_metrics(process)
            for process in self._processes
        )

        avg_turnaround = (
            sum(m.turnaround_time for m in individual) / len(individual)
        )
        avg_waiting = (
            sum(m.waiting_time for m in individual) / len(individual)
        )

        return SimulationMetrics(
            process_metrics     = individual,
            avg_turnaround_time = avg_turnaround,
            avg_waiting_time    = avg_waiting,
        )


    # ------------------------------------------------------------------
    # Cálculo individual
    # ------------------------------------------------------------------
    def _calculate_process_metrics(self, process: Process) -> ProcessMetrics:
        """
        Calcula as métricas individuais de um processo finalizado.

        Fórmulas:
            turnaround_time = finish_time - arrival_time
            waiting_time = turnaround_time - burst_time
        """

        turnaround_time = process.finish_time - process.arrival_time
        waiting_time    = turnaround_time - process.burst_time

        return ProcessMetrics(
            pid             = process.pid,
            name            = process.name,
            arrival_time    = process.arrival_time,
            burst_time      = process.burst_time,
            start_time      = process.start_time,
            finish_time     = process.finish_time,
            turnaround_time = turnaround_time,
            waiting_time    = waiting_time,
        )


    # ------------------------------------------------------------------
    # Validação
    # ------------------------------------------------------------------
    def _validate(self) -> None:
        """
        Valida se há processos finalizados aptos ao cálculo.

        Raises:
            ValueError: Se a lista estiver vazia ou algum processo não tiver
                start_time ou finish_time definidos.
        """
        
        if not self._processes:
            raise ValueError(
                "Não é possível calcular métricas: "
                "a lista de processos finalizados está vazia."
            )

        for process in self._processes:
            if process.finish_time is None:
                raise ValueError(
                    f"O processo '{process.name}' (pid={process.pid}) "
                    f"não possui finish_time definido. "
                    f"Apenas processos finalizados devem ser passados "
                    f"para o cálculo de métricas."
                )
            if process.start_time is None:
                raise ValueError(
                    f"O processo '{process.name}' (pid={process.pid}) "
                    f"não possui start_time definido. "
                    f"Apenas processos finalizados devem ser passados "
                    f"para o cálculo de métricas."
                )