import argparse


def parse_arguments():
    parser = argparse.ArgumentParser(description='Average the start and end tokens and print as latex table row')
    parser.add_argument('results', type=str,
                        help='The results of calculate_metrics.py')
    args = parser.parse_args()
    return args


def reformat_list_to_table(results_string):
    results = list(map(float, results_string.split(',')))
    percentile_10 = (results[0] + results[-4]) / 2 / 100
    percentile_25 = (results[1] + results[-3]) / 2 / 100
    percentile_50 = (results[2] + results[-2]) / 2 / 100
    percentile_100 = (results[3] + results[-1]) / 2 / 100
    return [percentile_10, percentile_25, percentile_50, percentile_100]


def main(results):
    resp = reformat_list_to_table(results)
    print("{:.2f} & {:.2f} & {:.2f} & {:.2f} \\\\".format(resp[0], resp[1], resp[2], resp[3]))


if __name__ == '__main__':
    arguments = parse_arguments()
    main(arguments.results)
