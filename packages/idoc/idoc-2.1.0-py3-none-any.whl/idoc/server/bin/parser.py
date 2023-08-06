import argparse
from idoc.server.core.control_thread import ControlThread

def list_options(category):
    """
    Return a list of str with the names of the classes that can be passed
    for a given category.
    """
    return [cls.__name__ for cls in ControlThread._option_dict[category]['possible_classes']]

def get_parser():
    # Arguments to follow the command, adding video, etc options
    parser = argparse.ArgumentParser(
        prog="IDOC - The Individual Drosophila Optogenetic Conditioner",
        description=(
            """
            A modular package to monitor and store the position of flies in separate chambers
            while running a preset paradigm of hardware events controlled by an Arduino board.
            A GUI is available by running the client.py script in the same computer.
            """
        ),
        epilog="Developed at the Liu Lab @ VIB-KU Leuven Center for Brain and Disease Research.",
        fromfile_prefix_chars='@', allow_abbrev=False
    )

    # General settings
    parser.add_argument("-D", "--debug", action='store_true', dest="debug")


    # Boolean flags
    ## Controller module
    parser.add_argument(
        "--control", action='store_true', dest='control',
        help="Turn on controller module"
    )
    parser.add_argument(
        "--no-control", action='store_false', dest='control',
        help="Turn off controller module"
    )

    ## Recognizer module
    parser.add_argument(
        "--recognize", action='store_true', dest='recognize',
        help="Turn on recognizer module"
    )

    parser.add_argument(
        "--no-recognize", action='store_false', dest='recognize',
        help="Turn off recognizer module"
    )
    parser.add_argument(
        "--wrap", action='store_true', dest="wrap",
        help="If pasased a video, play it in a loop. Useful for debugging"
    )
    parser.add_argument(
        "--no-wrap", action='store_false', dest="wrap",
        help="If pasased a video, DO NOT play it in a loop. Useful for analysis"
    )

    parser.add_argument(
        "--use-wall-clock", action='store_true', dest='use_wall_clock',
        help="""
        Default. If passed, the time is computed using the output of time.time()
        """
    )
    parser.add_argument(
        "--no-use-wall-clock", action='store_false', dest='use_wall_clock',
        help="""
        If passed, the time is computed using the CAP_PROP_POS_MSEC property
        of the OpenCV capture class. This is only compatible with the
        OpenCV camera and when analyzing a video offline.
        """
    )

    # # Module settings
    parser.add_argument(
        "-m", "--mapping-path", type=str, dest="mapping_path",
        help="Absolute path to csv providing pin number-pin name mapping"
    )
    parser.add_argument(
        "--paradigm-path", type=str, dest="paradigm_path",
        help="Absolute path to csv providing the Arduino top level paradigm"
    )

    parser.add_argument(
        "--arduino_port", type=str,
        help="Absolute path to the Arduino port. Usually '/dev/ttyACM0' in Linux and COM in Windows"
    )

    parser.add_argument(
        "-f", "--framerate", type=int,
        help="Frames per second in the opened stream, overrides config."
    )
    parser.add_argument(
        "-v", "--video-path", type=str, dest='video_path',
        help=
        """
        If offline tracking is desired, location of the input video file.
        Only possible if OpenCVCamera class is passed in --camera.
        """
    )


    parser.add_argument(
        "-a", "--adaptation-time", type=int, dest="adaptation_time",
        help=
        """
        Number of seconds to wait before starting paradigm and saving tracking data
        from the moment this script is started. If not provided, it is taken from config.
        """
    )

    parser.add_argument(
        "-d", "--duration", type=int, dest="max_duration",
        help=
        """
        Maximum number of seconds the software will run. If not provided, it is taken from config.
        """
    )

    parser.add_argument(
        "--run", action='store_true', dest='run',
        help="Batch run"
    )
    parser.add_argument(
        "--no-run", action='store_false', dest='run',
        help="Batch run"
    )

    parser.add_argument(
        "--start-datetime", type=str, dest='start_datetime',
        help=""
    )

    # User input for classes
    parser.add_argument("--board", type=str, choices=list_options("board"))
    parser.add_argument("--camera", type=str, help="Stream source", choices=list_options("camera"))
    parser.add_argument("--drawer", type=str, choices=list_options("drawer"))
    parser.add_argument("--roi-builder", type=str, dest="roi_builder", choices=list_options("roi_builder"))
    parser.add_argument("--result-writer", type=str, dest="result_writer", choices=list_options("result_writer"))
    parser.add_argument("--tracker", type=str, choices=list_options("tracker"))


    # General application module
    parser.add_argument("-e", "--experimenter", type=str, help="Add name of the experimenter/operator")

    # Bottle settings
    parser.add_argument("-p", "--port", type=int)


    parser.set_defaults(
        control=False, recognize=False,
        wrap=None,
        default=True,
        max_duration=None
    )

    return parser
