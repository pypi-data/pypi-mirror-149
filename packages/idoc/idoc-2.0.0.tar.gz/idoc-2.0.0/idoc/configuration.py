import os
import logging
import warnings
import yaml

CONFIG_FILE = os.path.join(os.environ["HOME"], ".config", "idoc", "idoc.yaml")
if not os.path.exists(os.path.dirname(CONFIG_FILE)):
    os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)

class IDOCConfiguration(object):
    """
    Handles the idoc configuration parameters
    Data are stored in and retrieved from a configuration file
    """

    _settings = {

        'default_class': {
            'board': "ArduinoDummy",
            'camera': "OpenCVCamera",
            'drawer': "DefaultDrawer",
            'result_writer': "CSVResultWriter",
            'roi_builder': "IDOCROIBuilder",
            'tracker': "AdaptiveBGModel"
        },

        'core' : {
            'debug': True
        },

        'network': {

            'port': 9000
        },

        'folders' : {
                        'results' : {'path' : '/idoc_data/results', 'description' : 'Where data will be saved by the saver class.'},
                        'paradigms': {'path': '/idoc_data/paradigms', 'description' : 'Where csv files containing hardware programs are stored.'}
        },

        # 'users' : {
        #               'admin' : { # pylint: disable=bad-continuation
        #                   'id' : 1, 'name' : 'admin', 'fullname' : '', 'PIN' : 9999, 'email' : '',
        #                   'telephone' : '', 'group': '', 'active' : False, 'isAdmin' : True,
        #                   'created' : datetime.datetime.now().timestamp()
        #               }
        # },

        'roi_builder': {
            'args': [],
            'kwargs': {}
        },

        'io': {
            'result_writer': {
                'args': [],
                'kwargs': {
                    'max_n_rows_to_insert': 1,
                }
            },

            'camera': {
                'args': [],
                'kwargs': {
                    'drop_each': 1,
                    'use_wall_clock': True,
                    'rotation': 0, #degs
                    'video_path': None
                }
            }
        },

        'controller': {
            'mapping_path': '/idoc_data/mega.csv',
            'paradigm_path': 'warm_up.csv',
            'arduino_port': "/dev/ttyACM0",
            'pwm': {
            },
        },

        'drawer': {
            'args': [],
            'kwargs': {
                'draw_frames': False,
                'video_out_fourcc': "DIVX",
                'framerate': None # match that of the camera
            },
            'last_drawn_path': "/tmp/last_img.png",
            'last_annot_path': "/tmp/last_img_annot.png",
        },

        'experiment': {
            'adaptation_time': 5,
            "max_duration": 18000,
            "location": None
        },
        "logging": "/home/vibflysleep/.config/idoc/logging.yaml"
    }


    def __init__(self, config_file=CONFIG_FILE):
        self._config_file = config_file
        self.load()

    @property
    def content(self):
        return self._settings

    @property
    def file_exists(self):

        return os.path.exists(self._config_file)

    def save(self):
        """
        Save settings to settings file
        """

        try:
            with open(self._config_file, 'w') as filehandle:
                yaml.dump(self._settings, filehandle)

            logging.info('Saved idoc configuration file to %s', self._config_file)

        except:
            raise ValueError('Problem writing to file % s' % self._config_file)

    def load(self):
        """
        Reads saved configuration folders settings from configuration file
        If file does not exist, creates default settings
        """

        if not self.file_exists:
            self.save()

        else:
            try:
                with open(self._config_file, 'r') as filehandle:
                    self._settings.update(yaml.load(filehandle, yaml.SafeLoader))
            except:
                raise ValueError("File %s is not a valid configuration file" % self._config_file)

        return self._settings


def integrity_check():

    try:
        with open(CONFIG_FILE, "r") as filehandle:
            config = yaml.load(filehandle, yaml.SafeLoader)
            print(f"Can load {CONFIG_FILE}")
    except Exception as error:
        warnings.warn(error)
        print(f"Cannot load {CONFIG_FILE}")
    


if __name__ == "__main__":
    config = IDOCConfiguration()
    config.save()
