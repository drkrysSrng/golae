from flask import Flask, request, redirect, render_template
from user_agents import parse
from datetime import datetime
from os import path

app = Flask(__name__)

# Function to save the URL variable to a file
def save_url_variable(url_variable):
    with open('url_variable.txt', 'w') as file:
        file.write(url_variable)

# Function to read the URL variable from the file
def read_url_variable():
    try:
        with open('url_variable.txt', 'r') as file:
            return file.read().strip()
    except FileNotFoundError:
        return ''

@app.route('/')
def index():
    url_variable = read_url_variable()

    client_ip = request.remote_addr
    user_agent_str = request.headers.get('User-Agent')

    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open("user_agent.txt", "a") as file:  # Use "a" to append to the file
        file.write(f"Date and Time: {current_datetime}\n")
        file.write(f"Client IP: {client_ip}\n")
        file.write(f"Operating System: {user_agent_str}\n\n")

    return redirect(url_variable)



@app.route('/assign')
def assign():
    url_variable = read_url_variable()  # Retrieve the URL variable from the file
    return render_template('set_url.html', url_variable=url_variable)

@app.route('/set_url', methods=['POST'])
def set_url():
    url_variable = request.form.get('url_variable')
    save_url_variable(url_variable)
    return redirect('/doc')


@app.route('/doc')
def display_text_file():
    file_path = 'user_agent.txt'  # Replace with the actual path to your text file

    if not path.exists(file_path):
        file_content = "Empty file"
    else:
        with open(file_path, 'r') as file:
            file_content = file.read()

    return render_template('text_viewer.html', content=file_content)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
