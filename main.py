# Imports
from showcase_window import Window
import os
import readchar
import sys
import importlib
import platform


# Functions
def find_showcase_modules():
    files = [x for x in os.listdir(os.path.join(os.getcwd(), "showcases")) if x.endswith(".py")]
    for non_showcase_file in ["__init__.py", "showcase_template.py"]:
        if non_showcase_file in files:
            files.remove(non_showcase_file)
    return files


# Program launch
if __name__ == "__main__":
    if False:
        """
        SET BOOLEAN ABOVE TO TRUE IF YOU WISH TO OVERRIDE DEFAULT LAUNCH PROCESS! (PROGRAMMERS ONLY)
        EDIT THE CODE IN THIS SECTION (AND IMPORT WHAT YOU NEED) AT YOUR OWN WILL.
        TO START, YOU CAN CREATE A WINDOW OBJECT WITH NONE, ADD CONTENT TO IT, AND CALL ITS MAINLOOP FUNCTION
        """
        pass

    else:
        showcase_modules = find_showcase_modules()
        if showcase_modules:
            # Importing each module dynamically while also filtering them out by seeing if they contain needed metadata
            imported_modules = list(filter(
                lambda inspected_module: all([x in dir(inspected_module) for x in ["MODULE_NAME", "MODULE_AUTHOR"]]),
                [importlib.import_module(f"showcases.{x.split('.')[0]}") for x in showcase_modules]
            ))

            while True:
                os.system("cls" if platform.system() == "Windows" else "clear")
                print("The following showcases have been detected on your system:")
                for index, module in enumerate(imported_modules):
                    print(f"{index + 1}. {module.MODULE_NAME} (Author: {module.MODULE_AUTHOR})")
                print("\nPlease enter your selection with a number corresponding to the showcase you wish to load, "
                      "or leave input empty to quit: ")
                module_number = input().strip()

                if not module_number:
                    sys.exit()

                if module_number.isnumeric():
                    module_number = int(module_number)
                    if module_number < 1 or module_number > len(imported_modules):
                        print("Please ensure the number fits within the range of available modules.")
                    else:
                        print("Running showcase...")
                        window = Window(imported_modules[module_number - 1])
                        window.mainloop()
                        print("Showcase has been closed.")
                else:
                    print("Invalid response.")
        else:
            print("You don't appear to have any installed showcases.\n"
                  "If you haven't installed any, please ensure they are in the "
                  "\"showcases\" folder inside the folder the program you're running is in.\n\n"
                  "Otherwise, install some showcase modules online from the web. The creator's showcases are "
                  "available with the following link:\nhttps://github.com/R1DF/Physics-Showcases\n")
            print("Press any key to exit.")
            readchar.readkey()
            sys.exit()
