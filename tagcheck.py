import os
import logging
from html.parser import HTMLParser

# Set up logging configuration
logging.basicConfig(
    filename='tagcheck.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class MyHTMLParser(HTMLParser):
    def __init__(self, tags_to_scan):
        super().__init__()
        self.current_line = 1
        self.tag_stack = []
        self.div_number = 1
        self.divisions = {}  # Store start line and division number
        self.output_lines = []
        self.tags_to_scan = tags_to_scan  # Tags that user chooses to scan

    def handle_starttag(self, tag, attrs):
        if tag in ['meta', 'link', 'br', 'hr', 'input', 'img', 'base', 'a', 'i'] and tag in self.tags_to_scan:
            self.handle_single_line_tag(tag)
        elif tag in self.tags_to_scan:
            if tag == 'div':
                self.output_lines.append(f"{self.current_line}: Start Line : <{tag} (Div #{self.div_number})")
                self.divisions[self.current_line] = self.div_number
                self.div_number += 1
                logging.info(f"{self.current_line}: Start Line : <{tag} (Div #{self.div_number - 1})")
            else:
                self.output_lines.append(f"{self.current_line}: Start Line : <{tag}>")
                logging.info(f"{self.current_line}: Start Line : <{tag}>")
            self.tag_stack.append((tag, self.current_line))

    def handle_endtag(self, tag):
        if tag in self.tags_to_scan and tag not in ['meta', 'link', 'br', 'hr', 'input', 'img', 'base', 'a', 'i']:
            if self.tag_stack:
                # Look for matching start tag
                for i in range(len(self.tag_stack) - 1, -1, -1):
                    start_tag, start_line = self.tag_stack[i]
                    if start_tag == tag:
                        del self.tag_stack[i]
                        if start_line == self.current_line:
                            self.output_lines.append(f"{self.current_line}: Single Line : </{tag}>")
                            logging.info(f"{self.current_line}: Single Line : </{tag}>")
                        else:
                            div_num = self.divisions.get(start_line, '')
                            self.output_lines.append(f"{self.current_line}: End Line : </{tag}> (Div #{div_num})" if div_num else f"{self.current_line}: End Line : </{tag}>")
                            logging.info(f"{self.current_line}: End Line : </{tag}> (Div #{div_num})" if div_num else f"{self.current_line}: End Line : </{tag}>")
                        break
                else:
                    self.output_lines.append(f"{self.current_line}: Unexpected end tag: </{tag}>")
                    logging.warning(f"{self.current_line}: Unexpected end tag: </{tag}>")
            else:
                self.output_lines.append(f"{self.current_line}: Unexpected end tag: </{tag}>")
                logging.warning(f"{self.current_line}: Unexpected end tag: </{tag}>")

    def handle_startendtag(self, tag, attrs):
        if tag in self.tags_to_scan:
            self.handle_single_line_tag(tag)

    def handle_single_line_tag(self, tag):
        self.output_lines.append(f"{self.current_line}: Single Line : <{tag}/>")

    def feed_html(self, html_content):
        # Split by newlines to simulate line-by-line parsing
        lines = html_content.split('\n')
        for line in lines:
            self.feed(line)
            self.current_line += 1  # Increment the line number after processing each line

    def display_output(self):
        # Ask the user how many lines they want to see per page
        while True:
            try:
                lines_per_page = int(input("Enter the number of lines per page: "))
                if lines_per_page <= 0:
                    print("Please enter a positive integer.")
                    continue
                break
            except ValueError:
                print("Invalid input. Please enter a valid number.")

        # Initialize pagination state
        total_lines = len(self.output_lines)
        current_page = 0
        total_pages = (total_lines + lines_per_page - 1) // lines_per_page  # Calculate total pages

        while True:
            # Determine the range of lines to display for the current page
            start_idx = current_page * lines_per_page
            end_idx = min(start_idx + lines_per_page, total_lines)
            page_lines = self.output_lines[start_idx:end_idx]

            # Print the lines for the current page
            print(f"\n--- Page {current_page + 1}/{total_pages} ---")
            for line in page_lines:
                print(line)

            # Provide navigation options to the user
            if current_page == 0 and current_page + 1 == total_pages:
                # If there's only one page
                break
            elif current_page == 0:
                navigation = input("\nPress 'n' for next page or 'q' to quit: ").strip().lower()
            elif current_page + 1 == total_pages:
                navigation = input("\nPress 'p' for previous page or 'q' to quit: ").strip().lower()
            else:
                navigation = input("\nPress 'n' for next page, 'p' for previous page, or 'q' to quit: ").strip().lower()

            if navigation == 'n' and current_page + 1 < total_pages:
                current_page += 1
            elif navigation == 'p' and current_page > 0:
                current_page -= 1
            elif navigation == 'q':
                break
            else:
                print("Invalid input. Please try again.")

def choose_tags():
    # Allow the user to select which tags to scan
    all_tags = [
        'html', 'head', 'title', 'meta', 'link', 'body', 'div', 'span', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
        'p', 'a', 'img', 'ul', 'ol', 'li', 'table', 'tr', 'td', 'th', 'br', 'hr', 'input', 'form', 'button', 'i', 'b', 'u'
    ]
    while True:
        print("----------------------")
        print("Choose which tags to scan (separate by comma or enter 'all' for all tags):")
        print("Type 'q' or 'quit' to exit.")
        print(f"Available tags: {', '.join(all_tags)}")
        print("----------------------")
        user_input = input("Enter your choice: ").strip().lower()
        print("----------------------")

        if user_input in ['q', 'quit']:
            print("Exiting the program.")
            print("----------------------")
            exit()  # Exit the program if the user chooses to quit

        if user_input == 'all':
            return all_tags  # If user selects 'all', scan all tags
        else:
            selected_tags = [tag.strip() for tag in user_input.split(',')]
            # Validate user input to ensure only valid tags are included
            invalid_tags = [tag for tag in selected_tags if tag not in all_tags]

            if invalid_tags:
                print(f"Invalid tags: {', '.join(invalid_tags)}. Please try again.")
                logging.warning(f"Invalid tags entered: {', '.join(invalid_tags)}")
            else:
                return selected_tags

def choose_file(directory):
    # List all files in the specified directory
    try:
        files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
        if not files:
            print("No files found in the directory.")
            logging.warning(f"No files found in the directory: {directory}")
            return None
        
        print("----------------------")
        print("Choose a file from the list below:")
        for idx, file in enumerate(files):
            print(f"{idx + 1}. {file}")
        print("----------------------")

        while True:
            try:
                choice = int(input("Enter the number of the file you want to select: "))
                if 1 <= choice <= len(files):
                    return os.path.join(directory, files[choice - 1])
                else:
                    print("Invalid choice. Please enter a number corresponding to a file.")
            except ValueError:
                print("Invalid input. Please enter a number.")
    except Exception as e:
        print(f"An error occurred while accessing the directory: {e}")
        logging.error(f"An error occurred while accessing the directory: {e}")
        return None

def main():
    while True:
        tags_to_scan = choose_tags()
        logging.info(f"Tags to scan: {', '.join(tags_to_scan)}")

        # Ask the user for the directory containing HTML files
        directory = input("Enter the directory path containing HTML files: ").strip()
        print("----------------------")

        # Choose a file from the specified directory
        html_path = choose_file(directory)
        if not html_path:
            continue

        # Initialize the parser with the user-specified tags
        parser = MyHTMLParser(tags_to_scan)

        try:
            with open(html_path, 'r', encoding='utf-8') as file:
                html_content = file.read()
                parser.feed_html(html_content)
                parser.display_output()
            logging.info(f"Processed file: {html_path}")
            break  # Exit loop if file is found and processed
        except FileNotFoundError:
            print(f"File not found: {html_path}. Please try again.")
            logging.error(f"File not found: {html_path}")
        except Exception as e:
            print(f"An error occurred: {e}")
            logging.error(f"An error occurred: {e}")
            break  # Exit if an unknown error occurs

if __name__ == "__main__":
    main()























