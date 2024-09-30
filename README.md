# -HTML-Tag-Scanner
This program allows users to scan and parse HTML files for specific HTML tags.

Provides a line-by-line analysis of the specified tags, logging the occurrence of start tags, end tags, and self-closing tags. Users can select which tags to scan and navigate through the parsed results in a paginated view.

Features:
Custom Tag Selection: Users can select specific HTML tags to scan or choose to scan all available tags.
Directory and File Selection: The program lists available files in a specified directory, allowing users to select the HTML file they want to process.
Line-by-Line Parsing: The program parses HTML content line by line, tracking and displaying the start, end, and self-closing tags, as well as the associated line numbers.
Pagination: Users can view parsed results in a paginated format and control how many lines they want to display per page.
Logging: All key actions, errors, and tag occurrences are logged in a file named tagcheck.log.
Error Handling: The program handles invalid user inputs, file-not-found errors, and unexpected conditions gracefully.

Installation:

Clone the repository or download the program files.

Install the dependencies: The program only requires Python's built-in libraries, so no additional package installation is needed. Ensure you are using Python 3.6 or above.

Optionally, you can install tqdm if you want to add a progress bar:
pip install tqdm

How to Use:

Run the Program: Execute the program in your terminal:
python html_tag_scanner.py

Choose Tags:

You'll be prompted to enter a list of tags you wish to scan (e.g., div, p, a).
Alternatively, you can type all to scan all available tags.
To exit the program, type q or quit.

Select a Directory:

Enter the directory containing the HTML file you want to process.
The program will list all files in the directory.

Choose a File:

Select the HTML file you wish to scan by entering the corresponding number from the list.
View Parsed Results:

The program will parse the file line by line and display the occurrence of the selected tags.
You will be asked how many lines you'd like to see per page.
Navigate Through Results:

Press n to view the next page.
Press p to view the previous page.
Press q to quit.

------------------------------------------------------------------------------------------------
Example Workflow:

Choose which tags to scan (separate by comma or enter 'all' for all tags):
Available tags: html, head, title, meta, link, body, div, span, h1, h2, h3, h4, h5, h6, p, a, img, ul, ol, li, table, tr, td, th, br, hr, input, form, button, i, b, u
Enter your choice: div, p, a

Enter the directory to scan HTML files: /path/to/html/files

Choose a file from the list below:
1. index.html
2. about.html
3. contact.html
Enter the number of the file you want to select: 1

Enter the number of lines per page: 10

--- Page 1/3 ---
1: Start Line : <div (Div #1)
3: Start Line : <p>
4: End Line : </p>
7: Start Line : <a>
8: End Line : </a>
...

Press 'n' for next page or 'q' to quit: n

--- Page 2/3 ---
12: Start Line : <div (Div #2)
14: Start Line : <p>
15: End Line : </p>
...

------------------------------------------------------------------------------------------------

Logging:

All tag occurrences and system messages are logged in a file named tagcheck.log, located in the same directory where you run the program. This file contains information such as:

Which tags were scanned
The occurrence of start, end, and self-closing tags with corresponding line numbers
Any warnings, such as unexpected end tags or invalid input

Error Handling:

If an invalid tag is selected, the program will notify the user and prompt them to try again.
If no files are found in the specified directory, a warning will be displayed.
If the selected file does not exist, the program will return a file-not-found error, and the user can try again.

Customization:

Tags to Scan: You can modify the default list of tags by editing the all_tags list inside the choose_tags function.
Logging Level: The logging level is set to DEBUG by default. To modify the logging level (e.g., to INFO or WARNING), change the level parameter in the logging.basicConfig() call.
