# R1DF's Showcase Manager
This project uses Python and the Tkinter library to help the user explore various ideas in maths and physics with the use
of "showcases".

## How it works
1. Every time the user runs `main.py`, the script checks for valid modules inside the `showcases` directory it is located together
with.
2. All these valid modules are saved to a list, out of which the user is able to select a module they want.
3. When a showcase is selected, a `Toplevel` window is made that demonstrates the showcase.
4. When the user closes that window, they can select any other showcase as well.

## Downloading showcases
Downloading showcases is simple. Just download the `.py` file that contains the Showcase object and stick it in the `showcases`
folder that is right next to the `main.py` script. The new showcases will be detected automatically on the next launch.

## Creating your own showcase
To create your own showcase, you must have a good enough understanding of the Python language and the Tkinter library.<br>
First, Create a Python file which will serve as the only module that has the showcase. After that, follow these starter steps:
* Before you make the Showcase class, add the following variables at the top of the script, below the imports section:
  * `MODULE_NAME`: How the module will appear when `main.py` launches and detects it.
  * `MODULE_AUTHOR`: How you wish to be referred to as creator of the module.
  * `MODULE_DESCRIPTION`: A little description about what the showcase is about. Please use linebreaks to split sentences!
* Create a `Showcase` object that inherits from `ShowcaseTemplate`.
* Ensure, in the first lines in the class, that the `super()` function is being called with `master` and `master_showcase` being used as an argument from `__init__`[^3].
* Write what you want to happen! Remember: A `Showcase` is just a Tkinter canvas.

When you're done, upload your showcase wherever you want. You can test it out by running `main.py` with your file inside the `showcases` folder.

[^1]: Showcase objects inherit from Canvas objects in the Tkinter library. Think of them as extended Canvas objects.
[^2]: Window objects inherit from Tk objects in the Tkinter library. Think of them like a normal window with a GUI.
[^3]: To see an example of this, check out the 5 default showcases in the `showcases` package in the repository's code. The first lines
in the class will all see a call to the parent class' constructor.
