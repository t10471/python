import path
path.dummy()
import t10471.migration.manage as manage
import argparse


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--user')
    p.add_argument('--password')
    p.add_argument('--host')
    p.add_argument('--db')
    args,argv = p.parse_known_args()
    manage.run(argv, args.user, args.password, args.host, args.db)

if __name__ == '__main__':
    main()
