from app.main import create_app
import os
import sys
import getopt
import unittest
import dotenv


def run(flask_app_env):
    app = create_app(flask_app_env)
    # app.app_context().push()
    app.run()


def test():
    """Runs the unit tests."""
    tests = unittest.TestLoader().discover('app/test', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


def main(argv):
    # TODO: Write help doc => print help instead of printing error
    try:
        opts, _ = getopt.getopt(argv[1:], 's', ['setting='])
    except getopt.GetoptError:
        print(getopt.GetoptError)
        sys.exit(2)

    if argv[0] == "run":
        for opt, arg in opts:
            if opt in ['--s', '--setting']:
                run(arg) if arg in ('dev', 'test', 'prod') else print(
                    "Wrong --env, please choose from this list: ('dev', 'test', 'prod')")
            else:
                print("--s or --setting")

    elif argv[0] == "test":
        test()
    else:
        print("Please specify the option you want to exc: [run, test]")


if __name__ == '__main__':
    main(sys.argv[1:])
