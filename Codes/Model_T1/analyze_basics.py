import pyabc
import numpy as np
import os

sampler_ids = ["STAT", "DYN_Wait", "DYN", "LA_Wait", "LA"]
iters = 1
model_id = "cr_0.02"

walltimes = []
for sampler_id in sampler_ids:
    ws_for_sampler = []
    for ix in range(iters):
        db_file = f"data_la/{model_id}__{sampler_id}__{ix}.db"
        if not os.path.exists(db_file):
            continue
        h = pyabc.History("sqlite:///" + db_file, create=False)
        abc = h.get_abc()
        #if abc.end_time is None:
        #   continue
        ws_for_sampler.append((abc.end_time - abc.start_time).total_seconds())
    walltimes.append(ws_for_sampler)
    print(f"{sampler_id}\t {np.mean(ws_for_sampler):.2f} ({np.std(ws_for_sampler):.2f} ({ws_for_sampler}))")
