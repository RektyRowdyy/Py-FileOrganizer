# IMPORTING LIBRARIES
from os import scandir, rename
from os.path import splitext, exists, join
from shutil import move
from time import sleep
import pdb

#FOR LOGGING
import logging

#A SHELL TOOL TO RUN COMMANDS IN RESPONSE TO DIRECTORY CHANGES
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# FOLDERS TO TRACK
source_dir = "C:/Users/Administrator/Downloads"
dest_dir_audio = "C:/Users/Administrator/Downloads/Audio"
dest_dir_music = "C:/Users/Administrator/Downloads/Music"
dest_dir_video = "C:/Users/Administrator/Downloads/Videos"
dest_dir_image = "C:/Users/Administrator/Downloads/Images"
dest_dir_documents = "C:/Users/Administrator/Downloads/Documents"
dest_dir_other = "C:/Users/Administrator/Downloads/Others"

# ? supported Image types
image_extensions = [".jpg", ".jpeg", ".jpe", ".jif", ".jfif", ".jfi", ".png", ".gif", ".webp", "mpeg"]

# ? supported Video types
video_extensions = [".webm", ".mp4", ".mp4v", ".avi", ".wmv", ".mov", ".qt", ".flv"]

# ? supported Audio types
audio_extensions = [".m4a""mp3", ".wav",".aac"]

# ? supported Document types
document_extensions = [".doc", ".docx",".pdf", ".xls", ".xlsx", ".ppt", ".pptx"]

# ? Other extensions
other_extensions = [".zip",".psd"] 


#IF FILE IF SAME NAME ALREADY EXISTS
def make_unique(dest, name):
    filename, extension = splitext(name)
    counter = 1
    # * IF FILE EXISTS, ADDS NUMBER TO THE END OF THE FILENAME
    while exists(f"{dest}/{name}"):
        name = f"{filename}({str(counter)}){extension}"
        counter += 1

    return name

# SAVE FILE TO DESTINATION
def move_file(dest, entry, name):
    if exists(f"{dest}/{name}"):
        unique_name = make_unique(dest, name)
        oldName = join(dest, name)
        newName = join(dest, unique_name)
        rename(oldName, newName)
    move(entry, dest)

# ? THIS FUNCTION WILL RUN WHENEVER THERE IS A CHANGE IN "source_dir"
class MoverHandler(FileSystemEventHandler):
    def on_modified(self, event):
        with scandir(source_dir) as entries:
            for entry in entries:
                name = entry.name
                self.check_audio_files(entry, name)
                self.check_video_files(entry, name)
                self.check_image_files(entry, name)
                self.check_document_files(entry, name)
                self.check_other_files(entry,name)
                

                

    def check_audio_files(self, entry, name):  # * Checks all Audio Files
        for audio_extension in audio_extensions:
            if name.endswith(audio_extension) or name.endswith(audio_extension.upper()):
                dest = dest_dir_music
                move_file(dest, entry, name)
                logging.info(f"Moved audio file: {name}")

    def check_video_files(self, entry, name):  # * Checks all Video Files
        for video_extension in video_extensions:
            if name.endswith(video_extension) or name.endswith(video_extension.upper()):
                move_file(dest_dir_video, entry, name)
                logging.info(f"Moved video file: {name}")

    def check_image_files(self, entry, name):  # * Checks all Image Files
        for image_extension in image_extensions:
            if name.endswith(image_extension) or name.endswith(image_extension.upper()):
                move_file(dest_dir_image, entry, name)
                logging.info(f"Moved image file: {name}")

    def check_document_files(self, entry, name):  # * Checks all Document Files
        for documents_extension in document_extensions:
            if name.endswith(documents_extension) or name.endswith(documents_extension.upper()):
                move_file(dest_dir_documents, entry, name)
                logging.info(f"Moved document file: {name}")
            
    def check_other_files(self, entry, name): # *Checks all Other Files
        for other_extension in other_extensions:
            if name.endswith(other_extension) or name.endswith(other_extension.upper()):
                move_file(dest_dir_other,entry,name)
                logging.info(f"Moved other file: {name}")
        

# ! NO NEED TO CHANGE BELOW CODE
# ! STARTER CODE FOR WATCHDOG LIBRARY
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = source_dir
    event_handler = MoverHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            sleep(10)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()