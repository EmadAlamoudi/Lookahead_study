import pyabc
import matplotlib.pyplot as plt
import os
import tempfile
import numpy as np
import scipy as sp
import pandas as pd
import time
import logging

import argparse


parser = argparse.ArgumentParser(description='Parse necessary arguments')
parser.add_argument('-pt', '--port', type=str, default="50004",
                    help='Which port should be use?')
parser.add_argument('-ip', '--ip', type=str,
                    help='Dynamically passed - BW: Login Node 3')
args = parser.parse_args()

pop_size = 100
iters = 5
batch_size = 1
n_pop = 6
mean_short = 0.05
mean_long = 1
sigma_short = 0.025
sigma = 0.5

normal_sigma = lambda mean, sigma: np.sqrt(np.log(sigma**2/mean**2+1))
normal_mean = lambda mean, sigma: np.log(mean) - normal_sigma(mean, sigma)**2 / 2

prior = pyabc.Distribution(p=pyabc.RV("uniform", -2, 4))
model_id = "bimodal"
measurement_data = {"y": 1}

def model(pars):
    p = pars["p"]
    y = {"y": p**2 + 0.05 * np.random.normal()}

    # sleep a little to emulate heterogeneous run times
    if p > 0:
        sleep_s = np.random.lognormal(mean=normal_mean(mean_long, sigma), sigma=normal_sigma(mean_long, sigma))
        sleep_s = min(sleep_s, 60.)
        time.sleep(sleep_s)
    else:
        # sleep a little to emulate heterogeneous run times
        sleep_s = np.random.lognormal(mean=normal_mean(mean_short, sigma_short), sigma=normal_sigma(mean_short, sigma_short))
        sleep_s = min(sleep_s, 60.)
        time.sleep(sleep_s)

    return y

def distance(y, y_0):
    return np.abs(y["y"] - y_0["y"]).sum()


# storage folder
db_dir = "data_la"
os.makedirs(db_dir, exist_ok=True)

for i_sampler, (sampler, sampler_id) in enumerate(zip([
    pyabc.sampler.RedisStaticSampler(host=args.ip, port=args.port),
    pyabc.sampler.RedisEvalParallelSampler(
        host=args.ip, port=args.port,
        look_ahead=False,
        wait_for_all_samples=True,
        batch_size=batch_size,
    ),
    pyabc.sampler.RedisEvalParallelSampler(
        host=args.ip, port=args.port,
        look_ahead=False,
        wait_for_all_samples=False,
        batch_size=batch_size,
    ),
    pyabc.sampler.RedisEvalParallelSampler(
        host=args.ip, port=args.port,
        look_ahead=True,
        look_ahead_delay_evaluation=True,
        wait_for_all_samples=True,
        batch_size=batch_size,
        max_n_eval_look_ahead_factor=1,
    ),
    pyabc.sampler.RedisEvalParallelSampler(
        host=args.ip, port=args.port,
        look_ahead=True,
        look_ahead_delay_evaluation=True,
        wait_for_all_samples=False,
        batch_size=batch_size,
        max_n_eval_look_ahead_factor=1,
    ),
    pyabc.sampler.RedisEvalParallelSampler(
        host=args.ip, port=args.port,
        look_ahead=True,
        look_ahead_delay_evaluation=True,
        wait_for_all_samples=False,
        adapt_pre_proposal=True,
        batch_size=batch_size,
        max_n_eval_look_ahead_factor=1,
    )],
    ["STAT", "DYN_Wait", "DYN", "LA_Wait", "LA", "LA_fix"]
)):
    if i_sampler not in [0, 1, 2, 3, 4, 5]:
        continue
    for i in range(0, iters):
        db_file = os.path.join(db_dir, f"{model_id}__{sigma}__{sampler_id}__{pop_size}__{i}.db")
        if os.path.exists(db_file):
            print(f"db_file {db_file} exists, continuing")
            continue

        abc = pyabc.ABCSMC(
            models=model,
            parameter_priors=prior,
            distance_function=distance,
            population_size=pop_size,
            sampler=sampler,
            #eps=eps,
        )

        abc.new("sqlite:///" + db_file, measurement_data)
        abc.run(max_nr_populations=n_pop)

print("ABC out")
