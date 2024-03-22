import locale


def format_currency(amount):
    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

    return locale.currency(amount, grouping=True)
