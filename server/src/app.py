# from crypt import methods
# from crypt import methods
from distutils.log import debug
from flask import Flask, jsonify, request
from flask_cors import cross_origin
import json

app = Flask(__name__)

dictMarkers = {
    "Chemudugunta": {
        "lat": 14.3777, "lng": 79.9291
    },
    "Kakutur": {
        "lat": 14.3605, "lng": 79.9291
    },
    "Kumkumpudi": {
        "lat": 14.3785, "lng": 79.9137
    },
    "Padarupalli": {
        "lat": 14.3993, "lng": 79.9626
    },
    "Kallurpalli Rural": {
        "lat": 14.3804, "lng": 79.9584
    },
    "Golagamudi": {
        "lat": 14.3519, "lng": 79.9759
    },
    "Kanuparthipadu": {
        "lat": 14.3819, "lng": 79.992
    },
    "Sportello Presto": {
        "lat": 14.413671, "lng": 79.982161
    },
    "Ambapuram": {
        "lat": 14.4163, "lng": 79.9221
    },
    "Akkacheruvupadu": {
        "lat": 14.4390, "lng": 79.9165
    },
    "Ogurupadu": {
        "lat": 14.433799, "lng": 79.931733
    },
    "Vengalrao Nagar": {
        "lat": 14.4172, "lng": 79.9445
    },
    "Kottur": {
        "lat": 14.4107, "lng": 79.9438
    },
    "Ayyappa Swamy Temple": {
        "lat": 14.4030, "lng": 79.9500
    },
    "Ganga Bhavani Temple, Kanuparthipadu": {
        "lat": 14.393288, "lng": 79.982344
    },
    "Vijaya Hospital, Pogathota": {"lat": 14.449, "lng": 79.9832},
    "KIMS Hospital, Ambedkar Nagar": {"lat": 14.4344, "lng": 79.9682},
    "Apollo Hospitals, Ramji Nagar": {"lat": 14.4383, "lng": 79.9926},
    "Narayana Hospital, Chinthareddy Palem": {"lat": 14.4464, "lng": 79.983},
    "Vijaya Care Hospital, Rama Murthy Palem": {"lat": 14.452165, "lng": 79.987839},
    "Rainbow Super Speciality Hospital, Brindavan Colony": {"lat": 14.452, "lng": 79.9859},
    "Simhapuri Hospital, Balaji Nagar": {"lat": 14.4481, "lng": 79.9953},
    "Lotus Hospital, Pogathota": {"lat": 14.4486, "lng": 79.9847},
    "St. Joseph Hospital, Santhapet": {"lat": 14.457659, "lng": 79.983007},
    "Jayabharath Hospital, Somasekhara Puram": {"lat": 14.44503, "lng": 79.983217},
}


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


@app.route("/getMarkers", methods=["GET"], strict_slashes=False)
@cross_origin()
def getMarkers():
    args = request.args
    print(args)
    markers = []
    dictMarkerType = {0: FacilityCenter.fbfMarkersList,
                      1: FacilityCenter.mbfMarkersList,
                      2: FacilityCenter.hospitalMarkersList}
    type = 2
    if(args.get("type") == "fixed"):
        type = 0
    elif(args.get("type") == "mobile"):
        type = 1

    for i in range(len(dictMarkerType[type])):
        d = {"id": i+1,
             "location": dictMarkerType[type][i],
             "position": dictMarkers[dictMarkerType[type][i]]}
        markers.append(d)
    res = jsonify(json.dumps({"markers": markers}))
    # res.headers.add("Access-Control-Allow-Origin", "*")
    return res, 200


@app.route("/hospitalDemand", methods=["POST"], strict_slashes=False)
@cross_origin()
def newHospitalDemand():
    hospitalDemand = request.json["body"]
    print("hospital demand : ", hospitalDemand)
    register_hospital_demand(json.loads(hospitalDemand))
    res = jsonify(json.dumps({"msg": "successfully registered demand",
                  "hospitalDemand": hospitalDemand, "count": FacilityCenter.HospitalDemandCount}))
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

    fbfMarkersList = []
    mbfMarkersList = []
    hospitalMarkersList = []
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
    if(donor["facilityCenter"] == "fixed"):
        FacilityCenter.fbfMarkersList.append(donor["location"])
    elif(donor["facilityCenter"] == "mobile"):
        FacilityCenter.mbfMarkersList.append(donor["location"])


def register_hospital_demand(hospitalDemand):
    FacilityCenter.HospitalDemandCount += 1
    FacilityCenter.hospitalDemandList.append(hospitalDemand)
    FacilityCenter.hospitalMarkersList.append(hospitalDemand["hospitalName"])

    # FacilityCenter.hospitalDemandList.append(HospitalDemand(
    #     hospitalDemand["hospitalName"], hospitalDemand["age"], hospitalDemand["bloodgroup"], hospitalDemand["quantity"]).dict)


if __name__ == '__main__':
    app.run(debug=True)
