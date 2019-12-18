"""make sequence for testbed
 the sequnce based on the dipole-dipole configuration to obtain:
 * small dipoles for resolving near-array variability (skip 2)
 * large dipoles for resolving cross-array variability (skip 15, 31, 47)"""
__author__ = "LucaP"
__year__ = "2019"

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time

def add_skip(skip, npot_max, electrodes, rec):
    seq = []
    for a in electrodes:
        b = a + 1 + skip
        for m in range(b + 1, electrodes[-1]):
            n = m + 1 + skip
            npot += 1
            if npot == npot_max:
                break
            seq.append([a, b, m, n])
            if rec:
                seq.append([m, n, a, b])
    seq = pd.DataFrame(np.array(seq), columns=['a', 'b', 'm', 'n'])
    return(seq)

def add_Wenner(skip, electrodes, rec):
    seq = []
    for a in range(1, electrodes[-1] - 3*skip - 2):
        m = a + skip + 1
        n = m + skip + 1
        b = n + skip + 1
        seq.append([a, b, m, n])
        if rec:
            seq.append([m, n, a, b])
    seq = pd.DataFrame(np.array(seq), columns=['a', 'b', 'm', 'n'])
    return(seq)

def add_grad(skip, electrodes, rec):
    seq = []
    for a in range(1, electrodes[-1] - 3*skip - 2):
        b = a + ((skip + 1) * 3)
        for m in range(a + 1, b - 2*skip):
            n = m + skip +1
            seq.append([a, b, m, n])
            if rec:
                seq.append([m, n, a, b])
    seq = pd.DataFrame(np.array(seq), columns=['a', 'b', 'm', 'n'])
    return(seq)

def plot(seq):
    for i, r in seq.iterrows():
        plt.plot(r['a'], 0, 'or')
        plt.plot(r['m'], 0, 'ob')
        plt.plot(r['n'], 0, 'ob')
        plt.plot(r['b'], 0, 'or')
        plt.xlim((0, 31.5))
        plt.show(block=False)
        plt.pause(0.5)
        plt.close()

def fun_rec(a: np.ndarray, b: np.ndarray, m: np.ndarray, n: np.ndarray):
    l = int(len(a))
    rec_num = np.zeros_like(a)
    rec_fnd = np.zeros_like(a)
    for i in range(l):
        if rec_num[i] != 0:
            continue
        for j in range(i + 1, l):
            if (a[i] == m[j] and b[i] == n[j] and m[i] == a[j] and n[i] == b[j]):
                rec_num[i] = j + 1
                rec_num[j] = i + 1
                rec_fnd[i] = 1  # mark the meas with reciprocals, else leave 0
                rec_fnd[j] = 2  # distinguish between directs and reciprocals
                break
    return(rec_num, rec_fnd)

if __name__ == "__main__":

    num_elec = 64
    num_quad = 20000
    opt = True

    electrodes = np.linspace(1, num_elec , num_elec, endpoint=True, dtype = np.int8)
    seq_list = []

    grads = [1, 2, 3, 4, 5, 6, 8, 11, 14, 17, 20]

    seq = []

    for g in grads:

        seq = add_grad(g, electrodes, rec=True)
        print('grad', g, 'len', len(seq))
        seq_list.append(seq)

    seq = pd.concat(seq_list, ignore_index=True)

    if opt:
        seq = seq.sort_values(by=['a', 'b'])

    groups = seq.groupby(['a', 'b'])
    inj = 0
    for n, g in groups:
        inj += len(g) // 8  + 1
    print('inj', inj)
    print('number of groups: ', groups.ngroups)
    print('mean group length: ', groups.size().reset_index(name='counts')['counts'].mean())
    print('mode group length: ',groups.size().reset_index(name='counts')['counts'].mode())

    # write labrecque schedule
    seq_clean = seq.to_numpy()
    np.savetxt('sequence.txt', seq_clean, fmt = '%i %i %i %i')
    len_seq_clean = seq.shape[0]
    id_meas = np.linspace(1, len_seq_clean, len_seq_clean, endpoint = True, dtype = np.int16)
    ones = np.ones_like(id_meas)
    seq_schd = np.column_stack((id_meas, ones, seq_clean[:,0], ones, seq_clean[:, 1], ones, seq_clean[:, 2], ones, seq_clean[:, 3]))
    np.savetxt('sequence_schd.txt', seq_schd, fmt = '%i %i %i %i %i %i %i %i %i')

    # get only direct for modeling
    rec_num, rec_fnd = fun_rec(seq_clean[:, 0], seq_clean[:, 1], seq_clean[:, 2], seq_clean[:, 3])
    seq_dir = seq_clean[rec_fnd == 1, :]
    print(len(seq_clean))
    print(len(seq_dir))
    np.savetxt('sequence_direct.txt', seq_dir, fmt = '%i %i %i %i')
