def wer(ref, hyp, debug=False):
    r = ref.split()
    h = hyp.split()
    # costs will holds the costs, like in the Levenshtein distance algorithm
    costs = [[0 for _ in range(len(h) + 1)] for _ in range(len(r) + 1)]
    # backtrace will hold the operations we've done.
    # so we could later backtrace, like the WER algorithm requires us to.
    backtrace = [[0 for _ in range(len(h) + 1)] for _ in range(len(r) + 1)]
 
    op_ok = 0
    op_sub = 1
    op_ins = 2
    op_del = 3

    del_penalty = 1
    ins_penalty = 1
    sub_penalty = 1

    # First column represents the case where we achieve zero
    # hypothesis words by deleting all reference words.
    for i in range(1, len(r)+1):
        costs[i][0] = del_penalty*i
        backtrace[i][0] = op_del

    # First row represents the case where we achieve the hypothesis
    # by inserting all hypothesis words into a zero-length reference.
    for j in range(1, len(h) + 1):
        costs[0][j] = ins_penalty * j
        backtrace[0][j] = op_ins

    # computation
    for i in range(1, len(r)+1):
        for j in range(1, len(h)+1):
            if r[i-1] == h[j-1]:
                costs[i][j] = costs[i-1][j-1]
                backtrace[i][j] = op_ok
            else:
                substitution_cost = costs[i-1][j-1] + sub_penalty  # penalty is always 1
                insertion_cost = costs[i][j-1] + ins_penalty   # penalty is always 1
                deletion_cost = costs[i-1][j] + del_penalty   # penalty is always 1
                 
                costs[i][j] = min(substitution_cost, insertion_cost, deletion_cost)
                if costs[i][j] == substitution_cost:
                    backtrace[i][j] = op_sub
                elif costs[i][j] == insertion_cost:
                    backtrace[i][j] = op_ins
                else:
                    backtrace[i][j] = op_del
                 
    # back trace though the best route:
    i = len(r)
    j = len(h)
    num_sub = 0
    num_del = 0
    num_ins = 0
    num_cor = 0

    lines = []
    if debug:
        lines.append(["OP", "REF", "HYP"])
    while i > 0 or j > 0:
        if backtrace[i][j] == op_ok:
            num_cor += 1
            i -= 1
            j -= 1
            if debug:
                lines.append(["OK", r[i], h[j]])
        elif backtrace[i][j] == op_sub:
            num_sub += 1
            i -= 1
            j -= 1
            if debug:
                lines.append(["SUB", r[i], h[j]])
        elif backtrace[i][j] == op_ins:
            num_ins += 1
            j -= 1
            if debug:
                lines.append(["INS", "***", h[j]])
        elif backtrace[i][j] == op_del:
            num_del += 1
            i -= 1
            if debug:
                lines.append(["DEL", r[i], "***"])
    if debug:
        lines = [lines[0]] + lines[:0:-1]
    wer_result = round((num_sub + num_del + num_ins) / float(len(r)), 3)
    return {'WER': wer_result, 'Cor': num_cor, 'Sub': num_sub, 'Ins': num_ins, 'Del': num_del}, lines
