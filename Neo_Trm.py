import sys
import os
import uuid
import subprocess
import platform
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, quote
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QLineEdit, QVBoxLayout, QWidget, QInputDialog, \
    QMessageBox, QFileDialog
from PyQt5.QtGui import QFont, QColor, QTextCursor, QPalette
from PyQt5.QtCore import Qt
import shutil


class TerminalFileApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("File Storage Terminal")
        self.setGeometry(100, 100, 800, 600)

        # Password check
        self.password = "mysecret"  # Change this to your desired password
        if not self.check_password():
            sys.exit()

        # Storage directory
        self.storage_dir = os.path.expanduser("~/Documents/MyFiles")
        if not os.path.exists(self.storage_dir):
            os.makedirs(self.storage_dir)

        # Create a, b, c, d folders if they don't exist
        self.folders = ['a', 'b', 'c', 'd']
        for folder in self.folders:
            folder_path = os.path.join(self.storage_dir, folder)
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)

        # History file
        self.history_file = os.path.join(self.storage_dir, "history.log")

        # Setup UI to look like a terminal
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()

        # Output area (read-only)
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        self.output.setFont(QFont("Courier New", 12))  # DOS-like font
        self.output.setStyleSheet("background-color: #000000; color: #00FF00; border: none;")
        palette = self.output.palette()
        palette.setColor(QPalette.Text, QColor("#00FF00"))
        palette.setColor(QPalette.Base, QColor("#000000"))
        self.output.setPalette(palette)
        self.layout.addWidget(self.output)

        # Input line
        self.input_line = QLineEdit()
        self.input_line.setFont(QFont("Courier New", 12))  # DOS-like font
        self.input_line.setStyleSheet(
            "background-color: #000000; color: #00FF00; border: 1px solid #555555; padding: 5px;")
        self.input_line.returnPressed.connect(self.process_command)
        self.input_line.setFocusPolicy(Qt.StrongFocus)
        self.layout.addWidget(self.input_line)

        self.central_widget.setLayout(self.layout)

        # Load history
        self.load_history()

        # New welcome message
        self.print_to_output("""
Hello Neo!!! we can take code
============================================================
Available commands:
  - sweet fold <folder> in fold <folder> : List files in a folder
  - add up in fold <folder> : Upload a file to a folder
  - add down <filename> in fold <folder> : Open a file
  - del <filename> in fold <folder> : Delete a file
  - move <filename> to <new_folder> in fold <current_folder> : Move a file
  - del/all/in time : Delete all files in all folders
  - del/fold <folder> in time : Delete all files in a folder
  - filer chart : Show file size chart
  - list : List all files in all folders
  - search <filename> : Search for a file
  - boot/<link> in fold <folder> [max <number>] : Download images from a website
  - sear/("keyword") in fold <folder> : Search web and save links
  - del/code : Clear command history
  - exit : Close the terminal
============================================================
Type a command below and hit Enter to begin!
""")
        self.input_line.setFocus()  # Force focus on input
        self.activateWindow()  # Ensure window is active

    def check_password(self):
        password, ok = QInputDialog.getText(self, "Password", "Enter password:", echo=0)  # Password masking
        if ok and password == self.password:
            return True
        else:
            QMessageBox.warning(self, "Error", "Incorrect password!")
            return False

    def print_to_output(self, text):
        try:
            self.output.append(text)
            self.output.moveCursor(QTextCursor.End)
            # Save to history file
            with open(self.history_file, "a", encoding="utf-8") as f:
                f.write(text + "\n")
        except Exception as e:
            self.output.append(f"Error saving to history: {str(e)}")

    def load_history(self):
        try:
            if os.path.exists(self.history_file):
                with open(self.history_file, "r", encoding="utf-8") as f:
                    history = f.read()
                    self.output.append(history.strip())
                    self.output.moveCursor(QTextCursor.End)
        except Exception as e:
            self.output.append(f"Error loading history: {str(e)}")

    def clear_history(self):
        reply = QMessageBox.question(self, "Confirm Clear History",
                                     "Are you sure you want to clear the command history?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            try:
                # Clear the history file
                with open(self.history_file, "w", encoding="utf-8") as f:
                    f.write("")  # Empty the file
                # Clear the output display
                self.output.clear()
                # Reprint welcome message
                self.print_to_output("""
Hello Neo!!! we can take code
============================================================
Available commands:
  - sweet fold <folder> in fold <folder> : List files in a folder
  - add up in fold <folder> : Upload a file to a folder
  - add down <filename> in fold <folder> : Open a file
  - del <filename> in fold <folder> : Delete a file
  - move <filename> to <new_folder> in fold <current_folder> : Move a file
  - del/all/in time : Delete all files in all folders
  - del/fold <folder> in time : Delete all files in a folder
  - filer chart : Show file size chart
  - list : List all files in all folders
  - search <filename> : Search for a file
  - boot/<link> in fold <folder> [max <number>] : Download images from a website
  - sear/("keyword") in fold <folder> : Search web and save links
  - del/code : Clear command history
  - exit : Close the terminal
============================================================
Type a command below and hit Enter to begin!
""")
                self.print_to_output("Command history cleared successfully.")
            except PermissionError:
                self.print_to_output("Error: Permission denied while trying to clear history file. Check file permissions.")
            except Exception as e:
                self.print_to_output(f"Error clearing history: {str(e)}")
        else:
            self.print_to_output("Clear history canceled.")

    def search_web(self, keyword, folder):
        if folder not in self.folders:
            self.print_to_output(f"Error: Folder must be one of: {', '.join(self.folders)}")
            return
        folder_path = os.path.join(self.storage_dir, folder)
        self.print_to_output(f"Searching for \"{keyword}\" and saving links to a text file in '{folder}'...")
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            # Use Google search with the keyword
            search_url = f"https://www.google.com/search?q={quote(keyword)}"
            response = requests.get(search_url, headers=headers, timeout=10)
            if response.status_code != 200:
                self.print_to_output(f"Error: Failed to perform search (Status code: {response.status_code})")
                return

            soup = BeautifulSoup(response.text, 'html.parser')
            links = []
            # Find all links in search results (limit to 10)
            for a_tag in soup.find_all('a', href=True)[:10]:
                href = a_tag['href']
                if href.startswith('/url?q='):
                    # Extract the actual URL from Google's redirect
                    link = href.replace('/url?q=', '').split('&')[0]
                    if link.startswith('http') and 'google.com' not in link:
                        links.append(link)

            if not links:
                self.print_to_output("No relevant links found for the keyword.")
                return

            # Save links to a text file
            filename = f"search_results_{uuid.uuid4()}.txt"
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(f"Search results for keyword: \"{keyword}\"\n\n")
                for i, link in enumerate(links, 1):
                    f.write(f"{i}. {link}\n")
            self.print_to_output(f"Saved {len(links)} links to '{filename}' in '{folder}'")
        except Exception as e:
            self.print_to_output(f"Error during web search: {str(e)}")

    def download_images(self, url, folder, max_images=5):
        if folder not in self.folders:
            self.print_to_output(f"Error: Folder must be one of: {', '.join(self.folders)}")
            return
        folder_path = os.path.join(self.storage_dir, folder)
        self.print_to_output(f"Downloading up to {max_images} images from {url} to '{folder}' in the background...")
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code != 200:
                self.print_to_output(f"Error: Failed to access {url} (Status code: {response.status_code})")
                return

            soup = BeautifulSoup(response.text, 'html.parser')
            img_tags = soup.find_all('img')
            img_urls = []
            for img in img_tags:
                src = img.get('src') or img.get('data-src') or img.get('data-srcset') or img.get('data-fallback-src')
                if src:
                    # Convert relative URLs to absolute
                    full_url = urljoin(url, src)
                    if full_url.endswith(('.jpg', '.jpeg', '.png', '.gif')):
                        img_urls.append(full_url)

            if not img_urls:
                self.print_to_output("No supported images (jpg, jpeg, png, gif) found on the website.")
                return

            count = 0
            for i, img_url in enumerate(img_urls[:max_images], 1):
                try:
                    img_response = requests.get(img_url, headers=headers, stream=True, timeout=10)
                    if img_response.status_code == 200:
                        filename = f"image_{uuid.uuid4()}{os.path.splitext(img_url)[1]}"
                        file_path = os.path.join(folder_path, filename)
                        with open(file_path, 'wb') as f:
                            for chunk in img_response.iter_content(chunk_size=8192):
                                f.write(chunk)
                        self.print_to_output(f"Downloaded '{filename}' to '{folder}'")
                        count += 1
                    else:
                        self.print_to_output(f"Failed to download {img_url} (Status code: {img_response.status_code})")
                except Exception as e:
                    self.print_to_output(f"Error downloading {img_url}: {str(e)}")
            self.print_to_output(f"Completed: {count} images downloaded to '{folder}' without opening the website.")
        except Exception as e:
            self.print_to_output(f"Error accessing {url}: {str(e)}")

    def process_command(self):
        try:
            command = self.input_line.text().strip()
            if command:
                self.print_to_output(f"> {command}")
                self.input_line.clear()
                self.input_line.setFocus()  # Ensure focus returns to input

                if command.startswith("sweet fold "):
                    parts = command.split(" in fold ")
                    if len(parts) == 2:
                        folder = parts[1].strip()
                        self.list_folder_files(folder)
                    else:
                        self.print_to_output("Error: Usage: sweet fold <folder> in fold <folder>")
                elif command.startswith("add up in fold "):
                    folder = command.split(" in fold ")[1].strip()
                    self.add_up(folder)
                elif command.startswith("add down "):
                    parts = command.split(" in fold ")
                    if len(parts) == 2:
                        filename, folder = parts[0].split(" ", 2)[2].strip(), parts[1].strip()
                        self.add_down(filename, folder)
                    else:
                        self.print_to_output("Error: Usage: add down <filename> in fold <folder>")
                elif command.startswith("del "):
                    if command.startswith("del/fold "):
                        parts = command.split(" in time")
                        if len(parts) == 2:
                            folder = parts[0].split(" ", 1)[1].strip()
                            self.delete_folder_files(folder)
                        else:
                            self.print_to_output("Error: Usage: del/fold <folder> in time")
                    elif command == "del/all/in time":
                        self.delete_all_files()
                    elif command == "del/code":
                        self.clear_history()
                    else:
                        parts = command.split(" in fold ")
                        if len(parts) == 2:
                            filename, folder = parts[0].split(" ", 1)[1].strip(), parts[1].strip()
                            self.del_file(filename, folder)
                        else:
                            self.print_to_output("Error: Usage: del <filename> in fold <folder>")
                elif command.startswith("move "):
                    parts = command.split(" in fold ")
                    if len(parts) == 2:
                        move_parts = parts[0].split(" to ")
                        if len(move_parts) == 2:
                            filename, new_folder = move_parts[0].split(" ", 1)[1].strip(), move_parts[1].strip()
                            current_folder = parts[1].strip()
                            self.move_file(filename, current_folder, new_folder)
                        else:
                            self.print_to_output(
                                "Error: Usage: move <filename> to <new_folder> in fold <current_folder>")
                    else:
                        self.print_to_output("Error: Usage: move <filename> to <new_folder> in fold <current_folder>")
                elif command == "filer chart":
                    self.show_file_chart()
                elif command == "list":
                    self.list_files()
                elif command.startswith("search "):
                    filename = command.split(" ", 1)[1].strip()
                    self.search_file(filename)
                elif command.startswith("boot/") and " in fold " in command:
                    parts = command.split(" in fold ")
                    if len(parts) == 2:
                        boot_parts = parts[1].split(" max ")
                        folder = boot_parts[0].strip()
                        max_images = 5  # Default max images
                        if len(boot_parts) == 2:
                            try:
                                max_images = int(boot_parts[1].strip())
                                if max_images <= 0:
                                    self.print_to_output("Error: max <number> must be a positive integer")
                                    return
                            except ValueError:
                                self.print_to_output("Error: max <number> must be a valid integer")
                                return
                        url = parts[0].replace("boot/", "").strip()
                        if not url.startswith(('http://', 'https://')):
                            url = 'https://' + url
                        self.download_images(url, folder, max_images)
                    else:
                        self.print_to_output("Error: Usage: boot/<link> in fold <folder> [max <number>]")
                elif command.startswith("sear/(\"") and " in fold " in command:
                    parts = command.split(" in fold ")
                    if len(parts) == 2:
                        folder = parts[1].strip()
                        # Extract keyword between quotes
                        keyword_part = parts[0].replace("sear/(\"", "").strip()
                        if keyword_part.endswith("\")"):
                            keyword = keyword_part[:-2]
                            self.search_web(keyword, folder)
                        else:
                            self.print_to_output("Error: Keyword must be enclosed in quotes, e.g., sear/(\"keyword\")")
                    else:
                        self.print_to_output("Error: Usage: sear/(\"keyword\") in fold <folder>")
                elif command == "exit":
                    sys.exit()
                else:
                    self.print_to_output(
                        "Error: Unknown command. Try: sweet fold <folder> in fold <folder>, add up in fold <folder>, "
                        "add down <filename> in fold <folder>, del <filename> in fold <folder>, "
                        "move <filename> to <new_folder> in fold <current_folder>, del/all/in time, "
                        "del/fold <folder> in time, filer chart, list, search <filename>, boot/<link> in fold <folder> [max <number>], "
                        "sear/(\"keyword\") in fold <folder>, del/code, exit")
        except Exception as e:
            self.print_to_output(f"Error: {str(e)}")

    def list_folder_files(self, folder):
        if folder not in self.folders:
            self.print_to_output(f"Error: Folder must be one of: {', '.join(self.folders)}")
            return
        folder_path = os.path.join(self.storage_dir, folder)
        files = os.listdir(folder_path)
        if files:
            self.print_to_output(f"Files in {folder}:")
            for file in files:
                self.print_to_output(f"  {file}")
        else:
            self.print_to_output(f"No files in {folder}.")

    def add_up(self, folder):
        if folder not in self.folders:
            self.print_to_output(f"Error: Folder must be one of: {', '.join(self.folders)}")
            return
        file_path, _ = QFileDialog.getOpenFileName(self, "Select File")
        if file_path:
            original_ext = os.path.splitext(file_path)[1]
            random_name = str(uuid.uuid4()) + original_ext
            dest_path = os.path.join(self.storage_dir, folder, random_name)
            shutil.copy(file_path, dest_path)
            self.print_to_output(f"Uploaded file as '{random_name}' to '{folder}'")

    def add_down(self, filename, folder):
        if folder not in self.folders:
            self.print_to_output(f"Error: Folder must be one of: {', '.join(self.folders)}")
            return
        file_path = os.path.join(self.storage_dir, folder, filename)
        if os.path.exists(file_path):
            try:
                if platform.system() == "Windows":
                    os.startfile(file_path)
                elif platform.system() == "Darwin":  # macOS
                    subprocess.run(["open", file_path], check=True)
                else:  # Linux and others
                    subprocess.run(["xdg-open", file_path], check=True)
                self.print_to_output(f"Opening '{filename}' from '{folder}'")
            except Exception as e:
                self.print_to_output(f"Error opening file: {str(e)}")
        else:
            self.print_to_output(f"Error: '{filename}' not found in '{folder}'")

    def del_file(self, filename, folder):
        if folder not in self.folders:
            self.print_to_output(f"Error: Folder must be one of: {', '.join(self.folders)}")
            return
        file_path = os.path.join(self.storage_dir, folder, filename)
        if os.path.exists(file_path):
            os.remove(file_path)
            self.print_to_output(f"Deleted '{filename}' from '{folder}'")
        else:
            self.print_to_output(f"Error: '{filename}' not found in '{folder}'")

    def delete_all_files(self):
        reply = QMessageBox.question(self, "Confirm Delete",
                                     "Are you sure you want to delete all files in all folders?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            for folder in self.folders:
                folder_path = os.path.join(self.storage_dir, folder)
                for file in os.listdir(folder_path):
                    file_path = os.path.join(folder_path, file)
                    if os.path.isfile(file_path):
                        os.remove(file_path)
            self.print_to_output("All files deleted from all folders.")
        else:
            self.print_to_output("Delete all files canceled.")

    def delete_folder_files(self, folder):
        if folder not in self.folders:
            self.print_to_output(f"Error: Folder must be one of: {', '.join(self.folders)}")
            return
        reply = QMessageBox.question(self, "Confirm Delete",
                                     f"Are you sure you want to delete all files in folder '{folder}'?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            folder_path = os.path.join(self.storage_dir, folder)
            for file in os.listdir(folder_path):
                file_path = os.path.join(folder_path, file)
                if os.path.isfile(file_path):
                    os.remove(file_path)
            self.print_to_output(f"All files deleted from folder '{folder}'.")
        else:
            self.print_to_output(f"Delete files in folder '{folder}' canceled.")

    def move_file(self, filename, current_folder, new_folder):
        if current_folder not in self.folders or new_folder not in self.folders:
            self.print_to_output(f"Error: Folders must be one of: {', '.join(self.folders)}")
            return
        current_path = os.path.join(self.storage_dir, current_folder, filename)
        new_path = os.path.join(self.storage_dir, new_folder, filename)
        if os.path.exists(current_path):
            if os.path.exists(new_path):
                self.print_to_output(f"Error: '{filename}' already exists in '{new_folder}'")
                return
            shutil.move(current_path, new_path)
            self.print_to_output(f"Moved '{filename}' from '{current_folder}' to '{new_folder}'")
        else:
            self.print_to_output(f"Error: '{filename}' not found in '{current_folder}'")

    def list_files(self):
        files_found = False
        for folder in self.folders:
            folder_path = os.path.join(self.storage_dir, folder)
            files = os.listdir(folder_path)
            if files:
                files_found = True
                self.print_to_output(f"Files in {folder}:")
                for file in files:
                    size = os.path.getsize(os.path.join(folder_path, file)) / 1024  # KB
                    self.print_to_output(f"  {file} ({size:.2f} KB)")
        if not files_found:
            self.print_to_output("No files found in any folder.")

    def search_file(self, filename):
        found = False
        for folder in self.folders:
            folder_path = os.path.join(self.storage_dir, folder)
            if filename in os.listdir(folder_path):
                found = True
                self.print_to_output(f"Found '{filename}' in folder '{folder}'")
        if not found:
            self.print_to_output(f"Error: '{filename}' not found in any folder.")

    def show_file_chart(self):
        total_size = 0
        folder_sizes = {f: 0 for f in self.folders}

        for folder in self.folders:
            folder_path = os.path.join(self.storage_dir, folder)
            for root, _, files in os.walk(folder_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    size = os.path.getsize(file_path) / 1024  # KB
                    folder_sizes[folder] += size
                    total_size += size

        chart = f"""File Tree:
mother ({total_size:.2f} KB)
├── a ({folder_sizes['a']:.2f} KB)
├── b ({folder_sizes['b']:.2f} KB)
├── c ({folder_sizes['c']:.2f} KB)
└── d ({folder_sizes['d']:.2f} KB)
"""
        self.print_to_output(chart)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TerminalFileApp()
    window.show()
    sys.exit(app.exec_())