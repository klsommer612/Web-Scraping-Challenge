from flask import Flask, render_template
# Import scrape_mars
import scrape_mars
import pymongo

# Create an instance of the Flask app
app = Flask(__name__)

# Create connection ans store in variable
conn = 'mongodb://localhost:27017/mission_to_mars'

client = pymongo.MongoClient(conn)

@app.route('/')
def index():
    mars = client.db.mars.find_one()
    return render_template('index.html', mars=mars)

@app.route('/scrape')
def scrape():
    mars = client.db.mars
    mars_data = scrape_mars.scrape()
    mars.update({}, mars_data)
    return 'Scrape Complete'

if __name__ == '__main__':
    app.run(debug=True)
