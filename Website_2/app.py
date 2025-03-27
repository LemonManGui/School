from flask import Flask, send_from_directory, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/pdf')
def serve_pdf():
    return send_from_directory('static', 'mass_info.pdf')

if __name__ == '__main__':
    app.run(debug=True)