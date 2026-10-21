import matplotlib.pyplot as plt

COLORS = {"degree": "#eb6834", "betweenness": "#1baf7a",
          "kcore": "#eda100", "random": "#2a78d6"}


def plot_robustness(results, title, path):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.5))

    for name, (removed, lcc, eff) in results.items():
        color = COLORS.get(name, "gray")
        ax1.plot(removed, lcc, color=color, linewidth=2, label=name)
        ax2.plot(removed, [e / eff[0] for e in eff], color=color, linewidth=2, label=name)

    ax1.set_title("Largest connected component")
    ax2.set_title("Global efficiency (relative to start)")
    for ax in (ax1, ax2):
        ax.set_xlabel("Fraction of nodes removed")
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1.02)
        ax.grid(alpha=0.3)
    ax1.legend()

    fig.suptitle(title)
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)