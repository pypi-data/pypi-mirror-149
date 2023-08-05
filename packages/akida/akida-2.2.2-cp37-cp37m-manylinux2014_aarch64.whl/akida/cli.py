import argparse

from .core import devices, __version__
from .deploy import generate_files, deploy_engine


def list_devices():
    devices_list = devices()
    if len(devices_list) == 0:
        print("No devices detected")
    else:
        print("Available devices:")
        for device in devices_list:
            print(device.desc)


def main():
    parser = argparse.ArgumentParser()
    sp = parser.add_subparsers(dest="action")
    sp.add_parser("devices", help="List available devices")
    sp.add_parser("version", help="Return akida version")
    engine_parser = sp.add_parser("engine", help="Deploy engine sources and applications")
    # Create parent subparser for arguments shared between engine methods
    engine_parent = argparse.ArgumentParser(add_help=False)
    engine_parent.add_argument(
        "--dest-path",
        type=str,
        default=None,
        required=True,
        help="The destination path.")
    engine_action_parser = engine_parser.add_subparsers(
        dest="engine_action",
        help="Action: deploy or generate.")
    engine_action_parser.add_parser(
        "deploy",
        help="Deploy the engine library.",
        parents=[engine_parent])
    gen_parser = engine_action_parser.add_parser(
        "generate",
        help="Generate application(s) from fixture file(s).",
        parents=[engine_parent])
    gen_parser.add_argument("--fixture-files",
                            help="A list of python fixture files",
                            nargs="+",
                            type=str,
                            required=True)
    gen_parser.add_argument("--modules-paths",
                            help="Path to additional modules required for fixtures",
                            nargs="+",
                            type=str,
                            default=None)
    args = parser.parse_args()
    if args.action == "devices":
        list_devices()
    elif args.action == "version":
        print(__version__)
    elif args.action == "engine":
        if args.engine_action == "deploy":
            deploy_engine(args.dest_path)
        elif args.engine_action == "generate":
            generate_files(args.fixture_files, args.dest_path, args.modules_paths)
