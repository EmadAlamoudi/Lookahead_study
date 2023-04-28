import pyabc
from pyabc import (IntegratedModel, ModelResult,
                   QuantileEpsilon)
import fitmulticell.model as morpheus_model
from scipy import stats
import numpy as np
import pandas as pd
import os
import tempfile
import matplotlib.pyplot as plt
import math
from collections import OrderedDict
import fitmulticell.sumstat.base as bs
from pyabc.sampler import RedisEvalParallelSampler
import argparse
from fitmulticell.sumstat import SummaryStatistics
import fcntl, os, time



root_path = os.getcwd()


parser = argparse.ArgumentParser(description='Parse necessary arguments')
parser.add_argument('-pt', '--port', type=str, default="50004",
                    help='Which port should be use?')
parser.add_argument('-ip', '--ip', type=str,
                    help='Dynamically passed - BW: Login Node 3')
args = parser.parse_args()

file_ = root_path + "/YAP_Signaling_Liver_Regeneration_Model_reparametrized_further.xml"

par_map = {'k1': './CellTypes/CellType/Constant[@symbol="k1"]',
           'k2': './CellTypes/CellType/Constant[@symbol="k2"]',
           'k3_0': './CellTypes/CellType/Constant[@symbol="k3_0"]',
           'k4': './CellTypes/CellType/Constant[@symbol="k4"]',
           'k5': './CellTypes/CellType/Constant[@symbol="k5"]',
           'k6': './CellTypes/CellType/Constant[@symbol="k6"]',
           'k7': './CellTypes/CellType/Constant[@symbol="k7"]',
           'k8': './CellTypes/CellType/Constant[@symbol="k8"]',
           'k9': './CellTypes/CellType/Constant[@symbol="k9"]',
           'k10': './CellTypes/CellType/Constant[@symbol="k10"]',
           'k11': './CellTypes/CellType/Constant[@symbol="k11"]',
           'K_M1': './CellTypes/CellType/Constant[@symbol="K_M1"]',
           'K_M2': './CellTypes/CellType/Constant[@symbol="K_M2"]',
           'intensity_normalization_total': './CellTypes/CellType/Constant[@symbol="intensity_normalization_total"]',
           }



def additive_noise(sumstat: dict = {}):
    noisy_sumstat = {}
    sumstat_edit = prepare_data_3(sumstat)
    # calculated form data
    sigma = {'YAP_nuclear_observable': 0.061763933333333,
             'YAP_total_observable': 0.050105066666667}
    for key, val in sumstat_edit.items():
        if key == 'loc': continue
        if key == 'YAP_nuclear_observable':
            noisy_sumstat[key] = val + sigma[key] * np.random.randn(len(val))
        else:
            noisy_sumstat[key] = val + sigma[key] * np.random.randn(len(val))

    return noisy_sumstat


sumstat = SummaryStatistics(sum_stat_calculator=additive_noise, ignore=["cell.id", "Tension", "time"])

maximum_sim_time = [900, 1800]
model = morpheus_model.MorpheusModel(
    file_, par_map=par_map,par_scale="linear",
    show_stdout=False, show_stderr=False,
    timeout=maximum_sim_time[0],
    raise_on_error=False,executable="/home/ealamoodi/morpheus-binary/morpheus-2.2.0-beta2",
    sumstat = sumstat)



obs_pars = {'k1': 100,
            'k2': 2.02,
            'k3_0': 1.7,
            'k4': 0.11,
            'k5': 100,
            'k6': 0.18,
            'k7': 100,
            'k8': 100,
            'k9': 0.17,
            'k10': 1.1,
            'k11': 30,
            'K_M1': 0.0008,
            'K_M2': 0.25,
            'intensity_normalization_total': 1}

# generate data
# observed_data = model.sample(obs_pars)
model.par_scale = "log10"
obs_pars_log = {key: math.log10(val) for key, val in obs_pars.items()}

observe_data_path = root_path + "/YAP_Signaling_Liver_Regeneration_Data_edited_7.csv"
data = pd.read_csv(observe_data_path, sep=',')
dict_data = {}
for col in data.columns:
    dict_data[col] = data[col].to_numpy()

import csv

data2 = csv.DictReader(open(observe_data_path))
#observed_data = load_obj("obs_data_4_132t")


limits = {key: (math.log10((10**-1)*val), math.log10((10**1)*val)) for key, val in obs_pars.items()}

#set_2
limits["k1"] = (1, 3)
limits["k5"] = (1, 4)
limits["k7"] = (1, 4)
limits["k8"] = (1, 4)
limits["k2"] = (0,2)
limits["K_M1"] = (-4,-2)




prior = pyabc.Distribution(**{key: pyabc.RV("uniform", lb, ub - lb)
                              for key, (lb, ub) in limits.items()})




def eucl_dist(sim, obs):
    if sim == -15:
        print("timeout")
        return np.inf    
    
    total = 0
    for key in sim:
        if key in ('loc', "time", "cell.id", "Tension"):
            continue
        x = np.array(sim[key])
        y = np.array(obs["IdSumstat__" + key])
        z = np.array(obs["SEM_IdSumstat__" + key])
        # simulation does not finish successfuly, only partial part of the
        # result wrtten. In such case, ignore the parameter vector
        if x.size != y.size:
            # size does not match
            return np.inf
        # if np.max(y) != 0:
        #     x = x/np.max(y)
        #     y = y/np.max(y)
        total += np.sum(((x - y)/z) ** 2)
    return total


def prepare_data_3(sim):
    unique_obs = [0,8,15,20,30,50]
    step = 10
    itemindex = []
    new_dict = dict()
    uniqe_key_list = []
    for key in [*sim]:
        if key == 'loc':
            continue
        new_dict[key]=[]
        for index in unique_obs:
            new_dict[key].extend(sim[key][index*step:(index*step)+step])
    for key, val in new_dict.items():
        new_dict[key] = np.array(val)
    return new_dict


redis_sampler = RedisEvalParallelSampler(host=args.ip, port=args.port, adapt_look_ahead_proposal=False,look_ahead=False, log_file= root_path + "/log/Liver_regeneration_14para.csv")



# early rejection model

pop_size = [250, 500, 1000]

abc = pyabc.ABCSMC(model, prior, eucl_dist, population_size=pop_size[0],
                   eps=QuantileEpsilon(alpha=0.3),sampler=redis_sampler)



db_path = "sqlite:///" + root_path + "/db/" + "14param.db"
history = abc.new(db_path, dict_data)
abc.run(max_nr_populations=40)


pyabc.visualization.plot_epsilons(history)
df, w = history.get_distribution(t=history.max_t)
plt.savefig(root_path + '/outplot/Liver_regeneration_eps_14param.png')

pyabc.visualization.plot_kde_matrix(df, w, limits=limits, refval=obs_pars_log)
plt.savefig(root_path + '/outplot/Liver_regeneration_kde_mat_14param.png')








