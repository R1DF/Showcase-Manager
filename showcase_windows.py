# Imports
from tkinter import Tk, Toplevel, Frame, Listbox, Button, Label, messagebox, filedialog, Scrollbar
from time import localtime, strftime
import sys
import importlib
import importlib.util
import os
import conditions


# Showcase description toplevel class
class ShowcaseDescriptionWindow(Toplevel):
    def __init__(self, master, showcase_name, showcase_author, showcase_description):
        # Setup
        self.master = master
        super().__init__(self.master)
        self.title(f"Module description: \"{showcase_name}\"")
        self.resizable(False, False)

        # Adding widgets
        self.module_author_label = Label(self, text=f"The author of the module is:\n{showcase_author}")
        self.module_author_label.pack(pady=4)

        self.module_description_label = Label(self, text=f"Description:\n{showcase_description}")
        self.module_description_label.pack(pady=4)

        self.back_button = Button(self, text="Return", command=self.handle_close)
        self.back_button.pack()

        # Protocol
        self.protocol("WM_DELETE_WINDOW", self.handle_close)

    def handle_close(self):
        self.master.showcase_description_window = None
        self.master.unlock()
        super().destroy()

# Showcase toplevel class
class ShowcaseWindow(Toplevel):
    def __init__(self, master, showcase_module):
        # Setup
        self.master = master
        self.showcase_module = showcase_module
        super().__init__(self.master)
        self.title("Physics Showcase")
        self.WIDTH, self.HEIGHT = self.master.showcase_window_resolution
        self.geometry(f"{self.WIDTH}x{self.HEIGHT}")
        self.resizable(False, False)
        self.config(bg="GRAY")

        # Adding showcase
        self.showcase = showcase_module.Showcase(self)
        self.showcase.pack(expand=1, fill="both")

        # Protocol
        self.protocol("WM_DELETE_WINDOW", self.handle_close)

    def handle_close(self):
        self.master.showcase_window = None
        self.master.add_to_log(f"Closed showcase \"{self.showcase_module.MODULE_NAME}\".")
        self.master.unlock()
        super().destroy()


