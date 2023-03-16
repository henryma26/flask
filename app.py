import pandas as pd
from flask import Flask, render_template_string
import concurrent.futures
import random
import time

app = Flask(__name__)

# Sample DataFrame with 'price' column
data = {
    'item': ['Item1', 'Item2', 'Item3', 'Item4', 'Item5', 'Item6', 'Item7', 'Item8', 'Item9', 'Item10'],
    'price': [random.randint(1, 100) for _ in range(10)],
}
df = pd.DataFrame(data)

# Function to update the prices and rank the DataFrame
def update_prices_and_rank():
    while True:
        time.sleep(60)
        df['price'] = [random.randint(1, 100) for _ in range(10)]  # Update the prices
        df['rank'] = df['price'].rank(method='min', ascending=False).astype(int)  # Rank the rows
        df.sort_values('rank', inplace=True)  # Sort the DataFrame based on the rank

# Start the price update and ranking thread
executor = concurrent.futures.ThreadPoolExecutor()
executor.submit(update_prices_and_rank)

@app.route("/")
def index():
    # Rank the DataFrame before displaying
    df['rank'] = df['price'].rank(method='min', ascending=False).astype(int)
    df.sort_values('rank', inplace=True)
    
    # Render the DataFrame as an HTML table
    table = df.to_html(index=False, classes=["table", "table-striped", "table-hover"])
    
    # HTML template with Bootstrap CSS for table styling
    template = '''
    <!doctype html>
    <html lang="en">
      <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <meta http-equiv="refresh" content="60"> <!-- Auto-refresh every 60 seconds -->
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet">
        <title>Ranked DataFrame</title>
      </head>
      <body>
        <div class="container">
          <h1 class="mt-4">Ranked DataFrame</h1>
          {{ table|safe }}
        </div>
      </body>
    </html>
    '''
    
    return render_template_string(template, table=table)

if __name__ == "__main__":
    app.run(debug=True)