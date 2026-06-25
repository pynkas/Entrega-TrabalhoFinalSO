from models.process import Process
from schedulers.round_robin import RoundRobinScheduler
from engine.simulation_engine import SimulationEngine


# ------------------------------------------------------------------
# Processos de teste
# ------------------------------------------------------------------
p1 = Process(pid=1, name="P1", arrival_time=0, burst_time=4, priority=1)
p2 = Process(pid=2, name="P2", arrival_time=0, burst_time=1, priority=2)
p3 = Process(pid=3, name="P3", arrival_time=2, burst_time=6, priority=3)
p4 = Process(pid=4, name="P4", arrival_time=2, burst_time=2, priority=1)
p5 = Process(pid=5, name="P5", arrival_time=7, burst_time=1, priority=2)
p6 = Process(pid=6, name="P6", arrival_time=10, burst_time=3, priority=3)

scheduler = RoundRobinScheduler(
    quantum=2
)

engine = SimulationEngine(
    processes=[p1, p2, p3, p4, p5, p6],
    scheduler=scheduler
)

print("=== INÍCIO DA SIMULAÇÃO ===\n")

while not engine.is_finished:

    print(f"Tick: {engine.current_tick}")

    if engine.running_process:
        print(f"CPU: {engine.running_process.name}")
    else:
        print("CPU: OCIOSA")

    print(
        "Ready Queue:",
        [p.name for p in engine.ready_queue]
    )

    print(
        "Finished:",
        [p.name for p in engine.finished_processes]
    )

    print()

    engine.tick()

print("=== FIM DA SIMULAÇÃO ===\n")

print("Processos finalizados:\n")

for process in engine.finished_processes:
    print(
        f"{process.name} | "
        f"start={process.start_time} | "
        f"finish={process.finish_time} | "
        f"burst={process.burst_time}"
    )

print("\nTimeline/Gantt:\n")

for entry in engine.gantt_timeline:
    print(entry)