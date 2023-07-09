# Imports
from showcase_windows import ShowcaseManager
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

        a = Window()
        Showcase(a).pack(expand=1, fill="both")
        a.mainloop()

    else:
        # showcase_modules = find_showcase_modules()
        # if showcase_modules:
        #     # Importing each module dynamically while also filtering them out by seeing if they contain needed metadata
        #     imported_modules = list(filter(
        #         lambda inspected_module: all([x in dir(inspected_module) for x in ["MODULE_NAME", "MODULE_AUTHOR"]]),
        #         [importlib.import_module(f"showcases.{x.split('.')[0]}") for x in showcase_modules]
        #     ))

        manager = ShowcaseManager()
        manager.mainloop()


