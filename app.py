from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/expenses', methods=['GET', 'POST'])
def expenses():
    if request.method == 'GET':
        conn = sqlite3.connect('expenses.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM expenses ORDER BY id DESC')
        expenses = cursor.fetchall()
        conn.close()
        return jsonify({'expenses': expenses})
    elif request.method == 'POST':
        data = request.get_json()
        description = data['description']
        amount = data['amount']

        if description and amount:
            conn = sqlite3.connect('expenses.db')
            cursor = conn.cursor()
            cursor.execute('INSERT INTO expenses (description, amount) VALUES (?, ?)', (description, amount))
            conn.commit()
            conn.close()

            return jsonify({'message': 'Expense added successfully'})
        else:
            return jsonify({'error': 'Description and amount are required'}), 400

if __name__ == '__main__':
    app.run(debug=True)