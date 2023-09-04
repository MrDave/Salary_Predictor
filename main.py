from environs import Env
from argparse import ArgumentParser
import datetime
from handlers import print_job_table
from headhunter import get_hh_stats
from superjob import get_sj_stats


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
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--hh",
        action="store_true",
        help="get stats only from HeadHunter"
    )
    group.add_argument(
        "--sj",
        action="store_true",
        help="get stats only from SuperJob"
    )

    args = parser.parse_args()

    env = Env()
    env.read_env()

    sj_key = env.str("SJ_KEY")
    if args.timer:
        start_time = datetime.datetime.now()

    if not args.sj:
        hh_stats = get_hh_stats(args.single)
        hh_table_title = "HeadHunter Moscow"
        print_job_table(hh_stats, hh_table_title)

    if not args.hh:
        sj_stats = get_sj_stats(sj_key, args.single)
        sj_table_title = "SuperJob Moscow"
        print_job_table(sj_stats, sj_table_title)

    if args.timer:
        end_time = datetime.datetime.now()
        run_time = (end_time - start_time).seconds
        print(f"Start time: {start_time}\nEnd time: {end_time}\nTotal time: {run_time} second(s)")
