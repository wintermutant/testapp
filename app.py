from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
import os

app = Flask(__name__)

mongo_host = os.environ.get('MONGO_HOST', 'mongodb')
mongo_port = int(os.environ.get('MONGO_PORT', 27017))
client = MongoClient(f'mongodb://{mongo_host}:{mongo_port}/')
db = client.hello_app
names_collection = db.names

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        if name:
            names_collection.insert_one({'name': name})
            return render_template('index.html', greeting=f'Hello {name}!')
        return redirect(url_for('index'))

    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
