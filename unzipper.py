from zipfile import ZipFile
import tkinter as tk
from tkinter import filedialog
import os

# Opens explore to navigate to directory, return directory
def search_for_file_path(text_box=""):
    currdir = os.getcwd()
    tempdir = filedialog.askdirectory(parent=window, initialdir=currdir, title='Please select a directory')
    if len(tempdir) > 0:
        print ("You chose: %s" % tempdir)  	
    return tempdir

# RETHINK THIS SECTION. There has to be a way to put this output functiosn into serach_for_file_path
# Prints to parent folder text box
def parent_output():
	text = search_for_file_path()
	# Clear text box if requried
	parent_txt.delete("1.0", tk.END)
	parent_txt.insert("1.0", text)

# Prints to destination folder text box
def dest_output():
	text = search_for_file_path()
	dest_txt.delete("1.0", tk.END)
	dest_txt.insert("1.0", text)

# Returns all filepaths in directory with .zip files
def get_all_file_paths(directory):
	# Initialize lists for appending
	file_paths = []
	roots = []
	zip_files = []

	#crawl through directory. os.walk generates file names. 
	for root, directories, files in os.walk(directory):
		for filename in files:
			if filename.endswith('.zip'):
				# Log roots, filenames, and full file paths
				roots.append(root)
				zip_files.append(filename)
				filepath = os.path.join(root, filename)
				file_paths.append(filepath)
	return file_paths, roots, zip_files

def main():
	# Get parent and destination paths
	home_directory = parent_txt.get("1.0", tk.END).rstrip()
	dest_directory = dest_txt.get("1.0", tk.END).rstrip()

	# Calling function to get filepaths
	file_paths, roots, zip_files = get_all_file_paths(home_directory)
	text.insert(tk.END, "The files listed below have been unzipped: ")
	# Unzip each file
	for i in range(len(file_paths)):
		try:
			# Change to relevant working directory
			os.chdir(roots[i])
			# Unzip
			with ZipFile(zip_files[i], 'r') as zip:
				text.insert(tk.END, f"\n{file_paths[i]}")	# Displays unzipped fiels in GUI
				zip.printdir()								# Prints nice table to console
				zip.extractall(path=dest_directory)			# Unzip to directory
		except:
			raise ValueError("Can't move into that directory")
	# Print new line for next run
	text.insert(tk.END, "\n")

# Build GUI ------------------------------------------------------------

window = tk.Tk()
frame_a = tk.Frame()	# Heading
frame_b = tk.Frame()	# Button

# GUI Label
header = tk.Label(
	master=frame_a,
	text="Unzipper Program"
	)
header.pack()
frame_a.pack()

# Button to choose parent folder
button_p = tk.Button(
	text='Choose Parent Folder',
	command = parent_output,
	master=frame_b
	)
button_p.pack()

# Parent folder text output
parent_txt = tk.Text(
	master=frame_b,
	height=2
	)
parent_txt.pack()

# Button to choose destination for files
button_d = tk.Button(
	text='Choose Destination Folder',
	command=dest_output,
	master=frame_b
	)
button_d.pack()

# Destination folder text output
dest_txt = tk.Text(
	master=frame_b,
	height=2
	)
dest_txt.pack()

# Button to run unzipper
button_r = tk.Button(
	text='Unzip Files',
	command=main,
	master=frame_b
	)
button_r.pack()

text = tk.Text(
	master=frame_b,
	)
text.pack()
frame_b.pack()

window.mainloop()
