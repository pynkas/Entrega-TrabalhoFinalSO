import threading
import tkinter as tk
from tkinter import ttk, messagebox

from models.process import Process
from controller.simulation_controller import SimulationController
from schedulers.fifo import FIFOScheduler
from schedulers.sjf import SJFScheduler
from schedulers.priority import PriorityScheduler
from schedulers.round_robin import RoundRobinScheduler


# -------------------------
# Utilitários de desenho
# -------------------------
_PALETTE = [
    "#1f77b4", "#ff7f0e", "#2ca02c", "#d62728",
    "#9467bd", "#8c564b", "#e377c2", "#7f7f7f",
    "#bcbd22", "#17becf"
]

def pid_to_color_map(pids):
    """
    Gera um mapeamento PID -> cor a partir de uma paleta fixa.

    Recebe uma lista de PIDs (possivelmente com repetições) e retorna
    um dicionário com uma cor consistente para cada PID único.
    """

    unique = sorted(set(pids))
    mapping = {}
    for i, pid in enumerate(unique):
        mapping[pid] = _PALETTE[i % len(_PALETTE)]
    return mapping

def draw_gantt_on_canvas(canvas: tk.Canvas, gantt_timeline, width, height):
    """
    Desenha um gráfico de Gantt simples no canvas fornecido.

    - gantt_timeline é uma sequência de segmentos com atributos
      tick_start, tick_end, pid e name.
    - A função escala horizontalmente para caber em width e desenha
      retângulos coloridos e marcas de tempo.
    - Limpa o canvas antes de desenhar; se a timeline estiver vazia,
      exibe uma mensagem indicativa.
    """

    canvas.delete("all")
    if not gantt_timeline:
        canvas.create_text(width//2, height//2, text="Gráfico de Gantt (vazio)", fill="gray")
        return

    # calcular escala de tempo
    max_end = max(entry.tick_end for entry in gantt_timeline)
    margin = 20
    usable_w = max(100, width - 2*margin)
    scale = usable_w / (max_end if max_end > 0 else 1)

    # cores por pid
    pids = [e.pid for e in gantt_timeline]
    color_map = pid_to_color_map(pids)

    y = height // 2
    bar_height = 30
    for seg in gantt_timeline:
        x0 = margin + seg.tick_start * scale
        x1 = margin + seg.tick_end * scale
        color = color_map.get(seg.pid, "#333333")
        # retângulo
        canvas.create_rectangle(x0, y - bar_height//2, x1, y + bar_height//2, fill=color, outline="black")
        # texto central (nome)
        canvas.create_text((x0 + x1)/2, y, text=seg.name, fill="white")

    # eixo de tempo simples
    for t in range(0, max_end + 1):
        x = margin + t * scale
        canvas.create_line(x, y + bar_height//2 + 5, x, y + bar_height//2 + 10, fill="black")
        canvas.create_text(x, y + bar_height//2 + 20, text=str(t), fill="black", font=("TkDefaultFont", 8))


# -------------------------
# App principal
# -------------------------
DEFAULT_WINDOW_SIZE = "1000x600"

class SchedulerFactory:
    """
    Fábrica simples para instanciar schedulers por nome.

    Uso: SchedulerFactory.create("Round Robin", quantum=4)
    Lança ValueError para nomes desconhecidos ou falta de parâmetros.
    """

    @staticmethod
    def create(name: str, quantum: int | None = None):
        if name == "FIFO":
            return FIFOScheduler()
        if name == "SJF":
            return SJFScheduler()
        if name == "Priority":
            return PriorityScheduler()
        if name == "Round Robin":
            if quantum is None:
                raise ValueError("Quantum requerido para Round Robin")
            return RoundRobinScheduler(quantum)
        raise ValueError(f"Scheduler desconhecido: {name}")

class App(tk.Tk):
    """
    Aplicação GUI principal do simulador de escalonamento.

    Responsabilidades principais:
    - Permitir adicionar/remover processos.
    - Selecionar algoritmo e parâmetros (ex.: quantum).
    - Executar a simulação em thread separada e exibir o Gantt e métricas.
    """

    def __init__(self):
        super().__init__()
        self.title("Simulador de Escalonamento - GUI")
        self.geometry(DEFAULT_WINDOW_SIZE)

        self._process_list: list[Process] = []
        self._next_pid = 1
        self._run_thread: threading.Thread | None = None

        self._create_widgets()

    def _create_widgets(self):
        """
        Constrói e organiza todos os widgets da interface.

        Método interno; não deve ser chamado externamente após a inicialização.
        """

        main = ttk.Frame(self)
        main.pack(fill="both", expand=True, padx=8, pady=8)

        left = ttk.Frame(main)
        left.pack(side="left", fill="y", padx=(0,8))

        # Treeview de processos
        self.tree = ttk.Treeview(left, columns=("pid","name","arrival","burst","priority"), show="headings", height=12)
        for col, w in (("pid",40), ("name",140), ("arrival",80), ("burst",80), ("priority",80)):
            self.tree.heading(col, text=col.capitalize())
            self.tree.column(col, width=w, anchor="center")
        self.tree.pack(pady=6)

        # Formulário adicionar processo
        form = ttk.LabelFrame(left, text="Adicionar processo")
        form.pack(fill="x", pady=6)

        ttk.Label(form, text="Nome").grid(row=0, column=0, sticky="w", padx=4, pady=2)
        self.entry_name = ttk.Entry(form, width=18)
        self.entry_name.grid(row=0, column=1, padx=4, pady=2)

        ttk.Label(form, text="Arrival").grid(row=1, column=0, sticky="w", padx=4, pady=2)
        self.entry_arrival = ttk.Entry(form, width=8)
        self.entry_arrival.grid(row=1, column=1, sticky="w", padx=4, pady=2)

        ttk.Label(form, text="Burst").grid(row=2, column=0, sticky="w", padx=4, pady=2)
        self.entry_burst = ttk.Entry(form, width=8)
        self.entry_burst.grid(row=2, column=1, sticky="w", padx=4, pady=2)

        ttk.Label(form, text="Priority").grid(row=3, column=0, sticky="w", padx=4, pady=2)
        self.entry_priority = ttk.Entry(form, width=8)
        self.entry_priority.grid(row=3, column=1, sticky="w", padx=4, pady=2)
        self.entry_priority.insert(0, "0")

        btns = ttk.Frame(left)
        btns.pack(pady=6)
        ttk.Button(btns, text="Adicionar", command=self.on_add).grid(row=0, column=0, padx=4)
        ttk.Button(btns, text="Remover selecionado", command=self.on_remove).grid(row=0, column=1, padx=4)

        # Controles do scheduler
        sched_frame = ttk.LabelFrame(left, text="Scheduler")
        sched_frame.pack(fill="x", pady=6)

        ttk.Label(sched_frame, text="Algoritmo").grid(row=0, column=0, padx=4, pady=2, sticky="w")
        self.scheduler_var = tk.StringVar(value="FIFO")
        self.scheduler_combo = ttk.Combobox(sched_frame, textvariable=self.scheduler_var, state="readonly",
                                            values=["FIFO","SJF","Priority","Round Robin"])
        self.scheduler_combo.grid(row=0, column=1, padx=4, pady=2)
        self.scheduler_combo.bind("<<ComboboxSelected>>", self._on_scheduler_change)

        ttk.Label(sched_frame, text="Quantum").grid(row=1, column=0, padx=4, pady=2, sticky="w")
        self.entry_quantum = ttk.Entry(sched_frame, width=8)
        self.entry_quantum.grid(row=1, column=1, padx=4, pady=2)
        self.entry_quantum.insert(0, "4")
        self.entry_quantum.configure(state="disabled")

        # Run / Reset
        action_frame = ttk.Frame(left)
        action_frame.pack(pady=8)
        self.btn_run = ttk.Button(action_frame, text="Run", command=self.on_run)
        self.btn_run.grid(row=0, column=0, padx=6)
        self.btn_reset = ttk.Button(action_frame, text="Reset", command=self.on_reset, state="disabled")
        self.btn_reset.grid(row=0, column=1, padx=6)

        # Right: Canvas e métricas
        right = ttk.Frame(main)
        right.pack(side="right", fill="both", expand=True)

        # Canvas para Gantt
        self.canvas = tk.Canvas(right, bg="white")
        self.canvas.pack(fill="both", expand=True)

        # Métricas
        metrics_frame = ttk.LabelFrame(right, text="Métricas")
        metrics_frame.pack(fill="x", pady=6)
        self.lbl_avg_turn = ttk.Label(metrics_frame, text="Avg Turnaround: –")
        self.lbl_avg_turn.pack(anchor="w", padx=6, pady=2)
        self.lbl_avg_wait = ttk.Label(metrics_frame, text="Avg Waiting: –")
        self.lbl_avg_wait.pack(anchor="w", padx=6, pady=2)

    def _on_scheduler_change(self, _ev=None):
        """
        Habilita/desabilita o campo de quantum quando Round Robin é selecionado.
        """

        if self.scheduler_var.get() == "Round Robin":
            self.entry_quantum.configure(state="normal")
        else:
            self.entry_quantum.configure(state="disabled")

    def on_add(self):
        """
        Valida campos e adiciona um novo processo à lista e à Treeview.

        Gera um novo PID incremental e limpa o formulário após a inserção.
        """

        name = self.entry_name.get().strip()
        try:
            arrival = int(self.entry_arrival.get())
            burst = int(self.entry_burst.get())
            priority = int(self.entry_priority.get())
        except ValueError:
            messagebox.showerror("Erro", "Arrival, Burst e Priority devem ser inteiros")
            return

        if not name:
            messagebox.showerror("Erro", "Nome do processo não pode ser vazio")
            return
        if burst <= 0 or arrival < 0 or priority < 0:
            messagebox.showerror("Erro", "Valores inválidos: arrival>=0, burst>0, priority>=0")
            return

        pid = self._next_pid
        self._next_pid += 1
        proc = Process(pid=pid, name=name, arrival_time=arrival, burst_time=burst, priority=priority)
        self._process_list.append(proc)
        self.tree.insert("", "end", iid=str(pid), values=(pid, name, arrival, burst, priority))

        # limpar campos
        self.entry_name.delete(0, "end")
        self.entry_arrival.delete(0, "end")
        self.entry_burst.delete(0, "end")
        self.entry_priority.delete(0, "end")
        self.entry_priority.insert(0, "0")

    def on_remove(self):
        """
        Remove processos selecionados na Treeview da lista interna.
        """

        sel = self.tree.selection()
        if not sel:
            return
        for iid in sel:
            pid = int(iid)
            self._process_list = [p for p in self._process_list if p.pid != pid]
            self.tree.delete(iid)

    def on_run(self):
        """
        Inicia a simulação em uma thread separada.

        - Valida entrada (incluindo quantum para Round Robin).
        - Desabilita controles da UI enquanto a simulação roda.
        - Cria uma cópia dos processos para não alterar o estado da GUI.
        - Executa SimulationController.run() em thread daemon e atualiza a UI via self.after().
        """

        if not self._process_list:
            messagebox.showwarning("Aviso", "Adicione pelo menos um processo antes de executar")
            return

        sched_name = self.scheduler_var.get()
        quantum = None
        if sched_name == "Round Robin":
            try:
                quantum = int(self.entry_quantum.get())
                if quantum <= 0:
                    raise ValueError()
            except Exception:
                messagebox.showerror("Erro", "Quantum inválido")
                return

        self._set_controls_state(running=True)

        processes_copy = [
            Process(pid=p.pid, name=p.name, arrival_time=p.arrival_time, burst_time=p.burst_time, priority=p.priority)
            for p in self._process_list
        ]

        def worker():
            try:
                scheduler = SchedulerFactory.create(sched_name, quantum)
                controller = SimulationController(processes_copy, scheduler)
                metrics = controller.run()
                gantt = controller.gantt_timeline
                self.after(0, lambda: self._on_simulation_finished(gantt, metrics))
            except Exception as e:
                self.after(0, lambda: messagebox.showerror("Erro na simulação", str(e)))
                self.after(0, lambda: self._set_controls_state(running=False))

        self._run_thread = threading.Thread(target=worker, daemon=True)
        self._run_thread.start()

    def _on_simulation_finished(self, gantt, metrics):
        """
        Atualiza a UI com o Gantt e as métricas após a simulação.

        Chamado via self.after() a partir da thread de simulação.
        """

        w = self.canvas.winfo_width() or 800
        h = self.canvas.winfo_height() or 300
        draw_gantt_on_canvas(self.canvas, gantt, w, h)

        self.lbl_avg_turn.config(text=f"Avg Turnaround: {metrics.avg_turnaround_time:.2f}")
        self.lbl_avg_wait.config(text=f"Avg Waiting: {metrics.avg_waiting_time:.2f}")

        self._set_controls_state(running=False)
        self.btn_reset.configure(state="normal")

    def on_reset(self):
        """
        Limpa a visualização e restaura controles ao estado inicial.
        """

        self.canvas.delete("all")
        self.lbl_avg_turn.config(text="Avg Turnaround: –")
        self.lbl_avg_wait.config(text="Avg Waiting: –")
        self.btn_reset.configure(state="disabled")
        self._set_controls_state(running=False)

    def _set_controls_state(self, running: bool):
        """
        Habilita ou desabilita controles da UI conforme o estado de execução.

        Quando running=True, impede edição dos campos e seleção de scheduler.
        """

        state = "disabled" if running else "normal"
        self.btn_run.configure(state="disabled" if running else "normal")
        self.scheduler_combo.configure(state="disabled" if running else "readonly")
        self.entry_quantum.configure(state="disabled" if running else ("normal" if self.scheduler_var.get()=="Round Robin" else "disabled"))
        for child in (self.entry_name, self.entry_arrival, self.entry_burst, self.entry_priority):
            child.configure(state=state)

def main():
    """
    Ponto de entrada da aplicação GUI.

    Cria a instância App e inicia o loop principal do Tk.
    """

    app = App()
    app.mainloop()

if __name__ == "__main__":
    main()