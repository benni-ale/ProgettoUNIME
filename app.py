from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    # Placeholder for news extraction logic
    news_data = []  # This will be replaced with actual data
    return render_template('index.html', news=news_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)