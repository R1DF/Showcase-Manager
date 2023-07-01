# R1DF's Physics Showcase
This project uses Python and the Tkinter library to help the user explore various ideas in maths and physics with the use
of "showcases".

Despite the project's name, this project is not strictly linked to physics. The Physics Showcase can be used to explore
any sort of subject, but it is best for those with mathematics and calculations involved in order to help the user visualise
different concepts. Mathematics, physics, chemistry are good examples.

## How it works
1. Every time the user runs `main.py`, the script checks for valid modules inside the `showcases` directory it is located together
with.
2. All these valid modules are saved to a list, out of which the user is able to select a module they want.
3. A `Showcase`[^1] object is imported from that module, and it is added to the `Window`[^2] object that is now created.
4. The user can now engage with the showcase. They can close the window and switch to other showcases in the terminal as they please, or exit.
Programmers who wish to modify the launch process of the project are free to do so in `main.py`.

## Download
Please view the Releases section of the repository for official releases.<br>
THe Physics Showcase is only available for download for Windows users. If you use macOS/Linux, the repository must be downloaded
and `main.py` must be run with Python 3 installed. The project was coded in Python 3.11.

## Downloading showcases
Downloading showcases is simple. Just download the `.py` file that contains the Showcase object and stick it in the `showcases`
folder that is right next to the `main.py` script. The new showcases will be detected automatically on the next launch.

## Creating your own showcase
To create your own showcase, you must have a good enough understanding of the Python language and the Tkinter library.<br>
First, Create a Python file which will serve as the only module that has the showcase. After that, follow these starter steps:
* Before you make the Showcase class, add the following variables at the top of the script, below the imports section:
  * `MODULE_NAME`: How the module will appear when `main.py` launches and detects it.
  * `MODULE_AUTHOR`: How you wish to be referred to as creator of the module.
* Create a `Showcase` object that inherits from `ShowcaseTemplate`.
* Ensure, in the first lines in the class, that the `super()` function is being called with `master` being used as an argument from `__init__``[^3].
* Write what you want to happen! Remember: A `Showcase` is just a Tkinter canvas.

When you're done, upload your showcase wherever you want. You can test it out by running `main.py` with your file inside the `showcases` folder.

[^1]: Showcase objects inherit from Canvas objects in the Tkinter library. Think of them as extended Canvas objects.
[^2]: Window objects inherit from Tk objects in the Tkinter library. Think of them as like a normal window with a GUI.
[^3]: To see an example of this, check out the 5 default showcases in the `showcases` package in the repository's code. The first lines
in the class will all see a call to the parent class' constructor.
