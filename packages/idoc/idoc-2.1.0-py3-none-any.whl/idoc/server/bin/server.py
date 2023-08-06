import sys
import json
import urllib.parse
import logging
import logging.config
import os
from threading import Thread

import yaml
import bottle
import coloredlogs

from idoc.decorators import warning_decorator, error_decorator, wrong_id
from idoc.server.core.control_thread import ControlThread
from idoc.helpers import get_server
from idoc.configuration import IDOCConfiguration
from idoc.server.core.control_thread import ControlThread
from idoc import __version__ as VERSION
from idoc.helpers import get_machine_id
from idoc.server.bin.parser import get_parser, list_options

logger = logging.getLogger(__name__)

app = bottle.Bottle()
config = IDOCConfiguration()
ARGS = vars(get_parser().parse_args())

machine_id = get_machine_id()
RESULT_DIR = config.content["folders"]["results"]["path"]
PORT = config.content["network"]["port"]
DEBUG = config.content["network"]["port"]
LOGGING_CONFIG = config.content["logging"]

if os.path.exists(LOGGING_CONFIG):
    with open(LOGGING_CONFIG, "r") as filehandle:
        config = yaml.load(filehandle, yaml.SafeLoader)

logging.config.dictConfig(config)


control_thread = ControlThread(
    machine_id=machine_id,
    version=VERSION,
    result_dir=RESULT_DIR,
    user_data=ARGS,
)


logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename='IDOC.log',
                    filemode='w')

logger = logging.getLogger(__name__)
coloredlogs.install()


def stop(control):
    r"""
    A function to bind the arrival of specific signals to an action.
    """
    try:
        control_thread.stop()
        logger.info('Quitting')
        os._exit(0) # pylint: disable=protected-access
        # sys.exit(0)
    except Exception as error:
        logger.warning(error)

    return

def run(port):
    server = get_server(port)
    logger.info("Running bottle on server %s, port %d", server, port)
    bottle.run(app, host='0.0.0.0', port=port, debug=DEBUG, server=server)


@app.route('/static/<filepath:path>')
def server_static(filepath):
    return bottle.static_file(filepath, root="/")

@app.post("/settings/<id>")
@warning_decorator
@wrong_id
def update():
    r"""
    Receive the new settings passed by the user
    via a POST request in JSON format.
    A partial update is ok i.e. not all parameters
    need to be supplied, only those changing.
    A dictionary with the current values is returned
    upong GETting to this same URL.
    """

    post_data = bottle.request.body.read() # pylint: disable=no-member

    if isinstance(post_data, bytes):
        data_decoded = post_data.decode()
    else:
        data_decoded = post_data

    try:
        data_parsed = json.loads(data_decoded)
    except json.decoder.JSONDecodeError:
        data_parsed = urllib.parse.parse_qs(data_decoded)

    settings = data_parsed['settings']
    submodule = data_parsed['submodule']
    if submodule == "control_thread":
        control_thread.settings = settings
    else:
        target = control
        for module in submodule:
            target = getattr(target, module)

        if target is not None:
            target.settings = settings
        else:
            logger.warning("Module %s is not initialized yet.", module)

    return {"status": "success"}


@app.get("/settings/<id>")
@wrong_id
@warning_decorator
def report():
    r"""
    Return current value of the settings to the user
    Settings can be updated by POSTing to the same URL.
    """
    settings = control_thread.settings
    return settings


@app.get("/info/<id>")
@warning_decorator
@wrong_id
def inform():
    r"""
    Return information about the control thread to the user,
    contained in the info property.
    """
    return control_thread.info

@app.get('/id')
@error_decorator
def get_id():
    r"""
    Return the content of /etc/machine-id to the user.
    URLs are suffixed in the API to check the supplied id
    with the id of the machine.
    A mismatch is interpreted as a user mistake and a
    WrongMachineID expception is raised.
    """
    return {"id": control_thread.info["id"]}


@app.post('/load_paradigm/<id>')
@warning_decorator
@wrong_id
def load_paradigm():
    r"""
    Update the hardware paradigm loaded in IDOC.
    Do this by posting an object with key paradigm_path
    and value the filename of one of the csv files in the
    paradigms_dir.
    paradigms_dir is defined in the config file under
    folders > paradigms > path.
    A list of the paradigms can be retrieved by GETting to /list_paradigms/.
    """
    post_data = bottle.request.body.read() # pylint: disable=no-member
    if isinstance(post_data, bytes):
        data_decoded = post_data.decode()
    else:
        data_decoded = post_data

    try:
        data_parsed = json.loads(data_decoded)
    except json.decoder.JSONDecodeError:
        data_parsed = urllib.parse.parse_qs(data_decoded)

    paradigm_path = data_parsed["paradigm_path"][0]
    control_thread.load_paradigm(paradigm_path=paradigm_path)
    return {"status": "success"}


@app.post('/description/<id>')
@warning_decorator
@wrong_id
def description():
    r"""
    Set a description of the experiment
    """
    post_data = bottle.request.body.read() # pylint: disable=no-member
    if isinstance(post_data, bytes):
        data_decoded = post_data.decode()
    else:
        data_decoded = post_data

    data_parsed = json.loads(data_decoded)
    control_thread.description = data_parsed["description"]

    return {"status": "success"}


@app.get('/list_paradigms/<id>')
@warning_decorator
@wrong_id
def list_paradigms():
    r"""
    Get a list of the available paradigms that the user
    can select via POSTing to /load_paradigm.
    This is also available in info["controller"]["paradigms"].
    """
    return control_thread.list_paradigms()

@app.get('/mapping/<id>')
@warning_decorator
@wrong_id
def mapping():
    r"""
    Tell the user that is the hardware-board pin mapping loaded in IDOC
    This is also available in info["controller"]["mapping"].
    """
    return control_thread.mapping

@app.get('/pin_state/<id>')
@warning_decorator
@wrong_id
def pin_state():
    r"""
    Return the status of the board pins
    This is also available in info["controller"]["pin_state"]
    """
    return control_thread.pin_state


@app.get('/controls/<submodule>/<action>/<id>')
@warning_decorator
@wrong_id
def control(submodule, action):
    r"""
    Command the IDOC modules.
    Set a submodule as ready, start or stop it by supplying
    ready, start and stop as action
    Actions are available for the recognizer and controller modules
    as well as the control thread.
    """
    if submodule == "control_thread" and action == "stop":
        # exit the application completely
        stop()

    return control_thread.command(submodule, action)


@app.post("/controls/toggle/<id>")
@warning_decorator
@wrong_id
def toggle():

    post_data = bottle.request.body.read() # pylint: disable=no-member
    if isinstance(post_data, bytes):
        data_decoded = post_data.decode()
    else:
        data_decoded = post_data

    logger.debug(data_decoded)

    data_parsed = json.loads(data_decoded)
    hardware = data_parsed["hardware"]
    value = float(data_parsed["value"])
    return control_thread.toggle(hardware, value)



@app.get('/choices/<category>/<id>')
@warning_decorator
@wrong_id
def list_choices(category):
    return list_options(category)


def main():

    try:
        server_thread = Thread(target=run, name="bottle", args=(PORT,))
        control_thread.start()
        server_thread.start()
        control_thread.join()
        stop(control_thread)
    except KeyboardInterrupt:
        sys.exit(0)


if __name__ == "__main__":
    main()