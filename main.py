from headhunter import print_hh_table
from superjob import print_sj_table
from environs import Env
from argparse import ArgumentParser

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument(
        "-s",
        "--single",
        help="fetch only a single page instead of all",
        action="store_true"
    )
    parser.add_argument(
        "-t",
        "--timer",
        action="store_true",
        help="add start and end time of script running after the results"
    )

    args = parser.parse_args()

    env = Env()
    env.read_env()

    sj_key = env.str("SJ_KEY")

    print_hh_table(args)
    print_sj_table(sj_key, args)
