# import necessary libraries
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# create instance of Flask app
app = Flask(__name__)

# Use PyMongo to establish mongo connection
#app.config["mongo_uri"] = "mongodb://localhost:27017/mars_db"
mongo = PyMongo(app, uri = "mongodb://localhost:27017/mars_db")

# create route that renders index.html template
@app.route("/")
def home():

    # Find one record of data from the mongo database
    mars_info = mongo.db.mars.find_one()

    # Return template and data
    return render_template("index.html", mars_info = mars_info)


@app.route("/scrape")
def scrape():
    # Run the scrape function
    mars_data = scrape_mars.scrape_info()

    # Update the Mongo database using update and upsert=True
    mongo.db.mars.update({}, mars_data, upsert=True)

    # Redirect back to home page
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
