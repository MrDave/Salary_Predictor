from headhunter import get_hh_stats
from superjob import get_sj_stats
from environs import Env
from argparse import ArgumentParser

LANGUAGES = [
        "JavaScript",
        "Java",
        "Python",
        "Ruby",
        "PHP",
        "C++",
        "C#",
        "C",
        "Go",
        "Shell"
    ]


if __name__ == '__main__':
    parser = ArgumentParser(
        description="Get job offers from HeadHunter and SuperJob websites and compare their average salaries"
    )
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

    get_hh_stats(args)
    get_sj_stats(sj_key, args)
