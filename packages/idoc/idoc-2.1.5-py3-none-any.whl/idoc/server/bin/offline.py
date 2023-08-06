import logging
from threading import Thread

from idoc.server.core.control_thread import ControlThread
from idoc.helpers import get_server
from idoc.configuration import IDOCConfiguration
from idoc.server.core.control_thread import ControlThread
from .parser import get_parser, list_options
from .server import run, stop

logger = logging.getLogger(__name__)

config = IDOCConfiguration()
ARGS = vars(get_parser().parse_args())
from idoc import __version__ as VERSION
from idoc.helpers import get_machine_id

machine_id = get_machine_id()
RESULT_DIR = config.content["folders"]["results"]["path"]
PORT = config.content["network"]["port"]
DEBUG = config.content["network"]["port"]


control = ControlThread(
    machine_id=machine_id,
    version=VERSION,
    result_dir=RESULT_DIR,
    user_data=ARGS,
)


def offline():

    ARGS["control"] = False
    ARGS["recognize"] = True

    control = ControlThread(
        machine_id=machine_id,
        version=VERSION,
        result_dir=RESULT_DIR,
        user_data=ARGS,
    )

    server_thread = Thread(target=run, name="bottle", args=(PORT,))

    control.start()
    server_thread.start()
    control.join()
    stop()