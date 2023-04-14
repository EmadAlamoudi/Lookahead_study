import pyabc
import matplotlib.pyplot as plt
import os
import tempfile
import numpy as np
import scipy as sp
import pandas as pd
import time
import logging
import slad
from slad import CRProblem

# read cmd line arguments
host, port = slad.read_args()

problem = CRProblem()
base_model = problem.get_model()
prior = problem.get_prior()
model_id = problem.get_id()
measurement_data = problem.get_obs()

pop_size = 400
iters = 5
batch_size = 1
n_pop = 8
mean = 0.5
sigma = 0.1

normal_sigma = lambda mean, sigma: np.sqrt(np.log(sigma**2/mean**2+1))
normal_mean = lambda mean, sigma: np.log(mean) - normal_sigma(mean, sigma)**2 / 2


def model(pars):
    # numerical integration
    y = base_model(pars)

    # sleep a little to emulate heterogeneous run times
    sleep_s = np.random.lognormal(mean=normal_mean(mean, sigma), sigma=normal_sigma(mean, sigma))
    sleep_s = min(sleep_s, 60.)
    time.sleep(sleep_s)

    return y


def distance(y, y_0):
    return np.abs(y["y"] - y_0["y"]).sum()


# storage folder
db_dir = "data_la"
os.makedirs(db_dir, exist_ok=True)

for i_sampler, (sampler, sampler_id) in enumerate(zip([
    pyabc.sampler.RedisStaticSampler(host=host, port=port),
    pyabc.sampler.RedisEvalParallelSampler(
        host=host, port=port,
        look_ahead=False,
        wait_for_all_samples=True,
        batch_size=batch_size,
    ),
    pyabc.sampler.RedisEvalParallelSampler(
        host=host, port=port,
        look_ahead=False,
        wait_for_all_samples=False,
        batch_size=batch_size,
    ),
    pyabc.sampler.RedisEvalParallelSampler(
        host=host, port=port,
        look_ahead=True,
        look_ahead_delay_evaluation=True,
        wait_for_all_samples=True,
        batch_size=batch_size,
        max_n_eval_look_ahead_factor=1,
    ),
    pyabc.sampler.RedisEvalParallelSampler(
        host=host, port=port,
        look_ahead=True,
        look_ahead_delay_evaluation=True,
        wait_for_all_samples=False,
        batch_size=batch_size,
        max_n_eval_look_ahead_factor=1,
    )],
    ["STAT", "DYN_Wait", "DYN", "LA_Wait", "LA"]
)):
    if i_sampler not in [0, 1, 2, 4]:
        continue
    for i in range(0, iters):
        db_file = os.path.join(
            db_dir, f"db__{model_id}__{sigma}__{sampler_id}__{pop_size}__{i}.db")
        if os.path.exists(db_file):
            print(f"db_file {db_file} exists, continuing")
            continue

        if isinstance(sampler, pyabc.sampler.RedisEvalParallelSampler):
            sampler.log_file = os.path.join(
                db_dir,
                f"log_sampler__{model_id}__{sigma}__{sampler_id}__{pop_size}__{i}.db")

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
