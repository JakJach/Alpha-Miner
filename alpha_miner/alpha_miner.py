def alpha_miner(x):

    # first, search for all events in process, find starts and stops
    starts = []
    stops = []
    all_events = []

    for row in x:
        if row[0] not in starts:
            starts.append(row[0])
        if row[-1] not in stops:
            stops.append(row[-1])
        for event in row:
            if event not in all_events:
                all_events.append(event)

    starts = list(dict.fromkeys(starts))
    stops = list(dict.fromkeys(stops))

    sorted(starts)
    sorted(stops)
    sorted(all_events)

    # define dictionaries and list for found possible connections
    direct_succession = {}
    causality = {}
    parallel = []
    inv_causality = {}

    post_temp = []
    pre_temp = []
    causality_temp = []
    parallel_temp = []

    for event in all_events:
        for log in x:
            for index, stage in enumerate(log):
                if stage == event and index < (len(log) - 1):
                    if log[index + 1] not in post_temp:
                        post_temp.append(log[index + 1])
                if stage == event and index > 0:
                    if log[index - 1] not in pre_temp:
                        pre_temp.append(log[index - 1])
        sorted(post_temp)
        sorted(pre_temp)

        if post_temp:
            direct_succession[event] = post_temp

        for element in post_temp:
            if element not in pre_temp:
                causality_temp.append(element)
            else:
                parallel_temp.append(element)

        if causality_temp:
            causality[event] = causality_temp

        # add a pair of parallel events
        if parallel_temp:
            parallel.append(sorted([event, parallel_temp[0]]))

        # clear temp matrices
        pre_temp = []
        post_temp = []
        causality_temp = []
        parallel_temp = []

    for stage, followed_stage in causality.items():
        if len(followed_stage) == 1:
            index = causality.get(stage)[0]
            if index not in inv_causality:
                inv_causality[index] = [stage]
            else:
                temp = inv_causality.get(index)
                temp.append(stage)
                inv_causality[index] = temp

    return all_events, starts, stops, direct_succession, causality, parallel, inv_causality
