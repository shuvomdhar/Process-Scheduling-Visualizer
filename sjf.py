def sjf(processes):
    """
    Non-preemptive SJF.
    """
    procs = [p.copy() for p in processes]
    time = 0
    chart = []
    wt = {}
    tat = {}

    while procs:
        ready = [p for p in procs if p['at'] <= time]
        if not ready:
            time += 1
            continue
        # shortest burst
        shortest = min(ready, key=lambda x: x['bt'])
        procs.remove(shortest)
        start = time
        time += shortest['bt']
        end = time
        chart.append((shortest['id'], start, end))
        wt[shortest['id']] = start - shortest['at']
        tat[shortest['id']] = end - shortest['at']

    return chart, wt, tat
