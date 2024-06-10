import tkinter as tk
from tkinter import ttk, Frame, filedialog, scrolledtext
from PIL import Image, ImageTk
from tkinter import font as tkFont
import subprocess
import os
import shutil
import threading

class MainApplication(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("ML Genome Classifier")
        #self.geometry("1024x700")
        
        # Set the icon for the window
        #self.iconbitmap('misc/favicon.ico')

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        
        self.buttons_frame = tk.Frame(self, bg="white", bd=2, relief="ridge")
        self.buttons_frame.grid(row=0, column=0, sticky="nsew")
        self.buttons_frame.grid_rowconfigure(0, weight=1)
        self.buttons_frame.grid_columnconfigure(0, weight=1)

        
        self.probml_button = tk.Button(self.buttons_frame, text="ProbML\nModule", command=self.open_probml_page)
        self.kmers_button = tk.Button(self.buttons_frame, text="K-mer\nGeneration", command=self.open_kmers_page)
        self.training_button = tk.Button(self.buttons_frame, text="Train\nModels", command=self.open_training_page)
        self.classifying_button = tk.Button(self.buttons_frame, text="Predictions", command=self.open_classifying_page)

        # Making the button labels bold
        button_font_style = tkFont.Font(weight="bold", size="14", family="Arial")

        self.probml_button.config(font=button_font_style)
        self.kmers_button.config(font=button_font_style)
        self.training_button.config(font=button_font_style)
        self.classifying_button.config(font=button_font_style)

        # Changing the button features
        button_bg = "lavender"
        button_fg = "dark slate gray"
        button_relief = "flat"
        button_overelief = "raised"
        button_bd = "5"
        button_height = "5"
        button_width = "10"

 
        self.probml_button.config(bg=button_bg, fg=button_fg, relief=button_relief, bd=button_bd, height=button_height, width=button_width, overrelief=button_overelief)
        self.kmers_button.config(bg=button_bg, fg=button_fg, relief=button_relief, bd=button_bd, height=button_height, width=button_width, overrelief=button_overelief)
        self.training_button.config(bg=button_bg, fg=button_fg, relief=button_relief, bd=button_bd, height=button_height, width=button_width, overrelief=button_overelief)
        self.classifying_button.config(bg=button_bg, fg=button_fg, relief=button_relief, bd=button_bd, height=button_height, width=button_width, overrelief=button_overelief)


        self.probml_button.pack(fill="both", pady=10, padx=10, expand=True)
        self.kmers_button.pack(fill="both", pady=10, padx=10, expand=True)
        self.training_button.pack(fill="both", pady=10, padx=10, expand=True)
        self.classifying_button.pack(fill="both", pady=10, padx=10, expand=True)


        # Initializing the frames_container
        self.frames_container = tk.Frame(self, bg="white", bd=2, relief="groove")
        self.frames_container.grid(row=0, column=1, sticky="nsew")
        self.frames_container.grid_rowconfigure(0, weight=1)
        self.frames_container.grid_rowconfigure(1, weight=1)
        self.frames_container.grid_columnconfigure(0, weight=1)
        

        # Subtitle frame
        #self.subtitle_frame = tk.Frame(self.frames_container)
        #self.subtitle_frame.grid(row=0, column=0, padx=10, pady=10)

        # Create the label with the specified text
        #self.subtitle_label = tk.Label(self.subtitle_frame, text="Machine Learning Based Genome Classifcation")
        
        # Set the font to bold and size 16 pts
        #font_style = tkFont.Font(family="Arial", size=12, weight="bold")
        #self.subtitle_label.config(font=font_style)
        # Pack the label inside the frame
        #self.subtitle_label.pack(pady=10, padx=10)


        # Create a container frame for image
        self.image_console_container = tk.Frame(self.frames_container, bd=2, relief="ridge", bg="white")
        self.image_console_container.grid(row=0, column=0, sticky="nsew", pady=10, padx=10)
        self.image_console_container.grid_columnconfigure(0, weight=1)
        self.image_console_container.grid_rowconfigure(0, weight=1)

        # Add an image 
        self.image_path = "misc/banner.png" 
        self.image_label = tk.Label(self.image_console_container, bg="white")
        self.load_image()       

        # Widget for console
        self.console_container = tk.Frame(self.frames_container, bd=2, relief="ridge")
        self.console_container.grid(row=1, column=0, sticky="nsew", pady=10, padx=10)
        self.console_container.grid_columnconfigure(0, weight=1)
        self.console_container.grid_rowconfigure(0, weight=1)
        self.console_text = scrolledtext.ScrolledText(self.console_container, state='disabled', height=10, bg="lavender", fg="navy")
        self.console_text.grid(row=0, column=0, sticky="nsew")

        # Footnote
        self.footnote_text = tk.Label(self, text="(c) Systems Biology Lab, IIT Mandi")
        self.footnote_text.grid(row=2, column=0, sticky="w", padx=10)
        
        # Manual button
        self.manual_button = tk.Button(self, text="Help", command=self.open_help_page, relief="flat")
        self.manual_button.grid(row=2, column=1, sticky="e", padx=10)

        # Initializing the different frames
        self.probml_frame = ProbMLFrame(self.frames_container, self)
        self.kmers_frame = GenerateKmersFrame(self.frames_container, self)
        self.classification_frame = ClassificationFrame(self.frames_container, self)
        self.training_frame = TrainingFrame(self.frames_container, self)
        self.help_frame = HelpFrame(self.frames_container, self)

        # Initializing active frames
        self.active_frame = self.image_console_container

    def load_image(self):
        image = Image.open(self.image_path)
        image = image.resize((800, 392))
        self.image_tk = ImageTk.PhotoImage(image)
        self.image_label.config(image=self.image_tk)
        self.image_label.pack(anchor="center", expand=True, fill='both')

    def hide_active_frame(self):
        if self.active_frame is not None:
            self.active_frame.grid_forget()
            self.active_frame = None

    def open_probml_page(self):
        self.log_to_console("Opening ProbML module")
        self.hide_active_frame()
        self.active_frame = self.probml_frame
        self.probml_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        

    def open_kmers_page(self):
        self.log_to_console("Opening Kmer module")
        self.hide_active_frame()
        self.active_frame = self.kmers_frame
        self.kmers_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        

    def open_classifying_page(self):
        self.log_to_console("Opening Classification module")
        self.hide_active_frame()
        self.active_frame = self.classification_frame
        self.classification_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

    def open_training_page(self):
        self.log_to_console("Opening Training module")
        self.hide_active_frame()
        self.active_frame = self.training_frame
        self.training_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

    def open_help_page(self):
        self.log_to_console("Opening help page")
        self.hide_active_frame()
        self.active_frame = self.help_frame
        self.help_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

    def log_to_console(self, text):
        self.console_text.config(state='normal')
        self.console_text.insert(tk.END, text + "\n")
        self.console_text.see(tk.END)
        self.console_text.config(state='disabled')


# ProbML Frame begins here
class ProbMLFrame(tk.Frame):
    def __init__(self, master=None, app=None):

        frame_bg = "lavender"

        tk.Frame.__init__(self, master, bd=2, relief="ridge", bg=frame_bg)
        self.app = app

        for i in range(3):
            self.grid_columnconfigure(i, weight=1)

        for i in range(6):
            self.grid_rowconfigure(i, weight=1)


        # Subtitle frame
        #self.subtitle_frame = tk.Frame(self)
        #self.subtitle_frame.grid(row=0, column=1, columnspan=0,padx=10, pady=10)

        # Create the label with the specified text
        self.subtitle_label = tk.Label(self, text="Classify your genome(s) with XGB_LD3_IITMd models", bg=frame_bg)
        
        # Set the font to bold and size 16 pts
        font_style = tkFont.Font(family="Arial", size=12, weight="bold")
        self.subtitle_label.config(font=font_style)
        
        # Pack the label inside the frame
        self.subtitle_label.grid(row=0, column=1, columnspan=1, pady=10, padx=10, sticky="ew")


        self.upload_label = tk.Label(self, text="Choose your genome:", bg=frame_bg)
        self.upload_label.grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.upload_button = tk.Button(self, text="Upload Genome", command=self.upload_genome, anchor="center", width=20, bg=frame_bg)
        self.upload_button.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
       
        self.file_path_label = tk.Label(self, text="No file(s) selected", bg=frame_bg)
        self.file_path_label.grid(row=1, column=2, padx=10, pady=10, sticky="w")

        # Radio button for manual model selection
        # self.manual_model_var = tk.StringVar(value="Auto")
        # self.manual_radio = tk.Radiobutton(self, text="Manually select a model", variable=self.manual_model_var, value="Manual", command=self.toggle_model_selection, bg=frame_bg)
        # self.manual_radio.grid(row=2, column=1, padx=10, pady=10, sticky="ew")

        self.manual_model_var = tk.BooleanVar(value=False)
        self.manual_checkbutton = tk.Checkbutton(self, text="Manually select a model", variable=self.manual_model_var, command=self.toggle_model_selection, bg=frame_bg)
        self.manual_checkbutton.grid(row=2, column=1, padx=10, pady=10, sticky="ew")

        # Help button and tooltip for model section
        self.model_help_button = RoundButton(self, width=23, height=23, text="?")
        self.model_help_button.grid(row=2, column=1, padx=100, sticky="e")
        Tooltip(self.model_help_button, "Enable this option to manually select a model from a set of 12 in-house trained XGB_LD3_IITMd models. If disabled, a model will be randomly chosen for you.")
           
        self.dropbox_label = tk.Label(self, text="ProbML Models:", bg=frame_bg)
        self.model_combo = ttk.Combobox(self, values=["Model 1", "Model 2", "Model 3", "Model 4", "Model 5", "Model 6", "Model 7", "Model 8", "Model 9", "Model 10", "Model 11", "Model 12"], width=18)
        self.dropbox_label.grid(row=3, column=0, padx=10, pady=10, sticky="e")
        self.model_combo.grid(row=3, column=1, padx=10, pady=10, sticky="ew")
        self.dropbox_label.grid_remove()
        self.model_combo.grid_remove()

        self.model_combo.bind("<<ComboboxSelected>>", self.update_model_label)

        self.status_label = tk.Label(self, text="Status:", bg=frame_bg)
        self.status_label.grid(row=4, column=0, padx=10, pady=10, sticky="e")
        self.status_label2 = tk.Label(self, text="Waiting", bg=frame_bg)
        self.status_label2.grid(row=4, column=1, padx=10, pady=10, sticky="ew")

        self.submit_button = tk.Button(self, text="Submit", command=self.submit, width=10, bg=frame_bg)
        self.submit_button.grid(row=5, column=1, pady=10)

        self.file_path = None
        self.model_label = "Random"  # Default model label


    def upload_genome(self):
        self.file_path = filedialog.askopenfilename(multiple=True)

        # Update the label with the multiple file paths
        if self.file_path:
            filenames = ", ".join([os.path.basename(file) for file in self.file_path])
            num_files = len(filenames.split(", "))
            self.file_path_label.config(text=f"{num_files} file(s) selected")

    def toggle_model_selection(self):
        if self.manual_model_var.get():
            self.dropbox_label.grid()
            self.model_combo.grid()  # Show the combobox
            self.model_label = self.model_combo.get() if self.model_combo.get() else "Random"
        else:
            self.dropbox_label.grid_remove()
            self.model_combo.grid_remove()  # Hide the combobox
            self.model_label = "Random"

    def update_model_label(self, event):
        if self.manual_model_var.get():
            self.model_label = self.model_combo.get()


    def submit(self):
        
        if self.file_path:

            #Make a temp dir for processing and storing intermediate files
            if os.path.exists('tmp'):
                shutil.rmtree('tmp')
                os.mkdir('tmp')
            else:
                os.mkdir('tmp')

            # Open the file in write mode and write the FILE PATH
            fname = "\n".join(self.file_path)
            with open("tmp/file_path.txt", "w") as file:
                file.write(fname)

            def run_subprocess():
                self.app.log_to_console("Attempting to invoke the ProbML subprocess")
                #model_label = self.model_label
                process = subprocess.Popen(
                ["python", "scripts/probml.py", self.model_label], 
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
                )

                for stdout_line in iter(process.stdout.readline, ""):
                    self.app.log_to_console(stdout_line.strip())
                for stderr_line in iter(process.stderr.readline, ""):
                    self.app.log_to_console(stderr_line.strip())

                process.stdout.close()
                process.stderr.close()
                return_code = process.wait()
                if return_code:
                    raise subprocess.CalledProcessError(return_code, process.args)

                self.status_label2.config(text="Completed!")
                
                #Remove tmp folder
                if os.path.exists('tmp'):
                    shutil.rmtree('tmp')
                    
            self.status_label2.config(text="Submitted")
            threading.Thread(target=run_subprocess).start()

        else:
            self.status_label2.config(text="Please choose a genome")


# Kmer generation Frame begins here
class GenerateKmersFrame(tk.Frame):
    def __init__(self, master=None, app=None):

        frame_bg = "lavender"

        tk.Frame.__init__(self, master, bd=2, relief="ridge", bg=frame_bg)
        self.app = app

        for i in range(3):
            self.grid_columnconfigure(i, weight=1)

        for i in range(8):
            self.grid_rowconfigure(i, weight=1)

        # Subtitle frame
        self.subtitle_frame = tk.Frame(self, bg=frame_bg)
        self.subtitle_frame.grid(row=0, column=1, padx=10, pady=10)

        # Create the label with the specified text
        self.subtitle_label = tk.Label(self.subtitle_frame, text="Generate K-mers for your genome(s)", bg=frame_bg)
        
        # Set the font to bold and size 16 pts
        font_style = tkFont.Font(family="Arial", size=12, weight="bold")
        self.subtitle_label.config(font=font_style)
        
        # Pack the label inside the frame
        self.subtitle_label.pack(pady=10, padx=10)

        self.category_label = tk.Label(self, text="Category Label:", bg=frame_bg)
        self.category_combo = ttk.Combobox(self, values=["Positive", "Negative"], width=18)
        self.category_label.grid(row=2, column=0, padx=10, pady=20, sticky="e")
        self.category_combo.grid(row=2, column=1, padx=10, pady=20, sticky="ew")

        # Help button and tooltip 
        self.category_help_button = RoundButton(self, width=23, height=23, text="?")
        self.category_help_button.grid(row=2, column=2, padx=10, sticky="w")
        Tooltip(self.category_help_button, "Select a category to label your datasets between two contrasting traits or distinct features. For example, Probiotics can be labeled as positive, while Pathogenic can be labeled as negative")

        self.min_kmer_label = tk.Label(self, text="Minimum K-mer value:", bg=frame_bg)
        self.min_kmer_entry = tk.Entry(self)
        self.max_kmer_label = tk.Label(self, text="Maximum K-mer value:", bg=frame_bg)
        self.max_kmer_entry = tk.Entry(self)
        self.min_kmer_label.grid(row=3, column=0, padx=10, pady=20, sticky="e")
        self.min_kmer_entry.grid(row=3, column=1, padx=10, pady=20, sticky="ew")
        self.max_kmer_label.grid(row=4, column=0, padx=10, pady=20, sticky="e")
        self.max_kmer_entry.grid(row=4, column=1, padx=10, pady=20, sticky="ew")

        self.upload_label = tk.Label(self, text="Choose your genome:", bg=frame_bg)
        self.upload_label.grid(row=5, column=0, padx=10, pady=20, sticky="e")
        self.upload_button = tk.Button(self, text="Upload Genome", command=self.upload_genome, anchor="center", width=20, bg=frame_bg)
        self.upload_button.grid(row=5, column=1, padx=10, pady=20, sticky="ew")

        self.file_path_label = tk.Label(self, text="No file(s) selected", bg=frame_bg)
        self.file_path_label.grid(row=5, column=2, padx=10, pady=20, sticky="w")

        self.status_label = tk.Label(self, text="Status:", bg=frame_bg)
        self.status_label.grid(row=6, column=0, padx=10, pady=20, sticky="e")
        self.status_label2 = tk.Label(self, text="Waiting", bg=frame_bg)
        self.status_label2.grid(row=6, column=1, padx=20, pady=20, sticky="ew")

        self.submit_button = tk.Button(self, text="Submit", command=self.submit, width=10, bg=frame_bg)
        self.submit_button.grid(row=7, column=1, columnspan=1, pady=20)

        self.file_path = None


    def upload_genome(self):
        self.file_path = filedialog.askopenfilename(multiple=True)

        # Update the label with the multiple file paths
        if self.file_path:
            filenames = ", ".join([os.path.basename(file) for file in self.file_path])
            num_files = len(filenames.split(", "))
            self.file_path_label.config(text=f"{num_files} file(s) selected")


    def submit(self):
        if self.file_path:

            #Make a temp dir for processing and storing intermediate files
            if os.path.exists('tmp'):
                shutil.rmtree('tmp')
                os.mkdir('tmp')
            else:
                os.mkdir('tmp')

            # Open the file in write mode and write the FILE PATH
            fname = "\n".join(self.file_path)
            with open("tmp/file_path.txt", "w") as file:
                file.write(fname)  


            def run_subprocess():
                self.app.log_to_console("Attempting to invoke the Kmer generation subprocess")    
                category_label = self.category_combo.get()
                min_kmer_value = self.min_kmer_entry.get()
                max_kmer_value = self.max_kmer_entry.get()
                output_file_path = f"{category_label}_kmer_matrix.csv"
                input_file_path = "tmp/file_path.txt"

                if category_label:

                    process = subprocess.Popen(
                    ["python", "scripts/f2m.py", min_kmer_value, max_kmer_value, category_label, output_file_path, input_file_path],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                    )

                    for stdout_line in iter(process.stdout.readline, ""):
                        self.app.log_to_console(stdout_line.strip())
                    for stderr_line in iter(process.stderr.readline, ""):
                        self.app.log_to_console(stderr_line.strip())

                    process.stdout.close()
                    process.stderr.close()
                    return_code = process.wait()
                    if return_code:
                        raise subprocess.CalledProcessError(return_code, process.args)

                    self.status_label2.config(text="Completed!")

                    if os.path.exists('tmp'):
                        shutil.rmtree('tmp')

                else:
                    self.status_label2.config(text="Please choose a category Label")   
                    
            self.status_label2.config(text="Submitted")
            threading.Thread(target=run_subprocess).start()    
        else:
            self.status_label2.config(text="Please choose a Genome") 


# Training Frame begins here
class TrainingFrame(tk.Frame):
    def __init__(self, master=None, app=None):

        frame_bg = "lavender"

        tk.Frame.__init__(self, master, bd=2, relief="ridge", bg=frame_bg)
        self.app = app

        for i in range(3):
            self.grid_columnconfigure(i, weight=1)

        for i in range(7):
            self.grid_rowconfigure(i, weight=1)

        # Subtitle frame
        self.subtitle_frame = tk.Frame(self, bg=frame_bg)
        self.subtitle_frame.grid(row=0, column=1, padx=10, pady=10)

        # Create the label with the specified text
        self.subtitle_label = tk.Label(self.subtitle_frame, text="Train your own ML models", bg=frame_bg)
        
        # Set the font to bold and size 16 pts
        font_style = tkFont.Font(family="Arial", size=12, weight="bold")
        self.subtitle_label.config(font=font_style)
        
        # Pack the label inside the frame
        self.subtitle_label.pack(pady=10, padx=10)

        self.upload1_label = tk.Label(self, text="Choose positive kmer dataset:", bg=frame_bg)
        self.upload1_label.grid(row=1, column=0, padx=10, pady=20, sticky="e")
        self.upload1_button = tk.Button(self, text="Upload kmer", command=self.upload_pos, anchor="center", width=20, bg=frame_bg)
        self.upload1_button.grid(row=1, column=1, padx=10, pady=20, sticky="ew")

        self.upload2_label = tk.Label(self, text="Choose negative kmer dataset:", bg=frame_bg)
        self.upload2_label.grid(row=2, column=0, padx=10, pady=20, sticky="e")
        self.upload2_button = tk.Button(self, text="Upload kmer", command=self.upload_neg, anchor="center", width=20, bg=frame_bg)
        self.upload2_button.grid(row=2, column=1, padx=10, pady=20, sticky="ew")

        self.file_path_pos_label = tk.Label(self, text="No file(s) selected", bg=frame_bg)
        self.file_path_pos_label.grid(row=1, column=2, padx=10, pady=20, sticky="w")
        self.file_path_neg_label = tk.Label(self, text="No file(s) selected", bg=frame_bg)
        self.file_path_neg_label.grid(row=2, column=2, padx=10, pady=20, sticky="w")

        self.category_label = tk.Label(self, text="Choose the model:", bg=frame_bg)
        self.model_combo = ttk.Combobox(self, values=["DecisionTree", "KNN", "RandomForest", "SVM", "XGBoost"], width=20)
        self.category_label.grid(row=3, column=0, padx=10, pady=20, sticky="e")
        self.model_combo.grid(row=3, column=1, padx=10, pady=20, sticky="ew")

        self.split_label = tk.Label(self, text="Data partition (train:test):", bg=frame_bg)
        self.split_combo = ttk.Combobox(self, values=["50:50", "60:40", "70:30", "80:20", "90:10"], width=20)
        self.split_label.grid(row=4, column=0, padx=10, pady=20, sticky="e")
        self.split_combo.grid(row=4, column=1, padx=10, pady=20, sticky="ew")         

        self.status_label = tk.Label(self, text="Status:", bg=frame_bg)
        self.status_label.grid(row=5, column=0, padx=10, pady=20, sticky="e")
        self.status_label2 = tk.Label(self, text="Waiting", bg=frame_bg)
        self.status_label2.grid(row=5, column=1, padx=20, pady=20, sticky="ew")

        self.submit_button = tk.Button(self, text="Submit", command=self.submit, width=10, bg=frame_bg)
        self.submit_button.grid(row=6, column=1, columnspan=1, pady=20)

        #Initializing path variables
        self.file_path_pos = None
        self.file_path_neg = None

    def upload_pos(self):
        self.file_path_pos = filedialog.askopenfilename()

        #Update the label with the single file path
        if self.file_path_pos:
            filename = os.path.basename(self.file_path_pos)
            self.file_path_pos_label.config(text=filename)

    def upload_neg(self):
        self.file_path_neg = filedialog.askopenfilename()

        #Update the label with the single file path
        if self.file_path_neg:
            filename = os.path.basename(self.file_path_neg)
            self.file_path_neg_label.config(text=filename)

    def submit(self):

        if self.file_path_pos:
            if self.file_path_neg:

                def run_subprocess():
                    #Make a temp dir for processing and storing intermediate files
                    if os.path.exists('tmp'):
                        shutil.rmtree('tmp')
                        os.mkdir('tmp')
                    else:
                        os.mkdir('tmp')

                    self.app.log_to_console("Attempting to invoke the training subprocess")
                    model_label = self.model_combo.get()
                    dataset_split = self.split_combo.get()

                    process = subprocess.Popen(
                    ["python", "scripts/training.py", model_label, self.file_path_pos, self.file_path_neg, dataset_split], stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                    )

                    for stdout_line in iter(process.stdout.readline, ""):
                        self.app.log_to_console(stdout_line.strip())
                    for stderr_line in iter(process.stderr.readline, ""):
                        self.app.log_to_console(stderr_line.strip())

                    process.stdout.close()
                    process.stderr.close()
                    return_code = process.wait()
                    if return_code:
                        raise subprocess.CalledProcessError(return_code, process.args)
                    
                    self.status_label2.config(text="Completed!")

                    if os.path.exists('tmp'):
                        shutil.rmtree('tmp')
                        

                self.status_label2.config(text="Submitted")
                threading.Thread(target=run_subprocess).start()

            else:
                self.status_label2.config(text="Please choose a negative dataset")

        else:
            self.status_label2.config(text="Please choose a positive dataset")


# Classification Frame begins here
class ClassificationFrame(tk.Frame):
    def __init__(self, master=None, app=None):

        frame_bg = "lavender"

        tk.Frame.__init__(self, master, bd=2, relief="ridge", bg=frame_bg)
        self.app = app

        for i in range(3):
            self.grid_columnconfigure(i, weight=1)

        for i in range(7):
            self.grid_rowconfigure(i, weight=1)


        # Subtitle frame
        self.subtitle_frame = tk.Frame(self, bg=frame_bg)
        self.subtitle_frame.grid(row=0, column=1, padx=10, pady=10)

        # Create the label with the specified text
        self.subtitle_label = tk.Label(self.subtitle_frame, text="Classify genome(s) using your own model", bg=frame_bg)
        
        # Set the font to bold and size 16 pts
        font_style = tkFont.Font(family="Arial", size=12, weight="bold")
        self.subtitle_label.config(font=font_style)
        
        # Pack the label inside the frame
        self.subtitle_label.pack(pady=10, padx=10)

        self.upload_label = tk.Label(self, text="Choose your genome:", bg=frame_bg)
        self.upload_label.grid(row=1, column=0, padx=10, pady=20, sticky="e")
        self.upload_button = tk.Button(self, text="Upload Genome", command=self.upload_genome, anchor="center", width=20, bg=frame_bg)
        self.upload_button.grid(row=1, column=1, padx=10, pady=20, sticky="ew")
       
        self.file_path_label = tk.Label(self, text="No file(s) selected", bg=frame_bg)
        self.file_path_label.grid(row=1, column=2, padx=10, pady=20, sticky="w")
       
        self.your_label = tk.Label(self, text="Choose your Model:", bg=frame_bg)
        self.your_label.grid(row=2, column=0, padx=10, pady=20, sticky="e")
        self.your_button = tk.Button(self, text="Upload Model", command=self.upload_model, anchor="center", width=20, bg=frame_bg)
        self.your_button.grid(row=2, column=1, padx=10, pady=20, sticky="ew")

        self.your_path_label = tk.Label(self, text="No file(s) selected", bg=frame_bg)
        self.your_path_label.grid(row=2, column=2, padx=10, pady=20, sticky="w")

        self.min_kmer_label = tk.Label(self, text="Minimum K-mer value:", bg=frame_bg)
        self.min_kmer_entry = tk.Entry(self)
        self.max_kmer_label = tk.Label(self, text="Maximum K-mer value:", bg=frame_bg)
        self.max_kmer_entry = tk.Entry(self)
        self.min_kmer_label.grid(row=3, column=0, padx=10, pady=20, sticky="e")
        self.min_kmer_entry.grid(row=3, column=1, padx=10, pady=20, sticky="ew")
        self.max_kmer_label.grid(row=4, column=0, padx=10, pady=20, sticky="e")
        self.max_kmer_entry.grid(row=4, column=1, padx=10, pady=20, sticky="ew")

        # Help button and tooltip 
        self.min_help_button = RoundButton(self, width=23, height=23, text="?")
        self.min_help_button.grid(row=3, column=2, padx=10, sticky="w")
        Tooltip(self.min_help_button, "Specify the minimum k-mer value utilized in generating the datasets employed to train your chosen model.")

        # Help button and tooltip 
        self.max_help_button = RoundButton(self, width=23, height=23, text="?")
        self.max_help_button.grid(row=4, column=2, padx=10, sticky="w")
        Tooltip(self.max_help_button, "Specify the maximum k-mer value utilized in generating the datasets employed to train your chosen model.")

        self.status_label = tk.Label(self, text="Status:", bg=frame_bg)
        self.status_label.grid(row=5, column=0, padx=10, pady=20, sticky="e")
        self.status_label2 = tk.Label(self, text="Waiting", bg=frame_bg)
        self.status_label2.grid(row=5, column=1, padx=20, pady=20, sticky="ew")

        self.submit_button = tk.Button(self, text="Submit", command=self.submit, width=10, bg=frame_bg)
        self.submit_button.grid(row=6, column=1, columnspan=1, pady=20)

        self.file_path = None
        self.your_path = None

    def upload_genome(self):
        self.file_path = filedialog.askopenfilename(multiple=True)

        # Update the label with the multiple file paths
        if self.file_path:
            filenames = ", ".join([os.path.basename(file) for file in self.file_path])
            num_files = len(filenames.split(", "))
            self.file_path_label.config(text=f"{num_files} file(s) selected")

    def upload_model(self):
        self.your_path = filedialog.askopenfilename()

        # Update the label with the file path
        if self.your_path:
            filename = os.path.basename(self.your_path)
            self.your_path_label.config(text=filename)

    def submit(self):
        
        # Check If you have path for genome 
        if self.file_path:
            
            #Make a temp dir for processing and storing intermediate files
            if os.path.exists('tmp'):
                shutil.rmtree('tmp')
                os.mkdir('tmp')
            else:
                os.mkdir('tmp')

            # Open the file in write mode and write the FILE PATHS
            fname = "\n".join(self.file_path)
            with open("tmp/file_path.txt", "w") as file:
                file.write(fname)

            # Check If you have path for model
            if self.your_path:

                def run_subprocess():
                    self.app.log_to_console("Attempting to invoke the classification subprocess")
                    min_kmer_value = self.min_kmer_entry.get()
                    max_kmer_value = self.max_kmer_entry.get()

                    process = subprocess.Popen(
                    ["python", "scripts/classification.py", self.your_path, min_kmer_value, max_kmer_value], 
                    stdout=subprocess.PIPE, 
                    stderr=subprocess.PIPE,
                    text=True)
                    
                    
                    for stdout_line in iter(process.stdout.readline, ""):
                        self.app.log_to_console(stdout_line.strip())
                    for stderr_line in iter(process.stderr.readline, ""):
                        self.app.log_to_console(stderr_line.strip())

                    process.stdout.close()
                    process.stderr.close()
                    return_code = process.wait()
                    if return_code:
                        raise subprocess.CalledProcessError(return_code, process.args)

                    self.status_label2.config(text="Completed!")
                    if os.path.exists('tmp'):
                        shutil.rmtree('tmp')
                        
                self.status_label2.config(text="Submitted")
                threading.Thread(target=run_subprocess).start()

            else:
                self.status_label2.config(text="Please choose a model")
            

        else:
            self.status_label2.config(text="Please choose a genome")    
            

class HelpFrame(tk.Frame):
    def __init__(self, master=None, app=None):
        tk.Frame.__init__(self, master, bd=2, relief="ridge", bg="white")
        self.app = app

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        #for i in range(2):
        #    self.grid_rowconfigure(i, weight=1)

        # Subtitle frame
        self.subtitle_frame = tk.Frame(self, bg="white")
        self.subtitle_frame.grid(row=0, column=0, padx=10, pady=10)

        # Subtitle 
        self.subtitle_label = tk.Label(self.subtitle_frame, text="Help Page", bg="white")
        self.subtitle_label.pack(pady=10, padx=10)
        font_style = tkFont.Font(family="Arial", size=12, weight="bold")
        self.subtitle_label.config(font=font_style)

        # # Text Scroll widget
        # self.text_container = tk.Frame(self, bd=2, relief="ridge")
        # self.text_container.grid(row=1, column=0, sticky="nsew", pady=10, padx=10)
        # self.content_text = scrolledtext.ScrolledText(self.text_container, state='disabled', height=10)

        # Widget for console
        self.text_container = tk.Frame(self, bd=2, relief="ridge")
        self.text_container.grid(row=1, column=0, sticky="nsew", pady=10, padx=10)
        self.text_container.grid_columnconfigure(0, weight=1)
        self.text_container.grid_rowconfigure(0, weight=1)
        self.text_content = scrolledtext.ScrolledText(self.text_container, state='disabled')
        self.text_content.grid(row=0, column=0, sticky="nsew")
        
        with open("README.md", 'r') as file:
                text = file.read()

        # Enable the text widget to insert content
        self.text_content.config(state='normal')
        self.text_content.insert('1.0', text)
        # Optionally, disable the text widget to prevent user from editing
        self.text_content.config(state='disabled')
 

class Tooltip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip_window = None
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event):
        x = self.widget.winfo_rootx() + self.widget.winfo_width() + 5
        y = self.widget.winfo_rooty() + 5
        self.tooltip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(tw, text=self.text, background="white", relief="solid", borderwidth=1, wraplength=200, justify="left", padx=5, pady=5)
        label.pack()

    def hide_tooltip(self, event):
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None


class RoundButton(tk.Canvas):
    def __init__(self, parent, width, height, text, command=None, **kwargs):
        super().__init__(parent, width=width, height=height, bg=kwargs.get('bg', 'lavender'), highlightthickness=0)
        self.command = command
        self.width = width
        self.height = height

        # Create a circle
        self.create_oval(2, 2, width, height, fill=kwargs.get('fill', 'white'), outline=kwargs.get('outline', 'lavender'))
        
        # Create text
        self.create_text(width/1.8, height/1.8, text=text, fill=kwargs.get('text_color', 'black'), font=("Arial", 12, "bold"))

        # Bind events
        self.bind("<Button-1>", self.on_click)

    def on_click(self, event):
        if self.command:
            self.command()



if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()
