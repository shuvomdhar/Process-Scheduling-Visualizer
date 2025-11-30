import matplotlib
matplotlib.use('TkAgg')  # for popup windows
import matplotlib.pyplot as plt
import os

def plot_and_show(name, chart, wt, tat, save_path=None):
    """
    chart: list of (pid, start, end)
    wt, tat: dicts keyed by pid
    saves to save_path if provided (pdf). Otherwise just shows.
    """
    # Determine timeline
    if not chart:
        raise ValueError("Empty chart - nothing to plot")

    pids = sorted(list({pid for pid, s, e in chart}), key=lambda x: int(x.strip('P')) if x.strip('P').isdigit() else x)
    # Build figure: top Gantt, bottom table+averages
    fig = plt.figure(figsize=(10, 6))
    gs = fig.add_gridspec(3, 1, height_ratios=[2, 1, 0.4], hspace=0.4)

    # Gantt (top 2 rows)
    ax = fig.add_subplot(gs[0:2, 0])
    for pid, s, e in chart:
        ax.barh(pid, e - s, left=s, align='center', edgecolor='black')
        # place label centered
        ax.text((s + e) / 2, pid, pid, ha='center', va='center', color='white', fontsize=9, fontweight='bold')

    ax.set_xlabel("Time")
    ax.invert_yaxis()
    ax.grid(axis='x', linestyle='--', alpha=0.4)
    ax.set_title(f"{name} - Gantt Chart")

    # adjust y positions because using categorical y labels might overlap for many segments
    # Matplotlib supports categorical barh if we pass y as string labels — done above.
    # Table (middle)
    ax_table = fig.add_subplot(gs[2, 0])
    ax_table.axis('off')

    # Build table rows
    table_data = [["Process", "Arrival", "Burst", "Waiting", "Turnaround"]]
    # we need arrival and burst; reconstruct from chart/WT/TAT: best to derive arrival & burst from wt/tat+chart
    # We'll attempt to get arrival and burst from wt,tat: burst = tat - wt
    for pid in pids:
        w = wt.get(pid, 0)
        t = tat.get(pid, 0)
        b = t - w
        # arrival: compute earliest start minus waiting
        # alternative: try to find earliest segment start and compute arrival=start - wait
        starts = [s for pid2, s, e in chart if pid2 == pid]
        arrival = min(starts) - w if starts else 0
        table_data.append([pid, str(int(arrival)), str(int(b)), str(int(w)), str(int(t))])

    # create matplotlib table
    table = ax_table.table(cellText=table_data, loc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 1.2)

    # Average calculations
    avg_wt = sum(wt.values()) / len(wt) if wt else 0
    avg_tat = sum(tat.values()) / len(tat) if tat else 0

    # Show averages below the table
    fig.suptitle(f"{name} - Avg WT: {avg_wt:.2f}, Avg TAT: {avg_tat:.2f}", fontsize=10, y=0.95)

    if save_path:
        # ensure extension .pdf
        if not save_path.lower().endswith(".pdf"):
            save_path += ".pdf"
        fig.savefig(save_path, bbox_inches='tight')
        print(f"Saved PDF to: {os.path.abspath(save_path)}")

    plt.show()
    plt.close(fig)
