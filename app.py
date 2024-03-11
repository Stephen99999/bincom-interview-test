import mysql.connector
from flask import Flask, render_template, request

app = Flask(__name__)

# Step 1: Establish a connection to the MySQL database
connection = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    db='bincomphptest'
)
cursor = connection.cursor()


# Step 2: Define a route for the front page
@app.route('/')
def front_page():
    return render_template('front_page.html')


# Step 3: Define a route for the web page
@app.route('/polling_unit_results', methods=['GET', 'POST'])
def polling_unit_results():
    if request.method == 'POST':
        polling_unit_id = request.form['polling_unit_id']

        # Step 4: Retrieve the polling unit information from the database based on user input
        with connection.cursor() as cursor:
            query = "SELECT * FROM agentname WHERE pollingunit_uniqueid = %s"
            cursor.execute(query, (polling_unit_id,))
            polling_unit_info = cursor.fetchone()

        if polling_unit_info:
            # Step 5: Fetch the corresponding results for the selected polling unit
            with connection.cursor() as cursor:
                query = "SELECT * FROM announced_lga_results WHERE lga_name = %s"
                cursor.execute(query, (polling_unit_info[5],))  # assuming pollingunit_uniqueid is at index 5
                results = cursor.fetchall()

            # Step 6: Display the results on a webpage
            return render_template("polling_unit_results.html", polling_unit=polling_unit_info, data=results)
        else:
            return "Polling unit not found."

    return render_template('polling_unit.html')


if __name__ == '__main__':
    app.run()