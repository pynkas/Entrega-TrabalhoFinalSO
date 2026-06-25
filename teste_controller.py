from models.process import Process
from schedulers.fifo import FIFOScheduler
from schedulers.round_robin import RoundRobinScheduler
from controller.simulation_controller import SimulationController


# ------------------------------------------------------------------
# Processos de teste
# ------------------------------------------------------------------
p1 = Process(pid=1, name="P1", arrival_time=0, burst_time=4, priority=1)
p2 = Process(pid=2, name="P2", arrival_time=0, burst_time=1, priority=2)
p3 = Process(pid=3, name="P3", arrival_time=2, burst_time=6, priority=3)
p4 = Process(pid=4, name="P4", arrival_time=2, burst_time=2, priority=1)
p5 = Process(pid=5, name="P5", arrival_time=7, burst_time=1, priority=2)
p6 = Process(pid=6, name="P6", arrival_time=10, burst_time=3, priority=3)

controller = SimulationController(
    processes=[p1, p2, p3, p4, p5, p6],
    scheduler=RoundRobinScheduler(quantum=3),
)

metrics = controller.run()

print("\n=== PROCESSOS FINALIZADOS ===\n")

for process in controller.finished_processes:
    print(
        f"{process.name}"
        f" | start={process.start_time}"
        f" | finish={process.finish_time}"
        f" | burst={process.burst_time}"
    )

print("\n=== GANTT ===\n")

for entry in controller.gantt_timeline:
    print(entry)

print("\n=== MÉTRICAS INDIVIDUAIS ===\n")

for metric in metrics.process_metrics:
    print(
        f"{metric.name}"
        f" | turnaround={metric.turnaround_time}"
        f" | waiting={metric.waiting_time}"
    )

print("\n=== MÉDIAS ===\n")

print(
    f"Average Turnaround: "
    f"{metrics.avg_turnaround_time:.2f}"
)

print(
    f"Average Waiting: "
    f"{metrics.avg_waiting_time:.2f}"
)

print("\n=== TESTANDO RESET ===\n")

controller.reset()

metrics = controller.run()

print(
    f"Processos finalizados após reset: "
    f"{len(controller.finished_processes)}"
)

print(
    f"Average Waiting: "
    f"{metrics.avg_waiting_time:.2f}"
)