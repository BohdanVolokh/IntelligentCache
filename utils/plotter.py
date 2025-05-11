import matplotlib.pyplot as plt


def plot_cache_hits(results: dict, interval: int = 100):
    """
    Побудова графіка залежності кеш-хітів від кількості запитів.

    :param results: словник з назвою стратегії як ключем
                    і списком значень кеш-хітів як значенням
    :param interval: крок між вимірюваннями (за замовчуванням 100)
    """
    plt.figure(figsize=(10, 10))

    for label, values in results.items():
        steps = [interval * i for i in range(1, len(values) + 1)]
        linestyle = '-' if "Intellectual" in label else '--'
        plt.plot(steps, values, label=label, linestyle=linestyle, linewidth=2)

    plt.title("Кеш-хіт залежно від кількості запитів")
    plt.xlabel("Кількість запитів")
    plt.ylabel("Кеш-хіт (частка)")
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.show()