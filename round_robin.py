from collections import deque

def round_robin(processes, quantum):
    """
    processes: list of dicts with 'id','at','bt'
    quantum: int
    Returns chart (multiple segments per process possible), wt dict, tat dict
    """
    procs = sorted([p.copy() for p in processes], key=lambda x: x['at'])
    time = 0
    queue = deque()
    idx = 0
    chart = []
    remaining = {p['id']: p['bt'] for p in procs}
    first_response = {p['id']: None for p in procs}
    completed = set()
    arrival_times = {p['id']: p['at'] for p in procs}
    total_bt = {p['id']: p['bt'] for p in procs}

    while len(completed) < len(procs):
        # enqueue arrivals
        while idx < len(procs) and procs[idx]['at'] <= time:
            queue.append(procs[idx])
            idx += 1

        if not queue:
            # jump to next arrival if any
            if idx < len(procs):
                time = procs[idx]['at']
                continue
            else:
                break

        cur = queue.popleft()
        pid = cur['id']
        if first_response[pid] is None:
            first_response[pid] = time

        exec_time = min(quantum, remaining[pid])
        start = time
        time += exec_time
        remaining[pid] -= exec_time
        end = time
        chart.append((pid, start, end))

        # enqueue any newly arrived during execution
        while idx < len(procs) and procs[idx]['at'] <= time:
            queue.append(procs[idx])
            idx += 1

        if remaining[pid] > 0:
            # requeue
            queue.append({'id': pid, 'at': time, 'bt': remaining[pid]})
        else:
            completed.add(pid)

    wt = {}
    tat = {}
    for p in procs:
        pid = p['id']
        tat[pid] = sum((e - arrival_times[pid]) for (pid2, s, e) in chart if pid2 == pid) if False else None
    # compute TAT and WT properly: TAT = completion_time - arrival; WT = TAT - original_bt
    completion = {}
    for pid, s, e in chart:
        completion[pid] = e  # last overwrite gives completion time

    for p in procs:
        pid = p['id']
        comp = completion.get(pid, p['at'])
        tat[pid] = comp - p['at']
        wt[pid] = tat[pid] - total_bt[pid]

    return chart, wt, tat
