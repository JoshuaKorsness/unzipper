from zipfile import ZipFile
import tkinter as tk
from tkinter import filedialog
import os

# Opens explore to navigate to directory
def search_for_file_path():
    currdir = os.getcwd()
    tempdir = filedialog.askdirectory(parent=window, initialdir=currdir, title='Please select a directory')
    if len(tempdir) > 0:
        print ("You chose: %s" % tempdir)
    return tempdir

# Returns all filepaths with .zip files
def get_all_file_paths(directory):

	file_paths = []
	roots = []
	zip_files = []

	#crawl through directory. os.walk generates file names. 
	for root, directories, files in os.walk(directory):
		for filename in files:
			if filename.endswith('.zip'):
				# Join the two strings in order to form full filepath
				roots.append(root)
				zip_files.append(filename)
				filepath = os.path.join(root, filename)
				file_paths.append(filepath)
	return file_paths, roots, zip_files

def main():
	# Path to folder which needs to be zipped
	home_directory = search_for_file_path()

	# Calling function to get filepaths
	file_paths, roots, zip_files = get_all_file_paths(home_directory)
	text.insert(tk.END, "The files listed below have been unzipped: ")
	for filename in file_paths:
		print(file_paths) 

	for i in range(len(file_paths)):
		try:
			os.chdir(roots[i])
			with ZipFile(zip_files[i], 'r') as zip:
				text.insert(tk.END, f"\n{file_paths[i]}")
				zip.printdir()
				zip.extractall(path=home_directory)
		except:
			raise ValueError("Can't move into that directory")

# Build GUI ------------------------------------------------------------

window = tk.Tk()
frame_a = tk.Frame()	# Heading
frame_b = tk.Frame()	# Button

header = tk.Label(
	master=frame_a,
	text="Unzipper Program"
	)
header.pack()
frame_a.pack()

inst = tk.Label(
	master=frame_b,
	text='Click the button to navigate to a directory. All .zip files in children folders will be unzipped'
	)
inst.pack()
button = tk.Button(
	text='Navigate to Directory',
	command = main
	)
button.pack()
text = tk.Text(
	master=frame_b
	)
text.pack()
frame_b.pack()

window.mainloop()
