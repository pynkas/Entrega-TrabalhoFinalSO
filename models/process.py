"""
Define as estruturas que representam um processo simulado.

Inclui o enum ProcessState, com os estados do ciclo de vida, e a
dataclass Process, que armazena os dados e o estado de execução
de um processo no simulador.
"""

from dataclasses import dataclass, field
from enum import Enum, auto


# ---------------------------------------------------------------------------
# Enum de estados
# ---------------------------------------------------------------------------
class ProcessState(Enum):
    """          
    Estados possíveis de um processo no simulador.

    Transições válidas:
        NEW --> READY --> RUNNING --> FINISHED
                  ^           |
                  |___________|  (retorno para fila em algoritmos preemptivos)
    """

    NEW      = auto()
    READY    = auto()
    RUNNING  = auto()
    FINISHED = auto()

@dataclass
class Process:
    """    
    Representa um processo simulado no escalonador de CPU.

    Armazena os dados e o estado de execução do processo, sem conter
    lógica de escalonamento ou cálculo de métricas.
    """
    
    pid: int
    name: str
    arrival_time: int

    # Tempo total de CPU necessário; permanece fixo após a criação.
    burst_time: int

    # Menor valor indica maior prioridade. Usado pelo PriorityScheduler.
    priority: int


    # ------------------------------------------------------------------
    # Atributos gerenciados internamente (com valores padrão via field)
    # ------------------------------------------------------------------
    
    # Tempo restante de execução, inicializado com burst_time.
    remaining_time: int = field(init=False)

    # Estado atual do processo na simulação.
    state: ProcessState = field(init=False)

    # Tick da primeira entrada em RUNNING.
    start_time: int | None = field(init=False)

    # Tick de conclusão do processo.
    finish_time: int | None = field(init=False)

    def __post_init__(self) -> None:
        """
        Valida os dados de entrada e inicializa os atributos internos.

        Raises:
            ValueError: Se algum atributo informado for inválido.
        """

        self._validate()
        self.remaining_time = self.burst_time
        self.state          = ProcessState.NEW
        self.start_time     = None
        self.finish_time    = None

    def _validate(self) -> None:
        """
        Valida os atributos básicos do processo.

        Raises:
            ValueError: Se nome, burst_time, arrival_time ou priority forem inválidos.
        """
        
        if not self.name or not self.name.strip():
            raise ValueError(
                f"O nome do processo não pode ser vazio. "
                f"Valor recebido: {self.name!r}"
            )

        if self.burst_time <= 0:
            raise ValueError(
                f"burst_time deve ser maior que zero. "
                f"Valor recebido: {self.burst_time}"
            )

        if self.arrival_time < 0:
            raise ValueError(
                f"arrival_time não pode ser negativo. "
                f"Valor recebido: {self.arrival_time}"
            )

        if self.priority < 0:
            raise ValueError(
                f"priority não pode ser negativa. "
                f"Valor recebido: {self.priority}"
            )


    # ------------------------------------------------------------------
    # Métodos públicos
    # ------------------------------------------------------------------
    def reset(self) -> None:
        """    
        Restaura o processo ao estado inicial da simulação.

        Reinicia remaining_time, state, start_time e finish_time, preservando
        os dados originais de cadastro.
        """

        self.remaining_time = self.burst_time
        self.state          = ProcessState.NEW
        self.start_time     = None
        self.finish_time    = None

    def is_finished(self) -> bool:
        """
        Indica se o processo já consumiu todo o seu tempo de CPU.
        """
        return self.remaining_time <= 0

    def __str__(self) -> str:
        """
        Retorna uma representação textual resumida do processo.
        """
        return (
            f"Process("
            f"pid={self.pid}, "
            f"name={self.name!r}, "
            f"state={self.state.name}"
            f")"
        )

    def __repr__(self) -> str:
        """
        Retorna uma representação textual detalhada do processo.
        """
        return (
            f"Process("
            f"pid={self.pid}, "
            f"name={self.name!r}, "
            f"arrival_time={self.arrival_time}, "
            f"burst_time={self.burst_time}, "
            f"remaining_time={self.remaining_time}, "
            f"priority={self.priority}, "
            f"state={self.state.name}, "
            f"start_time={self.start_time}, "
            f"finish_time={self.finish_time}"
            f")"
        )