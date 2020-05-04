from alpha_miner.alpha_miner import alpha_miner
from alpha_miner.process_graph import ProcessGraph


# file path to txt file with logs
file_path = r'C:\Studia\S8\MiAPB\alpha_miner_project_4\logs\log1.txt'

# reading txt file and appending logs table
logs = []
with open(file_path, 'r') as file:
    for line in file:
        logs.append(line.replace('\n', '').split(' '))

# checking the logs list in console
for row in logs:
    print(row)

# using miner
[all_events, starts, ends, direct_succession, causality, parallel_events, inv_causality] = alpha_miner(logs)


# merging parallel events
new_parallel_events = []
deleted_events = []

for par in parallel_events:

    # checking, if the miner has connected parallel events to pairs; if not, the entry is deleted
    if len(par) > 1:
        new_event = par[0] + '||' + par[1]
        dic = {par[0]: new_event}

        # use dictionary to replace first event for parallel one in all the lists and remove the second
        if par[0] not in deleted_events:
            all_events = [dic.get(n, n) for n in all_events]
            if par[1] in all_events:
                all_events.remove(par[1])
            start_set_events = [dic.get(n, n) for n in starts]
            if par[1] in start_set_events:
                starts.remove(par[1])
            ends = [dic.get(n, n) for n in ends]
            if par[1] in ends:
                ends.remove(par[1])

            # use dictionary to replace first event for parallel one in all the dictionaries
            # and remove the second
            if par[1] in direct_succession:
                del direct_succession[par[1]]
            if par[1] in causality:
                del causality[par[1]]
            if par[1] in inv_causality:
                del inv_causality[par[1]]

            for key in direct_succession:
                direct_succession[key] = [dic.get(n, n) for n in direct_succession[key]]
                if par[1] in direct_succession[key]:
                    direct_succession[key].remove(par[1])
            direct_succession = dict([(dic.get(n, n), v) for n, v in direct_succession.items()])

            for key in causality:
                causality[key] = [dic.get(n, n) for n in causality[key]]
                if par[1] in causality[key]:
                    causality[key].remove(par[1])
            causality = dict([(dic.get(n, n), v) for n, v in causality.items()])

            for key in inv_causality:
                inv_causality[key] = [dic.get(n, n) for n in inv_causality[key]]
                if par[1] in inv_causality[key]:
                    inv_causality[key].remove(par[1])
            inv_causality = dict([(dic.get(n, n), v) for n, v in inv_causality.items()])

            new_parallel_events.append(new_event)
            deleted_events.append(par[1])

            for par_par in parallel_events:
                if par[0] in par_par and par in parallel_events:
                    parallel_events.remove(par)
        else:
            continue
    else:
        if par in parallel_events:
            parallel_events.remove(par)

parallel_events = sorted(new_parallel_events)


# sorting all lists after merging
sorted(all_events)
sorted(starts)
sorted(ends)
sorted(direct_succession)
sorted(causality)
sorted(inv_causality)

# print out the result of mining in console
print(all_events, starts, ends, direct_succession, causality, parallel_events, inv_causality)

# create graph
G = ProcessGraph()

# DRAW A GRAPH
# adding split gateways based on causality
for event in causality:
    if len(causality[event]) > 1:
        if tuple(causality[event]) in parallel_events:
            G.add_and_split_gateway(event, causality[event])
        else:
            G.add_xor_split_gateway(event, causality[event])
    # elif len(causality[event]) == 1:
    #    G.edge(event, causality[event][0])

# adding merge gateways based on inverted causality
for event in inv_causality:
    if len(inv_causality[event]) > 1:
        if tuple(inv_causality[event]) in parallel_events:
            G.add_and_merge_gateway(inv_causality[event], event)
        else:
            G.add_xor_merge_gateway(inv_causality[event], event)
    elif len(inv_causality[event]) == 1:
        source = list(inv_causality[event])[0]
        G.edge(source, event)

# adding start event
G.add_event("start")
if len(starts) > 1:
    pairs = []
    for event in starts:
        pairs.append(["start", event])
    G.edges(pairs)
#    if tuple(start_set_events) in parallel_events:
#        G.add_and_split_gateway(event,start_set_events)
#    else:
#        G.add_xor_split_gateway(event,start_set_events)
else:
    G.edge("start", list(starts)[0])

# adding end event
G.add_event("end")
if len(ends) > 1:
    pairs = []
    for event in ends:
        pairs.append([event, "end"])
    G.edges(pairs)
    # if tuple(end_set_events) in parallel_events:
    #    G.add_and_merge_gateway(end_set_events,event)
    # else:
    #    G.add_xor_merge_gateway(end_set_events,event)
else:
    G.edge(list(ends)[0], "end")

G.render('business_process')
G.view('business_process')