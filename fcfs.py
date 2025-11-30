def fcfs(processes):
    """
    processes: list of dicts: {'id': 'P1', 'at': int, 'bt': int, 'pr': optional}
    Returns: chart [(id,start,end)...], wt_dict, tat_dict
    """
    procs = sorted(processes, key=lambda p: p['at'])
    time = 0
    chart = []
    wt = {}
    tat = {}

    for p in procs:
        if time < p['at']:
            time = p['at']
        start = time
        time += p['bt']
        end = time
        chart.append((p['id'], start, end))
        wt[p['id']] = start - p['at']
        tat[p['id']] = end - p['at']

    return chart, wt, tat
