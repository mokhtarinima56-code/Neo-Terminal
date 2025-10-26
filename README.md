# Neo Terminal

**NeoTerminal** is a Python-based file management application with a retro, Matrix-inspired terminal interface, built using PyQt5. It provides a secure, intuitive platform for managing files across four designated folders (`a`, `b`, `c`, `d`) in the `~/Documents/MyFiles` directory. Beyond basic file operations, NeoTerminal integrates web-based functionalities like image downloading and web search result storage, all within a password-protected, command-driven environment. Its unique blend of nostalgic aesthetics and modern functionality makes it a versatile tool for file management and web interaction, with significant potential for expansion.

## Table of Contents
- [Core Algorithm](#core-algorithm)
- [Key Features](#key-features)
- [Applications](#applications)
- [Future Expansion Potential](#future-expansion-potential)
- [File Structure](#file-structure)
- [Security Considerations](#security-considerations)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)
- [Contact](#contact)

## Core Algorithm

NeoTerminal’s functionality is driven by a modular and extensible algorithm, leveraging PyQt5 for the GUI, Python’s file system operations, and web scraping libraries (`requests`, `BeautifulSoup`). Below is an overview of its core algorithmic components:

1. **Command Parsing and Processing**:
   - **Input Handling**: User inputs are captured via a QLineEdit widget, parsed using string manipulation to identify command patterns (e.g., `command <arg1> <arg2>`).
   - **Command Dispatch**: A central `process_command` method uses conditional branching to map commands to specific functions (e.g., file operations, web tasks). Regular expressions or tokenization could enhance parsing in future iterations.
   - **Error Handling**: Robust exception handling ensures invalid inputs, missing files, or network failures produce user-friendly error messages logged to both the UI and a history file.

2. **File System Operations**:
   - **Directory Management**: The application initializes a storage directory (`~/Documents/MyFiles`) with four subfolders (`a`, `b`, `c`, `d`). File operations (list, upload, delete, move) use Python’s `os` and `shutil` modules.
   - **UUID-Based Naming**: Uploaded files and web downloads are renamed with UUIDs to prevent naming conflicts, ensuring uniqueness across folders.
   - **Size Calculation**: The `filer chart` command calculates folder sizes by recursively walking directories (`os.walk`) and summing file sizes, displayed as a text-based tree.

3. **Web Integration**:
   - **Image Downloading**: The `boot/` command fetches images from a website by:
     1. Sending an HTTP GET request using `requests` with a browser-like User-Agent.
     2. Parsing HTML with `BeautifulSoup` to extract `<img>` tags and resolve relative URLs with `urljoin`.
     3. Filtering for supported formats (jpg, jpeg, png, gif) and downloading up to a user-specified limit.
   - **Web Search**: The `sear/` command performs a Google search by:
     1. Constructing a URL with the encoded keyword.
     2. Scraping search results for up to 10 valid links, excluding Google’s own URLs.
     3. Saving results to a text file with a UUID-based name.
   - **Concurrency**: Web operations are synchronous but could be optimized with asynchronous requests (`asyncio`, `aiohttp`) for better performance.

4. **Security and Logging**:
   - **Password Check**: A simple password comparison (hardcoded as `mysecret`) gates access, implemented via a QInputDialog.
   - **History Logging**: All commands and outputs are appended to `history.log` in UTF-8 encoding, with a `del/code` command to clear the log.
   - **UI Feedback**: Outputs are displayed in a read-only QTextEdit widget styled to mimic a terminal, with scrolling to the latest entry.

5. **Cross-Platform Compatibility**:
   - File opening uses platform-specific commands (`os.startfile` for Windows, `open` for macOS, `xdg-open` for Linux) to ensure seamless integration with the host OS.
   - The GUI is built with PyQt5, ensuring consistent rendering across platforms.

The algorithm prioritizes modularity, with separate methods for each operation (`list_folder_files`, `add_up`, `download_images`, etc.), making it easy to extend or modify functionality.

## Key Features
- **Retro Terminal Aesthetic**: Green-on-black UI with a Courier New font, inspired by classic terminals and "The Matrix."
- **File Management**: Supports listing, uploading, opening, deleting, moving, and searching files across four folders, with a text-based size visualization.
- **Web Capabilities**: Downloads images from websites and saves web search results as text files, integrating online content with local storage.
- **Security**: Password-protected access with command history logging for traceability.
- **Cross-Platform**: Works on Windows, macOS, and Linux with platform-specific file handling.

## Applications

NeoTerminal’s design and functionality make it suitable for various use cases:

1. **Personal File Management**:
   - Ideal for users who prefer a command-line-like interface for organizing files in a structured directory.
   - Useful for managing small projects or personal archives, with folders (`a`, `b`, `c`, `d`) serving as categories (e.g., work, media, documents).

2. **Web Content Archiving**:
   - Enables users to collect images or search results from websites for offline reference, such as research, design inspiration, or data collection.
   - Suitable for educators, researchers, or hobbyists archiving web content in a structured format.

3. **Educational Tool**:
   - Serves as a learning platform for students studying file systems, GUI programming, or web scraping, combining practical Python concepts with an engaging interface.
   - The retro aesthetic can attract beginners to explore programming in a fun, accessible way.

4. **Prototyping and Testing**:
   - Developers can use NeoTerminal to prototype file management workflows or test web scraping scripts within a controlled environment.
   - The modular codebase allows easy integration into larger systems or workflows.

5. **Nostalgic Productivity**:
   - Appeals to users who enjoy retro computing aesthetics, offering a functional alternative to modern file explorers with a unique, immersive experience.

## Future Expansion Potential

NeoTerminal’s modular design and robust foundation provide numerous opportunities for enhancement:

1. **Graphical Visualizations**:
   - Replace the text-based `filer chart` with interactive charts using libraries like Matplotlib, Plotly, or Chart.js, visualizing file sizes, types, or folder hierarchies.
   - Implement a dashboard view for real-time folder statistics (e.g., file counts, storage usage).

2. **Advanced Web Integration**:
   - Use APIs (e.g., Google Custom Search, Bing API) for more reliable and compliant web searches, replacing direct scraping.
   - Support additional web download formats (e.g., WebP, PDF, videos) or allow users to specify custom formats.
   - Introduce asynchronous web requests (`aiohttp`) to improve performance for large-scale downloads or searches.

3. **Enhanced File Management**:
   - Add commands to create, rename, or delete folders dynamically, expanding beyond the fixed `a`, `b`, `c`, `d` structure.
   - Implement file compression/decompression (e.g., ZIP, TAR) for efficient storage.
   - Add file preview functionality within the app (e.g., text snippets, image thumbnails).

4. **Security Improvements**:
   - Replace hardcoded password with a secure, encrypted authentication system (e.g., using `bcrypt` or a database).
   - Introduce multi-user support with role-based permissions (e.g., admin vs. guest access).
   - Add file encryption for sensitive uploads.

5. **Cloud Integration**:
   - Sync files with cloud storage services (e.g., Google Drive, Dropbox) for backup and remote access.
   - Enable web-based command execution via a server-client model, turning NeoTerminal into a remote file manager.

6. **Extensibility and Plugins**:
   - Develop a plugin system to allow users to add custom commands or integrations (e.g., media conversion, version control).
   - Support scripting within the terminal to automate repetitive tasks (e.g., batch renaming, scheduled downloads).

7. **AI and Automation**:
   - Integrate AI-driven features, such as file categorization based on content (e.g., using NLP for text files or image recognition for photos).
   - Add predictive command suggestions based on user history, leveraging machine learning models.

8. **Cross-Platform Enhancements**:
   - Optimize for mobile platforms by adapting the GUI for touch interfaces or creating a companion mobile app.
   - Add support for network drives or external storage devices.

9. **Localization and Accessibility**:
   - Support multiple languages for commands and UI elements to reach a global audience.
   - Improve accessibility with screen reader support and customizable UI themes (e.g., high-contrast modes).

10. **Performance Optimization**:
    - Cache frequently accessed folder data to reduce file system queries.
    - Implement multi-threading for file operations to handle large directories efficiently.

## File Structure
- **Storage Directory**: `~/Documents/MyFiles` contains four subfolders (`a`, `b`, `c`, `d`) for file storage.
- **History Log**: Commands and outputs are saved in `~/Documents/MyFiles/history.log` in UTF-8 encoding.
- **File Naming**: Uploaded files and web downloads use UUID-based names (e.g., `image_12345678-1234-1234-1234-1234567890ab.png`) to ensure uniqueness.
- **Web Outputs**: Search results are stored as text files (e.g., `search_results_12345678-1234-1234-1234-1234567890ab.txt`) in the specified folder.

## Security Considerations
- **Password**: The default password (`mysecret`) is hardcoded and should be changed for production use. Consider encrypting passwords in a configuration file or database.
- **File Permissions**: Ensure the application has read/write access to `~/Documents/MyFiles`. Lack of permissions may cause errors during file operations.
- **Web Scraping**: The web integration features (`boot/`, `sear/`) rely on scraping, which may violate website terms of service. Use responsibly and consider API alternatives for production.
- **Data Privacy**: Files and search results are stored locally, but future cloud integration should implement encryption to protect user data.

## Troubleshooting
- **Permission Errors**: Verify that the application has write access to `~/Documents/MyFiles`. On Linux, use `chmod` to adjust permissions if needed.
- **Web Command Failures**:
  - Ensure an active internet connection.
  - Check that URLs are valid and accessible for image downloads.
  - For search commands, ensure keywords are properly quoted (e.g., `sear/("example")`).
- **File Not Found**: Use the `list` or `search` commands to verify file existence and folder location.
- **UI Issues**: Ensure PyQt5 is correctly installed. Reinstall dependencies if the interface fails to render.

## Contributing
Contributions are welcome to enhance NeoTerminal’s functionality! To contribute:
1. Fork the repository.
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit changes with clear messages: `git commit -m "Add your feature"`
4. Push to the branch: `git push origin feature/your-feature`
5. Open a pull request with a detailed description of your changes.
- Adhere to PEP 8 for code style and include comments for clarity.
- Test changes thoroughly to ensure compatibility across platforms.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments
- **PyQt5**: For the cross-platform GUI framework [](https://www.riverbankcomputing.com/software/pyqt/).
- **BeautifulSoup**: For robust web scraping [](https://www.crummy.com/software/BeautifulSoup/).
- **Inspiration**: The retro aesthetic of "The Matrix" and classic terminal interfaces.

## Contact
For questions, suggestions, or issues:
- Open an issue on GitHub.
- Contact the maintainer at [mokhtarinima56@gmail.com
](mailto:mokhtarinima56@gmail.com
).

---
*Last updated: October 27, 2025*
