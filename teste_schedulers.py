from models.process import Process
from schedulers.fifo import FIFOScheduler
from schedulers.sjf import SJFScheduler
from schedulers.priority import PriorityScheduler
from engine.simulation_engine import SimulationEngine


def print_engine_state(engine: SimulationEngine) -> None:
    """
    Exibe o estado atual da simulação.
    """

    print(f"\nTick: {engine.current_tick}")

    if engine.running_process:
        print(f"CPU: {engine.running_process.name}")
    else:
        print("CPU: OCIOSA")

    print(
        "Ready Queue:",
        [process.name for process in engine.ready_queue]
    )

    print(
        "Finished:",
        [process.name for process in engine.finished_processes]
    )


# ------------------------------------------------------------------
# Processos de teste
# ------------------------------------------------------------------
p1 = Process(pid=1, name="P1", arrival_time=0, burst_time=4, priority=1)
p2 = Process(pid=2, name="P2", arrival_time=0, burst_time=1, priority=2)
p3 = Process(pid=3, name="P3", arrival_time=2, burst_time=6, priority=3)
p4 = Process(pid=4, name="P4", arrival_time=2, burst_time=2, priority=1)
p5 = Process(pid=5, name="P5", arrival_time=7, burst_time=1, priority=2)
p6 = Process(pid=6, name="P6", arrival_time=10, burst_time=3, priority=3)


# ------------------------------------------------------------------
# Scheduler
# Caso necessário, alterar:
# scheduler = FIFOScheduler()
# scheduler = PriorityScheduler()
# scheduler = SJFScheduler()
# Teste para Round Robin está arquivo separado.
# ------------------------------------------------------------------
scheduler = FIFOScheduler()


# ------------------------------------------------------------------
# Engine
# ------------------------------------------------------------------
engine = SimulationEngine(
    processes=[p1, p2, p3, p4, p5, p6],
    scheduler=scheduler,
)


# ------------------------------------------------------------------
# Simulação
# ------------------------------------------------------------------
print("\n=== INÍCIO DA SIMULAÇÃO ===")

print_engine_state(engine)

while not engine.is_finished:

    engine.tick()

    print_engine_state(engine)

print("\n=== FIM DA SIMULAÇÃO ===")


# ------------------------------------------------------------------
# Resultados finais
# ------------------------------------------------------------------
print("\nProcessos finalizados:\n")

for process in engine.get_finished_processes():

    print(
        f"{process.name} | "
        f"start={process.start_time} | "
        f"finish={process.finish_time} | "
        f"burst={process.burst_time}"
    )


# ------------------------------------------------------------------
# Gantt
# ------------------------------------------------------------------
print("\nTimeline/Gantt:\n")

try:
    for entry in engine.gantt_timeline:
        print(entry)

except AttributeError:
    print(
        "Atributo gantt_timeline não encontrado. "
        "Verifique o nome utilizado na SimulationEngine."
    )