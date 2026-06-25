"""
Escalonador por prioridade não-preemptivo.

Seleciona o processo com menor valor numérico em priority (menor = maior
prioridade). Desempates por arrival_time e, em último caso, pela ordem
na ready_queue. Pode causar starvation em processos de baixa prioridade.
"""

from models.process import Process
from schedulers.base_scheduler import BaseScheduler


class PriorityScheduler(BaseScheduler):
    """
    Scheduler por prioridade não-preemptivo.

    Seleciona o processo com menor priority. Desempates por arrival_time
    e, se necessário, pela ordem na ready_queue. Cada decisão depende
    apenas dos argumentos de select_next().
    """


    # ------------------------------------------------------------------
    # Propriedades do contrato
    # ------------------------------------------------------------------
    @property
    def name(self) -> str:
        """
        Nome do algoritmo.
        """

        return "Priority"

    @property
    def is_preemptive(self) -> bool:
        """
        Indica que o scheduler por prioridade é não-preemptivo, não interrompe 
        processos em execução.
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
        Seleciona o processo com menor priority.

        Desempata por arrival_time, e caso necessário, pela ordem na ready_queue.
        Retorna None se a fila estiver vazia.
        """

        if not ready_queue:
            return None

        return min(
            ready_queue,
            key=lambda process: (process.priority, process.arrival_time),
        )

    def should_preempt(
        self,
        running_process: Process,
        ready_queue: list[Process],
        current_tick: int,
    ) -> bool:
        """
        Escalonamento por prioridades não realiza preempção; sempre retorna False.
        """

        return False


    # ------------------------------------------------------------------
    # Reset
    # ------------------------------------------------------------------
    def reset(self) -> None:
        """
        Não realiza nenhuma ação, pois não mantém estado interno.
        """