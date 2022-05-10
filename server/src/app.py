# from crypt import methods
# from crypt import methods
from distutils.log import debug
from flask import Flask, jsonify, request
from flask_cors import cross_origin
import json

app = Flask(__name__)


@app.route("/", methods=["POST"], strict_slashes=False)
@cross_origin()
def home():
    donor = request.json["body"]
    print("donor : ", donor, type(donor))
    register_donor(json.loads(donor))
    res = jsonify(json.dumps({"msg": "successfully registered donor", "donor": donor, "donor count": FacilityCenter.donorCount,
                  "fbf": FacilityCenter.fbfCount, "mbf": FacilityCenter.mbfCount, "bloodCenterCount": FacilityCenter.bloodCenterCount, "donorsList": FacilityCenter.donorsList, "fbfDonorsList": FacilityCenter.fbfDonorsList, "mbfDonorsList": FacilityCenter.mbfDonorsList, "bloodCenterDonorsList": FacilityCenter.bloodCenterDonorsList}))
    # res.headers.add("Access-Control-Allow-Origin", "http://localhost:3000")
    # res.headers["Content-Type"]="application/json"
    return res, 200, {'Content-Type': 'application/json; charset=utf-8'}


@app.route("/hospitalDemand", methods=["POST"], strict_slashes=False)
@cross_origin()
def newHospitalDemand():
    hospitalDemand = request.json["body"]
    print("hospital demand : ", hospitalDemand)
    register_hospital_demand(json.loads(hospitalDemand))
    res = jsonify(json.dumps({"msg":"successfully registered demand", "hospitalDemand":hospitalDemand,"count":FacilityCenter.HospitalDemandCount}))
    return res, 200, {'Content-Type': 'application/json; charset=utf-8'}

@app.route("/showHospitalDemand", methods=["GET"], strict_slashes=False)
@cross_origin()
def showHospitalDemand():
    return jsonify(json.dumps({"hospitalDemand": FacilityCenter.hospitalDemandList})), 200


@app.route("/fbf", methods=["GET"], strict_slashes=False)
@cross_origin()
def fbf():
    return jsonify(json.dumps({"donors": FacilityCenter.fbfDonorsList})), 200


@app.route("/mbf", methods=["GET"], strict_slashes=False)
@cross_origin()
def mbf():
    return jsonify(json.dumps({"donors": FacilityCenter.mbfDonorsList})), 200


@app.route("/bloodCenter", methods=["GET"], strict_slashes=False)
@cross_origin()
def bloodCenter():
    return jsonify(json.dumps({"donors": FacilityCenter.bloodCenterDonorsList})), 200


@app.route("/all", methods=["GET"], strict_slashes=False)
@cross_origin()
def all():
    return jsonify(json.dumps({"donors": FacilityCenter.donorsList})), 200


class FacilityCenter:

    donorCount = 0
    fbfCount = 0
    mbfCount = 0
    bloodCenterCount = 0

    donorsList = []
    fbfDonorsList = []
    mbfDonorsList = []
    bloodCenterDonorsList = []

    hospitalDemandList = []
    HospitalDemandCount = 0


class HospitalDemand:

    def __init__(self, hospitalName, age, bloodgroup, quantity):
        self.hospitalName = hospitalName
        self.age = age
        self.bloodgroup = bloodgroup
        self.quantity = quantity


class Donor:

    def __init__(self, fname, lname, age, bloodGroup, location, mobile, facilityChoice):
        self.firstName = fname
        self.lastName = lname
        self.age = age
        self.bloodGroup = bloodGroup
        self.location = location
        self.mobile = mobile
        self.facilityChoice = facilityChoice
        self.list = [fname, lname, age, bloodGroup,
                     location, mobile, facilityChoice]
        self.dict = {"firstName": fname, "lastName": lname, "age": age, "bloodGroup": bloodGroup,
                     "location": location, "mobile": mobile, "facilityChoice": facilityChoice}

        if(facilityChoice == "fixed"):
            FacilityCenter.fbfCount += 1
            FacilityCenter.fbfDonorsList.append(self.dict)
        elif(facilityChoice == "mobile"):
            FacilityCenter.mbfCount += 1
            FacilityCenter.mbfDonorsList.append(self.dict)
        else:
            FacilityCenter.bloodCenterCount += 1
            FacilityCenter.bloodCenterDonorsList.append(self.dict)

        FacilityCenter.donorCount += 1


def register_donor(donor):
    FacilityCenter.donorsList.append(Donor(donor["firstName"], donor["lastName"], donor["age"],
                                     donor["bloodGroup"], donor["location"], donor["mobile"], donor["facilityCenter"]).dict)


def register_hospital_demand(hospitalDemand):
    FacilityCenter.HospitalDemandCount+=1
    FacilityCenter.hospitalDemandList.append(hospitalDemand)
    # FacilityCenter.hospitalDemandList.append(HospitalDemand(
    #     hospitalDemand["hospitalName"], hospitalDemand["age"], hospitalDemand["bloodgroup"], hospitalDemand["quantity"]).dict)


if __name__ == '__main__':
    app.run(debug=True)
