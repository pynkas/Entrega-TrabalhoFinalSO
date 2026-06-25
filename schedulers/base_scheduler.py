"""
Define o contrato abstrato dos algoritmos de escalonamento.

BaseScheduler estabelece a interface comum para os schedulers concretos.
Cada scheduler decide qual processo deve executar a partir da fila de
prontos, enquanto o controle de tempo, filas e estados permanece na
SimulationEngine.
"""

from abc import ABC, abstractmethod
from models.process import Process


# ---------------------------------------------------------------------------
# Classe abstrata
# ---------------------------------------------------------------------------
class BaseScheduler(ABC):
    """
    Classe base abstrata para algoritmos de escalonamento de CPU.

    Subclasses devem implementar a política de seleção do próximo processo,
    indicar se são preemptivas, expor um nome legível e restaurar seu estado
    interno quando necessário.

    A Engine permanece responsável por tempo, filas, estados dos processos
    e registro da simulação.
    """


    # ------------------------------------------------------------------
    # Método abstrato principal
    # ------------------------------------------------------------------
    @abstractmethod
    def select_next(
        self,
        ready_queue: list[Process],
        current_tick: int,
    ) -> Process | None:
        """
        Seleciona o próximo processo a executar.

        O método deve apenas escolher e retornar um processo da fila de prontos,
        sem remover itens da fila, alterar estados ou atualizar tempos. Essas
        operações pertencem à SimulationEngine.

        Args:
            ready_queue: Processos disponíveis para execução.
            current_tick: Tick atual da simulação.

        Returns:
            Processo selecionado ou None se não houver processo disponível.
        """


    # ------------------------------------------------------------------
    # Método abstrato: decisão de preempção
    # ------------------------------------------------------------------
    @abstractmethod
    def should_preempt(
        self,
        running_process: Process,
        ready_queue: list[Process],
        current_tick: int,
    ) -> bool:
        """
        Indica se o processo em execução deve ser interrompido.

        Usado pela Engine apenas em algoritmos preemptivos. Schedulers
        não-preemptivos implementam este método retornando False.

        Args:
            running_process: Processo atualmente executando.
            ready_queue: Fila de processos prontos.
            current_tick: Tick atual da simulação.

        Returns:
            True se o processo deve ser preemptado; caso contrário, False.
        """


    # ------------------------------------------------------------------
    # Método concreto: início de processo
    # ------------------------------------------------------------------
    def on_process_started(self, process: Process) -> None:
        """
        Chamado quando um processo assume a CPU.

        A implementação padrão não faz nada. Schedulers com estado interno (RR)
        podem sobrescrever este método para reinicializar controles próprios.

        Args:
            process: Processo que acabou de assumir a CPU.
        """


    # ------------------------------------------------------------------
    # Método abstrato de reset
    # ------------------------------------------------------------------
    @abstractmethod
    def reset(self) -> None:
        """
        Restaura o estado interno do scheduler.

        Schedulers sem estado implementam este método como operação vazia.
        Schedulers com estado, como os baseados em quantum (RR), devem limpar seus
        controles internos para uma nova simulação.
        """


    # ------------------------------------------------------------------
    # Propriedade abstrata: preempção
    # ------------------------------------------------------------------
    @property
    @abstractmethod
    def is_preemptive(self) -> bool:
        """
        Indica se o algoritmo pode interromper um processo antes do término.

        A Engine usa esta propriedade para decidir se deve verificar preempção
        durante a execução de cada tick.
        """


    # ------------------------------------------------------------------
    # Propriedade abstrata: nome
    # ------------------------------------------------------------------
    @property
    @abstractmethod
    def name(self) -> str:
        """
        Nome legível do algoritmo de escalonamento.
        """


    # ------------------------------------------------------------------
    # Método concreto: representação textual
    # ------------------------------------------------------------------
    def __str__(self) -> str:
        """
        Retorna uma representação textual do scheduler.
        """
        
        return (
            f"Scheduler("
            f"name={self.name!r}, "
            f"preemptive={self.is_preemptive}"
            f")"
        )