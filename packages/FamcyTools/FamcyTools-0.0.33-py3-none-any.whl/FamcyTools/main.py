import sys
import argparse
import subprocess
import pkg_resources

def command_line_interface(args=None, arglist=None):
    """
    Main Famcy command line entry point
    args, arglist are used for unit testing
    """

    help_text = """
Example commands:
    init           : Initialize all necessary folders and path
    start          : starts the Famcy server
    upgrade        : upgrade famcy version
"""
    cmd_help = """A variety of commands are available, each with different arguments:
    init           : Initialize all necessary folders and path
    start          : starts the Famcy server
    upgrade        : upgrade famcy version
"""

    parser = argparse.ArgumentParser(
        description=help_text, formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("command", help=cmd_help)
    parser.add_argument("args", nargs="*", help="arguments for the given command")

    parser.add_argument(
        "--dev", help="flag for development environment", action="store_false"
    )

    if not args:
        args = parser.parse_args(arglist)

    if args.command == "init":
        from FamcyTools.scripts import env_init
        env_init.main(args.args)

    elif args.command == "run":
        from FamcyTools.scripts import start
        start.main(args.args)

    elif args.command == "upgrade":
        from FamcyTools.scripts import famcy_upgrade
        famcy_upgrade.main(args.args)

    elif args.command == "deploy":
        from FamcyTools.scripts import deploy
        deploy.main(args.args)

    else:
        print("Unknown command %s" % args.command)
        sys.exit(-1)