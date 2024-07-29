from flask import Flask, jsonify, request
from datetime import datetime
import csv

app = Flask(__name__)

CSV_FILE_PATH = r"C:\Users\Ogechukweu Tasie\Project-3\Cleaned_StateDatabySeason63_49,48,62.csv"

def fetch_flu_data():
    data = []
    with open(CSV_FILE_PATH, 'r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            data.append(row)
    return data

@app.route('/')
def home():
    return "Welcome to the Flu Data API!"

@app.route('/api/flu-data/us')
def get_us_flu_data():
    data = fetch_flu_data()
    return jsonify(data)

@app.route('/api/flu-data/state/<state>')
def get_state_flu_data(state):
    data = fetch_flu_data()
    state_data = [item for item in data if item['States'] == state]
    return jsonify(state_data)

@app.route('/api/flu-data/history')
def get_historical_flu_data():
    data = fetch_flu_data()
    historical_data = [item for item in data if 'Weekend' in item]
    return jsonify(historical_data)

@app.route('/api/flu-data/filter')
def filter_flu_data():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    strain = request.args.get('Activity_Level_Label')

    data = fetch_flu_data()
    filtered_data = [
        item for item in data
        if (start_date <= datetime.strptime(item['WEEKEND'], '%b-%d-%Y').strftime('%Y-%m-%d') <= end_date) and item['ACTIVITY LEVEL LABEL'] == strain
    ]
    return jsonify(filtered_data)

if __name__ == '__main__':
    app.run(debug=True)

