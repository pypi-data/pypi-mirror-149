import warnings
import os.path
from idoc.configuration import IDOCConfiguration, LOGGING_FILE, MACHINE_NAME, MACHINE_ID

def main():
    # create the default config file
    IDOCConfiguration(warn_if_exists=True)
    
    if not os.path.exists(MACHINE_NAME):
        DEFAULT_NAME="IDOC_001"
        with open(MACHINE_NAME, "w") as filehandle:
            filehandle.write(f"{DEFAULT_NAME}\n")
            warnings.warn(
                f"Naming machine {DEFAULT_NAME}."\
                "If you wish to change the name,"\
                "please update the contents of {MACHINE_NAME}")

    if not os.path.exists(MACHINE_ID):
        warnings.warn(
            f"File {MACHINE_ID} does not exist."\
            " Please create it and" \
            " enter a string of 32 alphanumeric (0-9 and a-f)"\
            " characters and a newline characters"
        )