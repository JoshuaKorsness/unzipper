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
def parent_output():
	text = search_for_file_path()
	# Clear text box if requried
	parent_txt.delete("1.0", tk.END)
	parent_txt.insert("1.0", text)

def dest_output():
	text = search_for_file_path()
	dest_txt.delete("1.0", tk.END)
	dest_txt.insert("1.0", text)

# Returns all filepaths with .zip files
def get_all_file_paths(directory):
	print(f"Directory: {directory}")

	file_paths = []
	roots = []
	zip_files = []

	#crawl through directory. os.walk generates file names. 
	for root, directories, files in os.walk(directory):
		for filename in files:
			print(f"Filename: {filename}")
			if filename.endswith('.zip'):
				# Join the two strings in order to form full filepath
				roots.append(root)
				zip_files.append(filename)
				filepath = os.path.join(root, filename)
				file_paths.append(filepath)
	print(f"file_paths: {file_paths}")
	return file_paths, roots, zip_files

def main():
	# Path to folder which needs to be zipped
	home_directory = parent_txt.get("1.0", tk.END).rstrip()
	# print(f"Home Direct: {home_directory}")
	dest_directory = dest_txt.get("1.0", tk.END).rstrip()

	# Calling function to get filepaths
	file_paths, roots, zip_files = get_all_file_paths(home_directory)
	print(f"Filepaths: {file_paths}")
	text.insert(tk.END, "The files listed below have been unzipped: ")
	for filename in file_paths:
		print(file_paths) 

	for i in range(len(file_paths)):
		try:
			os.chdir(roots[i])
			with ZipFile(zip_files[i], 'r') as zip:
				text.insert(tk.END, f"\n{file_paths[i]}")
				zip.printdir()
				zip.extractall(path=dest_directory)
		except:
			raise ValueError("Can't move into that directory")

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
