# main_gui.py
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from fcfs import fcfs
from sjf import sjf
from priority import priority_non_preemptive
from round_robin import round_robin
from viz_utils import plot_and_show

ALGOS = ["FCFS", "SJF (Non-Preemptive)", "Priority (Non-Preemptive)", "Round Robin"]

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("CPU Scheduling Visualizer")
        self.process_entries = []
        self.create_widgets()

    def create_widgets(self):
        frm = ttk.Frame(self.root, padding=10)
        frm.grid(sticky="nsew")

        # Algorithm selection
        ttk.Label(frm, text="Select Algorithm:").grid(row=0, column=0, sticky="w")
        self.algo_var = tk.StringVar(value=ALGOS[0])
        algo_menu = ttk.OptionMenu(frm, self.algo_var, ALGOS[0], *ALGOS, command=self.on_algo_change)
        algo_menu.grid(row=0, column=1, sticky="w")

        # Time quantum label (for RR)
        self.q_label = ttk.Label(frm, text="Time Quantum:")
        self.q_entry = ttk.Entry(frm, width=8)
        # initially hidden
        self.q_label.grid(row=0, column=2, padx=(20,0))
        self.q_entry.grid(row=0, column=3)
        self.q_label.grid_remove()
        self.q_entry.grid_remove()

        # Number of processes
        ttk.Label(frm, text="Number of Processes:").grid(row=1, column=0, sticky="w", pady=(8,0))
        self.n_entry = ttk.Entry(frm, width=6)
        self.n_entry.grid(row=1, column=1, sticky="w", pady=(8,0))

        btn_create = ttk.Button(frm, text="Create Rows", command=self.create_rows)
        btn_create.grid(row=1, column=2, sticky="w", padx=(10,0), pady=(8,0))

        # Frame for processes
        self.proc_frame = ttk.Frame(frm, borderwidth=1, relief="solid", padding=6)
        self.proc_frame.grid(row=2, column=0, columnspan=4, pady=(10,0), sticky="nsew")

        # Buttons
        btn_run = ttk.Button(frm, text="Run Visualization", command=self.run_visualization)
        btn_run.grid(row=3, column=0, pady=(10,0))
        btn_export = ttk.Button(frm, text="Export PDF", command=self.export_pdf)
        btn_export.grid(row=3, column=1, pady=(10,0))

        # status
        self.status = ttk.Label(frm, text="", foreground="green")
        self.status.grid(row=4, column=0, columnspan=4, sticky="w", pady=(8,0))

    def on_algo_change(self, _=None):
        algo = self.algo_var.get()
        if "Round Robin" in algo:
            self.q_label.grid()
            self.q_entry.grid()
        else:
            self.q_label.grid_remove()
            self.q_entry.grid_remove()
        # If rows exist, update visibility of priority column
        self.refresh_priority_visibility()

    def create_rows(self):
        for widget in self.proc_frame.winfo_children():
            widget.destroy()
        self.process_entries = []
        try:
            n = int(self.n_entry.get())
            if n <= 0:
                raise ValueError
        except Exception:
            messagebox.showerror("Input Error", "Enter a valid positive integer for number of processes.")
            return

        headers = ["Process", "Arrival Time", "Burst Time", "Priority"]
        for col, h in enumerate(headers):
            ttk.Label(self.proc_frame, text=h, font=("Segoe UI", 9, "bold")).grid(row=0, column=col, padx=6, pady=4)

        for i in range(n):
            pid_lbl = ttk.Label(self.proc_frame, text=f"P{i+1}")
            pid_lbl.grid(row=i+1, column=0, padx=6, pady=4)

            at_e = ttk.Entry(self.proc_frame, width=8)
            at_e.grid(row=i+1, column=1, padx=6, pady=4)
            bt_e = ttk.Entry(self.proc_frame, width=8)
            bt_e.grid(row=i+1, column=2, padx=6, pady=4)
            pr_e = ttk.Entry(self.proc_frame, width=8)
            pr_e.grid(row=i+1, column=3, padx=6, pady=4)

            self.process_entries.append((f"P{i+1}", at_e, bt_e, pr_e))

        self.refresh_priority_visibility()
        self.status.config(text=f"Created {n} rows. Fill values and click Run.")

    def refresh_priority_visibility(self):
        algo = self.algo_var.get()
        show_priority = "Priority" in algo
        for _, at_e, bt_e, pr_e in self.process_entries:
            if show_priority:
                pr_e.grid()
            else:
                pr_e.delete(0, tk.END)
                pr_e.grid_remove()

    def read_processes(self, require_priority=False):
        procs = []
        for pid, at_e, bt_e, pr_e in self.process_entries:
            try:
                at = int(at_e.get())
                bt = int(bt_e.get())
                if at < 0 or bt <= 0:
                    raise ValueError
            except Exception:
                raise ValueError(f"Invalid arrival or burst for {pid}. Arrival must be >=0 and burst >0.")
            proc = {'id': pid, 'at': at, 'bt': bt}
            if require_priority:
                try:
                    pr = int(pr_e.get())
                except Exception:
                    raise ValueError(f"Invalid priority for {pid}. Enter integer.")
                proc['pr'] = pr
            procs.append(proc)
        return procs

    def run_visualization(self):
        algo = self.algo_var.get()
        try:
            if not self.process_entries:
                raise ValueError("Create process rows first.")

            if "FCFS" in algo:
                procs = self.read_processes(False)
                chart, wt, tat = fcfs(procs)
                plot_and_show("FCFS", chart, wt, tat)

            elif "SJF" in algo:
                procs = self.read_processes(False)
                chart, wt, tat = sjf(procs)
                plot_and_show("SJF (Non-Preemptive)", chart, wt, tat)

            elif "Priority" in algo:
                procs = self.read_processes(require_priority=True)
                chart, wt, tat = priority_non_preemptive(procs)
                plot_and_show("Priority (Non-Preemptive)", chart, wt, tat)

            elif "Round Robin" in algo:
                procs = self.read_processes(False)
                try:
                    q = int(self.q_entry.get())
                    if q <= 0:
                        raise ValueError
                except Exception:
                    raise ValueError("Enter a valid positive integer for Time Quantum.")
                chart, wt, tat = round_robin(procs, q)
                plot_and_show(f"Round Robin (Q={q})", chart, wt, tat)
            else:
                raise ValueError("Unknown algorithm selection.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return

    def export_pdf(self):
        algo = self.algo_var.get()
        try:
            if not self.process_entries:
                raise ValueError("Create process rows first.")
            if "FCFS" in algo:
                procs = self.read_processes(False)
                chart, wt, tat = fcfs(procs)
                default_name = "fcfs_schedule.pdf"
            elif "SJF" in algo:
                procs = self.read_processes(False)
                chart, wt, tat = sjf(procs)
                default_name = "sjf_schedule.pdf"
            elif "Priority" in algo:
                procs = self.read_processes(require_priority=True)
                chart, wt, tat = priority_non_preemptive(procs)
                default_name = "priority_schedule.pdf"
            elif "Round Robin" in algo:
                procs = self.read_processes(False)
                try:
                    q = int(self.q_entry.get())
                    if q <= 0:
                        raise ValueError
                except Exception:
                    raise ValueError("Enter a valid positive integer for Time Quantum.")
                chart, wt, tat = round_robin(procs, q)
                default_name = f"rr_q{q}_schedule.pdf"
            else:
                raise ValueError("Unknown algorithm selection.")

            fpath = filedialog.asksaveasfilename(defaultextension=".pdf",
                                                 filetypes=[("PDF files", "*.pdf")],
                                                 initialfile=default_name,
                                                 title="Save schedule as PDF")
            if not fpath:
                return
            plot_and_show(algo, chart, wt, tat, save_path=fpath)
            messagebox.showinfo("Saved", f"PDF saved to:\n{fpath}")
        except Exception as e:
            messagebox.showerror("Error", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
