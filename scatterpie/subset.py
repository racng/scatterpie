from itertools import chain

def get_subsets(data, normalize=False):
    """    
    get a dict of subsets in data
    
    @type data: list[Iterable]    
    @rtype: dict[str, list]
    input
      data: data to get groups for
    return
      set_collections: a dict of different subsets
    example:
    In: get_subsets([range(10), range(5,15), range(3,8)])
    Out: 
    {'001': set(),
    '010': {10, 11, 12, 13, 14},
    '011': set(),
    '100': {0, 1, 2},
    '101': {3, 4},
    '110': {8, 9},
    '111': {5, 6, 7}}
    """

    N = len(data)

    sets_data = [set(data[i]) for i in range(N)]  # sets for separate groups
    s_all = set(chain(*data))                             # union of all sets

    # bin(3) --> '0b11', so bin(3).split('0b')[-1] will remove "0b"
    set_collections = {}
    for n in range(1, 2**N):
        key = bin(n).split('0b')[-1].zfill(N)
        value = s_all
        sets_for_intersection = [sets_data[i] for i in range(N) if  key[i] == '1']
        sets_for_difference = [sets_data[i] for i in range(N) if  key[i] == '0']
        for s in sets_for_intersection:
            value = value & s
        for s in sets_for_difference:
            value = value - s
        set_collections[key] = value

    return set_collections

def get_subset_sizes(set_collections, normalize=False):
    if normalize:
        data_size = len(set(chain(*set_collections.values())))
        return {k: len(set_collections[k])/data_size for k in set_collections}
    return {k: len(set_collections[k]) for k in set_collections}

def get_subset_labels(set_collections, groups=None, normalize=False):
    set_sizes = get_subset_sizes(set_collections, normalize=normalize)
    labels = {k: "" for k in set_sizes}
    
    if groups is not None:
        ngroups = len(next(iter(set_sizes))) # number of digits in first key
        nlabels = len(groups)
        if nlabels!= ngroups:
            raise ValueError("{} labels provided for {} groups.".format(nlabels, ngroups))
        for i in range(ngroups):
            logic = ['0'] * ngroups
            logic[i] = '1'
            labels[''.join(logic)] = groups[i] + '\n'
    
    for k in set_sizes:
        labels[k] += str(set_sizes[k])
    return labels
