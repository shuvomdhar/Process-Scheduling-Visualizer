def priority_non_preemptive(processes):
    """
    processes must include 'pr' key.
    Lower priority number means higher priority.
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
        highest = min(ready, key=lambda x: x['pr'])
        procs.remove(highest)
        start = time
        time += highest['bt']
        end = time
        chart.append((highest['id'], start, end))
        wt[highest['id']] = start - highest['at']
        tat[highest['id']] = end - highest['at']

    return chart, wt, tat
