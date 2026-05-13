from argparse import ArgumentParser, Namespace


def parse_arguments() -> Namespace:
    """
    Parses arguments given at execution using argparse

    Returns:
        Namespace: the parsed arguments
    """
    try:
        parser = ArgumentParser(exit_on_error=False)

        parser.add_argument("input_file",
                            help="input file relative path")
        parsed = parser.parse_args()
    except Exception:
        raise Exception("[ERROR]: no input file found ; please enter your "
                        "input file's path after 'make run'")
    return parsed
