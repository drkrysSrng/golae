from flask import Flask, request, redirect, render_template
import requests
from flask_cors import CORS
from datetime import datetime
from os import path, environ
import pickle
from bs4 import BeautifulSoup  # You may need to install this library using: pip install beautifulsoup4

app = Flask(__name__)

URL_FILE = environ.get('URL_FILE') or "url_variable.pkl"
USER_AGENT_FILE = environ.get('USER_AGENT_FILE') or "filename_variable.pkl"

# Function to save the URL variable or filename to a file using pickle
def save_variable(variable, filename):
    with open(filename, 'wb') as file:
        pickle.dump(variable, file)

# Function to read the URL variable or filename from the file using pickle
def read_variable(filename):
    try:
        with open(filename, 'rb') as file:
            loaded_text = pickle.load(file)
            return loaded_text
    except FileNotFoundError:
        return ''

# Function to fetch HTML content of a URL
def fetch_html_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        return response.text
    except requests.RequestException as e:
        return f"Error fetching content from {url}: {e}"

# Function to extract preview information from HTML content
def extract_preview_info(html_content):
    if html_content:
        soup = BeautifulSoup(html_content, 'html.parser')
        # Customize this part based on how you want to extract preview information
        title = soup.title.string if soup.title else 'No Title'
        return f"Preview: {title}"
    return None

@app.route('/')
def index():
    url_variable = read_variable(URL_FILE)
    filename_variable = read_variable(USER_AGENT_FILE)

    # Use X-Forwarded-For to get the real client IP when behind a proxy
    client_ip = request.headers.get('X-Forwarded-For')
    if client_ip is None:
        client_ip = request.remote_addr

    user_agent_str = request.headers.get('User-Agent')

    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if url_variable:
        # Fetch HTML content from the redirected URL
        redirected_url = url_variable
        html_content = fetch_html_content(redirected_url)
        
        # Extract preview information from HTML content
        preview_info = extract_preview_info(html_content)

        with open(filename_variable, "a") as file:
            file.write(f"Date and Time: {current_datetime}\n")
            file.write(f"Client IP: {client_ip}\n")
            file.write(f"Operating System: {user_agent_str}\n")
            file.write(f"{preview_info}\n\n")

        # Save the redirected URL to a variable for further use
        save_variable(redirected_url, URL_FILE)

        # Redirect to the original URL
        return redirect(url_variable)
        
    elif filename_variable:
        # Do something with the filename, for example, serve it as a download
        return f"File will be served: {filename_variable}"
    else:
        return redirect('/assign')

@app.route('/assign')
def assign():
    url_variable = read_variable(URL_FILE)  # Retrieve the URL variable from the file
    filename_variable = read_variable(USER_AGENT_FILE)  # Retrieve the filename variable from the file
    return render_template('set_url.html', url_variable=url_variable, filename_variable=filename_variable)


@app.route('/set_url', methods=['POST'])
def set_url():
    url_variable = request.form.get('url_variable')
    filename_variable = request.form.get('filename_variable')
    delete_checkbox = request.form.get('delete_checkbox')  # Get the checkbox value

    if url_variable:
        save_variable(url_variable, URL_FILE)
    if filename_variable:
        save_variable(filename_variable, USER_AGENT_FILE)

    # Now you can use the value of delete_checkbox in your logic
    if delete_checkbox == 'on':
        if filename_variable:
            file_path = filename_variable  # Assuming filename_variable contains the path to the file
            try:
                # Attempt to remove the file
                remove(file_path)
                return f"File '{filename_variable}' deleted successfully."
            except Exception as e:
                return f"Failed to delete file '{filename_variable}'. Error: {str(e)}"

    return redirect('/doc')



@app.route('/doc')
def display_text_file():
    filename_variable = read_variable(USER_AGENT_FILE)

    if not path.exists(filename_variable):
        file_content = "Empty file"
    else:
        with open(filename_variable, 'r') as file:
            file_content = file.read()

    return render_template('text_viewer.html', content=file_content)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7777, debug=True)
    CORS(app)
