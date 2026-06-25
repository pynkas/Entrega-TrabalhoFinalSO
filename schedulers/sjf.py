"""
Escalonador SJF não-preemptivo, 

Seleciona o processo com menor burst_time. Desempates por menor arrival_time 
e, em último caso, pela posição na ready_queue.
"""

from models.process import Process
from schedulers.base_scheduler import BaseScheduler


class SJFScheduler(BaseScheduler):
    """
    Algoritmo de escalonamento SJF não-preemptivo (Shortest Job First).

    Seleciona sempre o processo com o menor burst_time entre os que estão
    na fila de prontos no momento em que a CPU fica disponível.

    Critério de seleção (em ordem de prioridade):
        1. Menor burst_time.
        2. Menor arrival_time (desempate).
        3. Posição original na ready_queue (desempate final).
    """


    # ------------------------------------------------------------------
    # Propriedades do contrato
    # ------------------------------------------------------------------
    @property
    def name(self) -> str:
        """
        Nome do algoritmo.
        """

        return "SJF"

    @property
    def is_preemptive(self) -> bool:
        """
        Indica que o SJF é não-preemptivo, não interrompe processos em 
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
        Retorna o processo com menor burst_time, e então arrival_time, ou None se vazia.

        Não modifica a ready_queue; empates respeitam a ordem atual da lista.
        """

        if not ready_queue:
            return None

        return min(
            ready_queue,
            key=lambda process: (process.burst_time, process.arrival_time),
        )

    def should_preempt(
        self,
        running_process: Process,
        ready_queue: list[Process],
        current_tick: int,
    ) -> bool:
        """
        SJF não realiza preempção; sempre retorna False.
        """

        return False


    # ------------------------------------------------------------------
    # Reset
    # ------------------------------------------------------------------
    def reset(self) -> None:
        """
        Não realiza nenhuma ação, pois SJF não mantém estado interno.
        """