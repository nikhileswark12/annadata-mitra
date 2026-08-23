import h5py
import json

f = h5py.File('f:/Annadata Mitra/annadata-mitra/ai-services/scratch/model.weights.h5', 'r')
keys = list(f.keys())
dense_key = [k for k in keys if 'dense' in k][0]
g = f[dense_key]
print(f"Keys in {dense_key}: {list(g.keys())}")
if 'vars' in g:
    print(f"Vars in {dense_key}: {list(g['vars'].keys())}")
    print(f"Var 0 shape: {g['vars']['0'].shape}")

conv_keys = [k for k in keys if 'Conv1' in k]
if conv_keys:
    print(f"Conv1 key: {conv_keys[0]}")
    c = f[conv_keys[0]]
    if 'vars' in c:
        print(f"Vars in Conv1: {list(c['vars'].keys())}")
