"""make sequence for testbed
 the sequnce based on the dipole-dipole configuration to obtain:
 * small dipoles for resolving near-array variability (skip 2)
 * large dipoles for resolving cross-array variability (skip 15, 31, 47)"""
__author__ = "LucaP"
__year__ = "2019"

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn

def add_dd(skip, pot_ms, electrodes, rec):
    a_lastn = skip + max(pot_ms) + skip + 1  # a s s b m1 m2 m3 s s n3 
    seq = []
    for a in electrodes:
        b = a + skip + 1
        for pot_m in pot_ms:
            m = b + pot_m
            n = m + skip + 1
            if n > electrodes[-1]:
                continue
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

def add_grad(skip_ab, skip_mn, skip_mm, electrodes, rec):
    seq = []
    for a in range(1, electrodes[-1] - skip_ab - 1):
        b = a + skip_ab + 1
        for m in range(a + 1, b - skip_mn - 1, skip_mm):
            n = m + skip_mn + 1
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

def add_dds(seq_list):
    dd = {2: [1, 2, 3, 4, 5, 6, 7, 8], 4: [6, 8, 10, 12, 14, 16, 18, 20], 6: [16, 20, 24, 28, 32, 36, 40, 44]}
    for k, v in dd.items():
        seq = add_dd(k, v, electrodes, rec=True)
        seq_list.append(seq)
    return(seq_list)

def add_grads(seq_list):
    grads = {11:[2, 1], 21: [4, 1], 53: [6, 3]}
    for k, v in grads.items():
        seq = add_grad(k, v[0], v[1], electrodes, rec=True)
        seq_list.append(seq)
    return(seq_list)

if __name__ == "__main__":

    num_elec = 64
    num_quad = 20000
    opt = True

    electrodes = np.linspace(1, num_elec , num_elec, endpoint=True, dtype = np.int8)
    seq_list = []

    #seq_list = add_dds(seq_list)
    seq_list = add_grads(seq_list)

    seq = pd.concat(seq_list, ignore_index=True)

    if opt:
        seq = seq.sort_values(by=['a', 'b'])

    groups = seq.groupby(['a', 'b'])
    inj = 0
    for n, g in groups:
        print(g)
        print(len(g))
        inj += ((len(g) - 1) // 8) + 1
    print('inj', inj)
    print('number of groups: ', groups.ngroups)
    print('mean group length: ', groups.size().reset_index(name='counts')['counts'].mean())
    print('mode group length: ',groups.size().reset_index(name='counts')['counts'].mode())
    seaborn.distplot(groups.size().reset_index(name='counts')['counts'], bins=range(1, 20))
    plt.show()
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
    print('len sequence', len(seq_clean))
    print('len direct sequence', len(seq_dir))
    np.savetxt('sequence_direct.txt', seq_dir, fmt = '%i %i %i %i')
