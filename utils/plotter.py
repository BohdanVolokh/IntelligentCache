import matplotlib.pyplot as plt


# def plot_cache_hits(results: dict, interval: int = 100):
#     """
#     Побудова графіка залежності кеш-хітів від кількості запитів.
#
#     :param results: словник з назвою стратегії як ключем
#                     і списком значень кеш-хітів як значенням
#     :param interval: крок між вимірюваннями (за замовчуванням 100)
#     """
#     plt.figure(figsize=(10, 10))
#
#     for label, values in results.items():
#         steps = [interval * i for i in range(1, len(values) + 1)]
#         linestyle = '-' if "Intellectual" in label else '--'
#         plt.plot(steps, values, label=label, linestyle=linestyle, linewidth=2)
#
#     plt.title("Кеш-хіт залежно від кількості запитів")
#     plt.xlabel("Кількість запитів")
#     plt.ylabel("Кеш-хіт (частка)")
#     plt.legend()
#     plt.grid(True, linestyle='--', alpha=0.6)
#     plt.tight_layout()
#     plt.show()
#     plt.close()  # звільняє памʼять після показу графіка

def plot_cache_hits_per_session(int_list, lru_list, lfu_list):
    """
    Побудова графіка кеш-хітів по сесіях для кожної стратегії.

    :param int_list: список кеш-хітів для інтелектуального методу
    :param lru_list: список кеш-хітів для LRU
    :param lfu_list: список кеш-хітів для LFU
    """
    plt.figure(figsize=(10, 6))
    plt.plot(int_list, label="Intellectual", linestyle='-', linewidth=2)
    plt.plot(lru_list, label="LRU", linestyle='--', linewidth=2)
    plt.plot(lfu_list, label="LFU", linestyle='--', linewidth=2)

    plt.title("Кеш-хіти за кожну сесію запуску MVP")
    plt.xlabel("Номер запуску (сесія)")
    plt.ylabel("Кеш-хіти (кількість)")
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.show()
    plt.close()