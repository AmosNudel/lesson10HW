from flask import Flask, render_template, request, jsonify
import pandas as pd

app = Flask(__name__)

# Load data
df = pd.read_csv('data.csv')

# Home route
@app.route('/')
def home():
    return render_template('index.html', data=df.to_dict(orient='records'))

@app.route('/add', methods=['POST'])
def add():
    new_data = request.get_json()
    global df
    
    # Generate a new id
    new_id = df['id'].max() + 1 if not df.empty else 1
    new_data['id'] = new_id

    df = df._append(new_data, ignore_index=True)
    # Save the updated DataFrame to CSV 
    df.to_csv('data.csv', index=False)
    return jsonify(df.to_dict(orient='records'))

@app.route('/delete/<int:id>', methods=['DELETE'])
def delete(id):
    global df
    # Check if the ID exists
    if id in df['id'].values:
        # Drop the row with the matching ID
        df = df[df['id'] != id]
        
        # Save the updated DataFrame to the CSV file
        df.to_csv('data.csv', index=False)
        return jsonify({'message': f'Entry with ID {id} deleted successfully.'}), 200
    else:
        return jsonify({'error': f'ID {id} not found.'}), 404
    
@app.route('/update/<int:id>', methods=['PUT'])
def update(id):
    global df
    updated_data = request.get_json()

    # Check if the ID exists
    if id in df['id'].values:
        # Update the row with the new data
        df.loc[df['id'] == id, 'name'] = updated_data.get('name', df.loc[df['id'] == id, 'name'].values[0])
        df.loc[df['id'] == id, 'age'] = updated_data.get('age', df.loc[df['id'] == id, 'age'].values[0])
        
        # Save the updated DataFrame to the CSV file
        df.to_csv('data.csv', index=False)
        return jsonify({'message': f'Entry with ID {id} updated successfully.'}), 200
    else:
        return jsonify({'error': f'ID {id} not found.'}), 404




if __name__ == '__main__':
    app.run(debug=True)
