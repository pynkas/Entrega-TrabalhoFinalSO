"""
Implementação do algoritmo FIFO.

Seleciona primeiro o processo que chegou há mais tempo na fila de
prontos. É um algoritmo não-preemptivo: após receber a CPU, o processo
executa até terminar.
"""

from models.process import Process
from schedulers.base_scheduler import BaseScheduler


class FIFOScheduler(BaseScheduler):
    """
    Scheduler FIFO não-preemptivo.

    Seleciona o processo com menor arrival_time entre os prontos. Em caso
    de empate, preserva a ordem atual da ready_queue. Não mantém estado
    interno entre chamadas.
    """


    # ------------------------------------------------------------------
    # Propriedades do contrato
    # ------------------------------------------------------------------
    @property
    def name(self) -> str:
        """
        Nome do algoritmo.
        """

        return "FIFO"

    @property
    def is_preemptive(self) -> bool:
        """
        Indica que o FIFO é não-preemptivo, não interrompe processos em 
        execução.
        """

        return False


    # ------------------------------------------------------------------
    # Seleção do próximo processo
    # ------------------------------------------------------------------
    def select_next(
        self,
        ready_queue: list[Process],
        current_tick: int,
    ) -> Process | None:
        """
        Seleciona o processo com menor arrival_time.

        Se houver empate, min() preserva a ordem original da ready_queue,
        mantendo o comportamento FIFO entre processos que chegaram no mesmo tick.
        Retorna None se a fila estiver vazia.
        """

        if not ready_queue:
            return None

        return min(ready_queue, key=lambda process: process.arrival_time)

    def should_preempt(
        self,
        running_process: Process,
        ready_queue: list[Process],
        current_tick: int,
    ) -> bool:
        """
        FIFO não realiza preempção; sempre retorna False.
        """

        return False


    # ------------------------------------------------------------------
    # Reset
    # ------------------------------------------------------------------
    def reset(self) -> None:
        """
        Não realiza nenhuma ação, pois FIFO não mantém estado interno.
        """