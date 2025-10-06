from flask import Flask #to create web application
from flask import jsonify #converts python objects to json HTTP responses
from flask import request

app = Flask(__name__)
teams={"CodeOrbit":["Ikhlas","Sundus","Hanan","Muzna","Fatma","Haya","Mariya","Hoor","Arooba","Aya"],
        "DataScience":["Quds","Fatma AlBalushi","Hajer"]
}

@app.route("/get_team_members")
def get_team_members():
    team_name=request.args.get("team_name")
    return jsonify(teams.get(team_name,[]))

@app.route("/get_all_teams")
def get_all_teams():
    return jsonify(list(teams.keys()))

if __name__=="__main__":
    app.run(host="0.0.0.0", port=5000)


