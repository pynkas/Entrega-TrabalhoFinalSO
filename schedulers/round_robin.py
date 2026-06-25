"""
Escalonador Round Robin (preemptivo) com quantum configurável.

Cada processo usa a CPU por até quantum ticks; ao expirar sem finalizar,
o processo é colocado no fim da fila de prontos. Valores menores de quantum
aumentam trocas de contexto; valores maiores aproximam FIFO.
"""

from models.process import Process
from schedulers.base_scheduler import BaseScheduler


class RoundRobinScheduler(BaseScheduler):
    """
    Scheduler Round Robin com quantum configurável.
    
    Mantém um contador interno de ticks usados pelo processo atual. A
    preempção ocorre quando esse contador atinge o quantum e há outro
    processo aguardando na fila de prontos.
    
    Args:
        quantum: Número máximo de ticks consecutivos por processo.
    
    Raises:
        ValueError: Se quantum for menor ou igual a zero.
        """
    
    def __init__(self, quantum: int) -> None:
        if quantum <= 0:
            raise ValueError(
                f"O quantum deve ser maior que zero. "
                f"Valor recebido: {quantum}"
            )

        self._quantum:     int = quantum
        self._ticks_used:  int = 0


    # ------------------------------------------------------------------
    # Propriedades do contrato
    # ------------------------------------------------------------------
    @property
    def name(self) -> str:
        """
        Nome do algoritmo e o valor do quantum.
        """

        return f"Round Robin (q={self._quantum})"

    @property
    def is_preemptive(self) -> bool:
        """
        Indica que o Round Robin é preemptivo.

        A Engine usará essa propriedade para chamar should_preempt()
        a cada tick enquanto houver um processo em execução.
        """

        return True


    # ------------------------------------------------------------------
    # Início de processo
    # ------------------------------------------------------------------
    def on_process_started(self, process: Process) -> None:
        """
        Reseta o contador de ticks do quantum quando um novo processo
        assume a CPU.
        """

        self._ticks_used = 0


    # ------------------------------------------------------------------
    # Decisão de preempção
    # ------------------------------------------------------------------
    def should_preempt(
        self,
        running_process: Process,
        ready_queue: list[Process],
        current_tick: int,
    ) -> bool:
        """
        Verifica se o quantum do processo atual expirou e sinaliza preempção.

        Incrementa _ticks_used; se _ticks_used >= _quantum, zera o contador
        e retorna True apenas se houver outro processo na ready_queue.
        Caso contrário, retorna False.
        """

        self._ticks_used += 1

        if self._ticks_used >= self._quantum:
            self._ticks_used = 0
            # Só preempta se há outro processo aguardando.
            # Fila vazia significa que não há benefício em interromper.
            return len(ready_queue) > 0

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
        Retorna o primeiro processo da ready_queue ou None se vazia.
        Não altera _ticks_used; a Engine continua a rotação.
        """

        if not ready_queue:
            return None

        return ready_queue[0]


    # ------------------------------------------------------------------
    # Reset
    # ------------------------------------------------------------------
    def reset(self) -> None:
        """
        Restaura o estado do scheduler para o início da simulação.
        Zera _ticks_used. O valor de _quantum é preservado.
        """
        
        self._ticks_used = 0
