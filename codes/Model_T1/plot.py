import pyabc
import matplotlib.pyplot as plt
import numpy as np

pyabc.settings.set_figure_params("pyabc")

sampler_ids = ["STAT", "DYN_Wait", "DYN", "LA"]
sampler_labels = ["STAT", "DYN_Old", "DYN", "LA"]
colors = ["C1", "C2", "C3", "C0"]

data_dir = "data_la"
model_id = "cr_0.02"

pop_size = 400
sigma = 0.5
iters = 5

times = []
for sampler_id in sampler_ids:
    times_for_sampler = []
    for ix in range(iters):
        h = pyabc.History(
            f"sqlite:///data_la/{model_id}__{sigma}__{sampler_id}__{pop_size}__{ix}.db", create=False)
        abc = h.get_abc()
        times_for_sampler.append(
            (abc.end_time - abc.start_time).total_seconds())
    times.append(times_for_sampler)


times = np.array(times)
times /= np.max(np.mean(times, axis=1))
print(np.mean(times, axis=1))
print(np.std(times, axis=1))
fig, axes = plt.subplots(ncols=2, figsize=(14, 4))

axes[0].bar(
    x=np.arange(len(sampler_ids)),
    height=np.mean(times, axis=1),
    yerr=np.std(times, axis=1),
    color=colors,
)

for sampler_ix, sampler_id in enumerate(sampler_ids):
    for ix in range(iters):
        h = pyabc.History(
            f"sqlite:///data_la/{model_id}__{sigma}__{sampler_id}__{pop_size}__{ix}.db", create=False)
        pyabc.visualization.plot_kde_1d_highlevel(
            h, x="p0", xname=r"$\theta_1$", xmin=-3.5, xmax=1,
            numx=200, color=colors[sampler_ix],
            ax=axes[1],
            label=sampler_id if ix == 0 else None,
        )

axes[1].legend()

for fmt in ["png", "pdf"]:
    plt.savefig(f"figures_la/fig.{fmt}")