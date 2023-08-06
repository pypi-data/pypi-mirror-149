import numpy as np

def assign_annotators(records, annotators: list=['a', 'b', 'c']):
    """
    Assign two annotators to each record.
    Ensures that each record has two distinct annotators.
    """
    n_record = len(records)
    n_annotator = len(annotators)

    N_JUMP = int(np.ceil(n_record / n_annotator))
    print(f'{n_record} records')
    print(f'{n_annotator} annotators')
    print(f'{N_JUMP}')

    ann0 = np.empty(n_record, dtype=str)
    ann1 = np.empty(n_record, dtype=str)
    for i, u in enumerate(annotators):
        # assign annotator 'u' to each record
        lower = N_JUMP*i
        upper = N_JUMP*(i+1)
        if upper > n_record:
            upper = n_record
        ann0[lower:upper] = u

        annotator_unassigned = [x for x in annotators if x != u]

        # assign the remaining annotators to these records
        N_JUMP_UNASSIGNED = int(np.ceil((upper - lower) / len(annotator_unassigned)))
        for j, u2 in enumerate(annotator_unassigned):
            lower_unassigned = lower + N_JUMP_UNASSIGNED*j
            upper_unassigned = lower + N_JUMP_UNASSIGNED*(j+1)
            ann1[lower_unassigned:upper_unassigned] = u2
    
    return ann0.tolist(), ann1.tolist()

# test it works
if __name__ == '__main__':
    seed = np.random.RandomState(3782)
    records = [r for r in range(700)]
    ann0, ann1 = assign_annotators(records)