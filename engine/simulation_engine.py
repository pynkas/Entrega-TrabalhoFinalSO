"""
Núcleo da simulação de escalonamento de processos.

Define a estrutura GanttEntry e a classe SimulationEngine, responsável
por controlar o tempo, as filas, as transições de estado e o registro
da execução no diagrama de Gantt.

A Engine delega ao Scheduler apenas a escolha do próximo processo,
sem conhecer os detalhes de cada algoritmo de escalonamento.
"""

from dataclasses import dataclass, field
from models.process import Process, ProcessState
from schedulers.base_scheduler import BaseScheduler


# ---------------------------------------------------------------------------
# Estrutura de dados para o Gantt
# ---------------------------------------------------------------------------
@dataclass
class GanttEntry:
    """    
    Intervalo contínuo de execução de um processo no diagrama de Gantt.

    Uma nova entrada é criada quando um processo começa a executar ou
    retorna após uma preempção.
    """

    pid:        int
    name:       str
    tick_start: int
    tick_end:   int


# ---------------------------------------------------------------------------
# Motor da simulação
# ---------------------------------------------------------------------------
class SimulationEngine:
    """                             
    Motor central da simulação de escalonamento.

    Controla o relógio, as filas de processos, as transições de estado
    e a timeline do diagrama de Gantt. A escolha do próximo processo é
    delegada ao scheduler configurado.

    Args:
        processes: Lista de processos cadastrados na simulação.
        scheduler: Algoritmo de escalonamento utilizado.
    """

    def __init__(
        self,
        processes: list[Process],
        scheduler: BaseScheduler,
    ) -> None:
        # Referências externas
        self._scheduler:  BaseScheduler = scheduler
        self._processes:  list[Process] = processes

        # Relógio da simulação
        self.current_tick: int = 0

        # Filas e estado de execução
        self.ready_queue:        list[Process]  = []
        self.running_process:    Process | None = None
        self.finished_processes: list[Process]  = []

        # Timeline para o diagrama de Gantt
        self.gantt_timeline: list[GanttEntry] = []

        # Término
        self._is_finished: bool = False


    # ------------------------------------------------------------------
    # Propriedade de estado
    # ------------------------------------------------------------------
    @property
    def is_finished(self) -> bool:
        """
        Indica se não há processos em execução, prontos ou pendentes.
        """
        return self._is_finished


    # ------------------------------------------------------------------
    # Método principal: tick
    # ------------------------------------------------------------------
    def tick(self) -> None:
        """            
        Avança a simulação em uma unidade de tempo.

        Em cada tick, a Engine admite novos processos, executa o processo
        atual, aplica preempção quando necessário, seleciona o próximo processo,
        registra o Gantt e atualiza o estado de término da simulação.
        """
        if self._is_finished:
            return

        # Passo 1 - Admitir processos que chegam neste tick
        self._admit_arriving_processes()

        # Passo 2 - Processar o processo atualmente em execução
        if self.running_process is not None:
            self._execute_running_process()

        # Passo 3 - Selecionar próximo processo se a CPU está ociosa
        if self.running_process is None and self.ready_queue:
            self._select_next_process()

        # Passo 4 - Registrar este tick no Gantt
        if self.running_process is not None:
            self._record_gantt()

        # Passo 5 - Verificar término da simulação
        self._check_if_finished()

        # Passo 6 - Avançar o relógio (apenas se a simulação ainda continua)
        # Congelar current_tick no tick real de término garante que o valor
        # exibido na GUI e usado nas métricas reflita o tempo total correto.
        if not self._is_finished:
            self.current_tick += 1


    # ------------------------------------------------------------------
    # Passos internos do tick (privados)
    # ------------------------------------------------------------------
    def _admit_arriving_processes(self) -> None:
        """
        Move para a fila de prontos os processos que chegam no tick atual.
        """
        for process in self._processes:
            if (
                process.state == ProcessState.NEW
                and process.arrival_time == self.current_tick
            ):
                process.state = ProcessState.READY
                self.ready_queue.append(process)

    def _execute_running_process(self) -> None:
        """   
        Consome um tick do processo em execução.

        Se o processo terminar, move-o para FINISHED. Caso o scheduler indique
        preempção, o processo atual volta para a fila de prontos e libera a CPU.
        """
        process = self.running_process

        # Consumir um tick de CPU
        process.remaining_time -= 1

        # Caso 1: processo concluiu
        if process.is_finished():
            process.state       = ProcessState.FINISHED
            process.finish_time = self.current_tick
            self.finished_processes.append(process)
            self.running_process = None
            return

        # Caso 2: algoritmo preemptivo - perguntar ao Scheduler se deve
        # preemptar. should_preempt() é a única chamada neste tick para
        # decisão de interrupção; select_next() será chamado uma única
        # vez no Passo 3, caso running_process tenha sido liberado aqui.
        if self._scheduler.is_preemptive:
            if self._scheduler.should_preempt(
                process, self.ready_queue, self.current_tick
            ):
                process.state = ProcessState.READY
                self.ready_queue.append(process)
                self.running_process = None

    def _select_next_process(self) -> None:
        """
        Seleciona o próximo processo por meio do scheduler.
        Se houver um processo escolhido, ele é promovido para RUNNING.

        Chamado quando a CPU está ociosa e há processos disponíveis na
        fila de prontos.
        """
        selected = self._scheduler.select_next(
            self.ready_queue, self.current_tick
        )

        if selected is not None:
            self._promote_to_running(selected)

    def _promote_to_running(self, process: Process) -> None:
        """
        Promove um processo da fila de prontos para RUNNING.

        Registra start_time apenas na primeira execução e notifica o scheduler
        que um novo processo assumiu a CPU.
        """
        self.ready_queue.remove(process)
        process.state = ProcessState.RUNNING

        # Registrar start_time apenas na primeira vez que executa
        if process.start_time is None:
            process.start_time = self.current_tick

        # Notificar o scheduler que um novo processo assumiu a CPU.
        # O RoundRobinScheduler usa para zerar o contador de quantum,
        # garantindo quantum completo independente de como o processo
        # anterior terminou (preempção ou término natural).
        self._scheduler.on_process_started(process)

        self.running_process = process

    def _record_gantt(self) -> None:
        """
        Registra a execução atual na timeline de Gantt.

        Se o mesmo processo já ocupa o último intervalo, apenas estende
        tick_end; caso contrário, cria uma nova entrada.
        """
        process = self.running_process

        if (
            self.gantt_timeline
            and self.gantt_timeline[-1].pid == process.pid
        ):
            # Estender o intervalo existente
            self.gantt_timeline[-1].tick_end = self.current_tick + 1
        else:
            # Iniciar novo intervalo
            self.gantt_timeline.append(
                GanttEntry(
                    pid        = process.pid,
                    name       = process.name,
                    tick_start = self.current_tick,
                    tick_end   = self.current_tick + 1,
                )
            )

    def _check_if_finished(self) -> None:
        """
        Verifica se a simulação encerrou completamente.

        A simulação é considerada concluída quando as três condições
        abaixo são verdadeiras simultaneamente:
            1. Não há processo em execução (CPU ociosa ou concluiu).
            2. A fila de prontos está vazia.
            3. Nenhum processo está aguardando chegada (estado NEW).

        Essa última condição evita encerrar a simulação durante períodos de
        CPU ociosa antes da chegada de processos futuros.
        """
        no_running = self.running_process is None
        no_ready   = len(self.ready_queue) == 0
        no_pending = not any(
            p.state == ProcessState.NEW for p in self._processes
        )

        if no_running and no_ready and no_pending:
            self._is_finished = True


    # ------------------------------------------------------------------
    # Métodos de acesso ao estado (para o Controller e a GUI)
    # ------------------------------------------------------------------
    def get_ready_queue(self) -> list[Process]:
        """
        Retorna uma cópia da fila dos processos prontos.
        """
        return list(self.ready_queue)

    def get_finished_processes(self) -> list[Process]:
        """
        Retorna uma cópia da fila dos processos finalizados.
        """
        return list(self.finished_processes)

    def get_gantt_timeline(self) -> list[GanttEntry]:
        """
        Retorna uma cópia da timeline de Gantt acumulada.
        """
        return list(self.gantt_timeline)


    # ------------------------------------------------------------------
    # Reset
    # ------------------------------------------------------------------
    def reset(self) -> None:
        """  
        Restaura a Engine ao estado inicial.

        Limpa filas, processo em execução, Gantt, relógio e estado de término,
        além de resetar o scheduler. Os objetos Process não são resetados aqui;
        essa responsabilidade é do Controller.
        """
        self.current_tick        = 0
        self.ready_queue         = []
        self.running_process     = None
        self.finished_processes  = []
        self.gantt_timeline      = []
        self._is_finished        = False

        self._scheduler.reset()


    # ------------------------------------------------------------------
    # Representação textual
    # ------------------------------------------------------------------
    def __str__(self) -> str:
        """
        Retorna um resumo textual do estado atual da Engine.
        """
        running_name = (
            self.running_process.name
            if self.running_process
            else "–"
        )
        return (
            f"SimulationEngine("
            f"tick={self.current_tick}, "
            f"scheduler={self._scheduler.name!r}, "
            f"running={running_name!r}, "
            f"ready={len(self.ready_queue)}, "
            f"finished={len(self.finished_processes)}"
            f")"
        )