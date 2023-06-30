import concurrent.futures

import flask
from google.cloud import bigquery


app = flask.Flask(__name__)
bigquery_client = bigquery.Client()

@app.route("/")
def classes():
    results = bigquery_client.query(
        """
        SELECT Label, Description
        FROM `bdcc21.openimages.classes`
        ORDER BY Description
    """
    ).result()

    return flask.render_template("classes.html", results=results)


@app.route("/images")
def images():
    label = flask.request.args.get('label')
    description = flask.request.args.get('description')
    results = bigquery_client.query(
        """
        SELECT ImageId FROM `bdcc21.openimages.image_labels`
        WHERE Label = '{}' AND Confidence = 1
        ORDER BY ImageId
        LIMIT 10  
    """.format(label)
    ).result()

    return flask.render_template("images.html", 
         label=label, description=description, results=results)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