# Main showcase controller window
class ShowcaseManager(Tk):
    def __init__(self):
        # Window setup
        super().__init__()
        self.modules = []
        self.title("List of Showcases")
        self.showcase_window_resolution = [600, 400]
        self.showcase_window = None
        self.showcase_description_window = None
        self.geometry()
        self.resizable(False, False)

        # Creating widgets
        self.modules_label = Label(text="Showcases:")
        self.modules_label.pack()

        self.modules_outer_frame = Frame()
        self.modules_outer_frame.pack()

        # Setting up module view
        self.modules_left_frame = Frame(self.modules_outer_frame)
        self.modules_left_frame.grid(row=0, column=0)

        self.modules_listbox = Listbox(self.modules_left_frame, width=30)
        self.modules_listbox.pack(side="left")

        self.modules_scrollbar = Scrollbar(self.modules_left_frame, command=self.modules_listbox.yview)
        self.modules_scrollbar.pack(side="right", fill="y")
        self.modules_listbox.config(yscrollcommand=self.modules_scrollbar.set)

        # Control panel
        self.controls_right_frame = Frame(self.modules_outer_frame)
        self.controls_right_frame.grid(row=0, column=1)

        self.run_module_button = Button(self.controls_right_frame, text="View selected showcase", command=self.view_selected_showcase, width=17)
        self.run_module_button.pack()

        self.open_external_module_button = Button(self.controls_right_frame, text="Load external showcase", command=self.load_external_showcase, width=17)
        self.open_external_module_button.pack()

        self.scan_for_modules_button = Button(self.controls_right_frame, text="Scan for new showcases", command=self.update_showcases, width=17)
        self.scan_for_modules_button.pack()

        self.view_module_description_button = Button(self.controls_right_frame, text="View showcase description", command=self.view_showcase_description, width=17)
        self.view_module_description_button.pack()

        # Logs panel
        self.logs_frame = Frame()
        self.logs_frame.pack()

        self.logs_label = Label(self.logs_frame, text="Log:")
        self.logs_label.pack()

        self.logs_outer_frame = Frame(self.logs_frame)
        self.logs_outer_frame.pack()

        self.logs_inner_frame = Frame(self.logs_outer_frame)
        self.logs_inner_frame.pack()

        self.logs_listbox = Listbox(self.logs_inner_frame, width=45)
        self.logs_listbox.pack(side="left")

        self.logs_y_scrollbar = Scrollbar(self.logs_inner_frame, command=self.logs_listbox.yview)
        self.logs_y_scrollbar.pack(side="right", fill="y")

        self.logs_x_scrollbar = Scrollbar(self.logs_outer_frame, orient="horizontal", command=self.logs_listbox.xview)
        self.logs_x_scrollbar.pack(side="bottom", fill="both")

        self.logs_listbox.config(yscrollcommand=self.logs_y_scrollbar.set, xscrollcommand=self.logs_x_scrollbar.set)

        # Protocol
        self.protocol("WM_DELETE_WINDOW", self.confirm_exit)

        # Bindings
        self.modules_listbox.bind("<Double-Button>", lambda x: self.view_selected_showcase())

        # Loading showcases
        sys.path.append(os.path.join(os.getcwd(), "showcases"))  # Recognise showcase package and makes template importable
        self.modules = self.scan_showcases()


    def scan_showcases(self):
        # Finding all files
        all_modules = [x for x in os.listdir(os.path.join(os.getcwd(), "showcases")) if x.endswith(".py")]
        for non_showcase_file in ["__init__.py", "showcase_template.py"]:
            if non_showcase_file in all_modules:
                all_modules.remove(non_showcase_file)

        # Filtering given files
        showcases = list(filter(lambda inspected_module: all([x in dir(inspected_module) for x in ["MODULE_NAME", "MODULE_AUTHOR", "MODULE_DESCRIPTION"]]),
                 [importlib.import_module(f"showcases.{x.split('.')[0]}") for x in all_modules]))

        # Adding showcases to listbox
        self.modules_listbox.delete(0, "end")
        for showcase in showcases:
            self.modules_listbox.insert("end", showcase.MODULE_NAME)

        # Returning showcases
        return showcases

    def check_module_conditions(self, module):
        if "MODULE_CONDITIONS" in dir(module):
            # For future version consider using * for more arguments?
            for function_name, argument, error_message in module.MODULE_CONDITIONS:
                function = getattr(conditions, function_name)
                if not function(self, argument):
                    self.add_to_log(error_message)
                    return False
        return True

    def view_selected_showcase(self):
        if self.showcase_window is not None:
            return  # To prevent Double-Button loophole abuse

        if not self.modules_listbox.curselection():
            messagebox.showerror("Error", "Please select a showcase.")
            return

        # Getting index of module and loading it
        selected_module = self.modules[self.modules_listbox.curselection()[0]]
        if self.check_module_conditions(selected_module):
            self.showcase_window = ShowcaseWindow(self, selected_module)
            self.add_to_log(f"Loaded showcase \"{selected_module.MODULE_NAME}\".")
            self.lock()

    def load_external_showcase(self):
        # Finding path
        module_path = filedialog.askopenfilename(
            title="Open external showcase",
            filetypes=[("Python module", ".py")]
        )
        module_filename = module_path.split("/")[-1]

        # Ensuring the user didn't cancel
        if not module_path:
            return

        # Importing dynamically
        spec = importlib.util.spec_from_file_location(module_filename.split(".")[0], module_path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)

        # Checking if there is a Showcase inside the module
        if "Showcase" not in dir(module):
            messagebox.showerror("Error", "This Python module does not contain a viewable showcase.")
            return

        # Load module
        if self.check_module_conditions(module):
            self.showcase_window = ShowcaseWindow(self, module)
            self.add_to_log(f"Loaded showcase \"{module.MODULE_NAME}\".")
            self.lock()


    def update_showcases(self):
        self.modules = self.scan_showcases()

    def view_showcase_description(self):
        if not self.modules_listbox.curselection():
            messagebox.showerror("Error", "Please select a showcase.")
            return

        # Getting module index and showing description
        selected_module = self.modules[self.modules_listbox.curselection()[0]]
        self.showcase_description_window = ShowcaseDescriptionWindow(self, selected_module.MODULE_NAME, selected_module.MODULE_AUTHOR,
                                                                     selected_module.MODULE_DESCRIPTION)
        self.lock()
    def unlock(self):
        # Enables all widgets below when there is no showcase running
        self.run_module_button.config(state="normal")
        self.open_external_module_button.config(state="normal")
        self.scan_for_modules_button.config(state="normal")
        self.view_module_description_button.config(state="normal")
        self.modules_listbox.config(state="normal")

    def lock(self):
        # Disables all widgets during a showcase.
        self.run_module_button.config(state="disabled")
        self.open_external_module_button.config(state="disabled")
        self.scan_for_modules_button.config(state="disabled")
        self.view_module_description_button.config(state="disabled")
        self.modules_listbox.config(state="disabled")

    def add_to_log(self, text):
        self.logs_listbox.insert("end", f"[{strftime('%d/%m %H:%M:%S', localtime())}] {text}")

    def confirm_exit(self):
        if messagebox.askyesno("Confirm exit", "Are you sure you want to quit?"):
            sys.exit()
