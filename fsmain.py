from flask import Flask
from flask import render_template
from flask import request
from flask import redirect, url_for, session
import models as dbHandler

import json

import requests

app = Flask(__name__)
app.secret_key = 'EasyPayIITIANS'

@app.route('/systime', methods=['GET'])
def testsystime():
	response = requests.get('http://localhost:8080/FS-backend/systime')
	print(response)
	json_data = response.json()
	return str(json_data)


@app.route('/scripts.js', methods=['GET'])
def hostScriptsJS():
	return render_template('scripts.js')

@app.route('/homepage', methods=['GET'])
def mainHomePage():


	# request.setRequestHeader('Content-type', 'application/json');
	# request.setRequestHeader('Access-Control-Allow-Origin', '*')
	# request.setRequestHeader('Access-Control-Allow-Methods', 'GET, POST, PUT')
	# request.setRequestHeader('Access-Control-Allow-Headers',
	# 						 ' Origin, Content-Type, Accept, Authorization, X-Request-With')
	# request.setRequestHeader('Access-Control-Allow-Credentials', ' true');

	response = requests.get("http://localhost:8080/FS-backend/systime", params=None,
							headers={
								"Access-Control-Allow-Origin": "*"
							})
	print(response)
	# json_data = response.json()
	return render_template('index.html')


@app.route("/sellADpage", methods=['GET'])
def sellADpage():
	return render_template('postAd.html')


@app.route("/postADInfo", methods=['POST'])
def postADInfo():
	print("Reached here..")
	city = request.form['city']
	address = request.form['address']
	description = request.form['description']
	propertyCost = request.form['propertyCost']
	numOfPoolMembers = request.form['numOfPoolMembers']
	numOfApartmentFloors = request.form['numOfApartmentFloors']
	numOfFlatsPerFloor = request.form['numOfFlatsPerFloor']
	apartmentArea = request.form['apartmentArea']

	payload = '{"commonDetails":{"lenderID":"7ac131aa-43ff-4f4f-933e-8c14e868f8f8","propertyType":"RESIDENTIAL","constructionType":"APARTMENT_CONSTRUCTION","city": "'+ city +'","latlon":{"latitude":109.99,"longitude":-196.87},"address":"'+ address +'","description":"'+ description +'","propertyCost":'+ propertyCost +',"numOfPoolMembers":'+ numOfPoolMembers +'},"houseconstructionAdDetails":{},"standaloneBuildingAdDetails":{},"apartmentConstructionAdDetails":{"numOfApartmentFloors":'+ numOfApartmentFloors +',"numOfFlatsPerFloor":'+ numOfFlatsPerFloor +',"apartmentArea":'+ apartmentArea +',"lengthOfApartmentPlot":100,"breadthOfApartmentPlot":30,"numOfAllowedFloorsForApartment":4}}'
	print(payload)

	response = requests.post("http://localhost:8080/FS-backend/v1.0/ad-info/create-or-update-ad", data=payload, headers={'Content-type':'application/json', 'Accept':'application/json'}
)
	print(response)
	return render_template('postAd.html')


    # if request.method=='POST':
    #     numoforders = request.form['numoforders']
    #     totalcost = request.form['totalcost']
    #     vehicleNumber = 1007
    #     # dbHandler.insertDailyRecord(vehicleNumber,int(numoforders),int(totalcost))
    #     # return redirect(url_for('mainpage'))
    # else:
    #     return render_template('postAd.html')



# @app.route('/user', methods=['GET'])
# def userhomePage():
# 	username="tarun"
# 	merchantList = dbHandler.retrieveNearbyMerchants()
# 	userCreditLimits = dbHandler.getUserLimtsAndUsage(username)
# 	creditTxns = dbHandler.getAllCreditTransactionsForUser(username)
# 	EMITxns = dbHandler.getAllEMITransactionsForUser(username)
# 	return render_template('user.html', result1 = merchantList, result2 = userCreditLimits, result3 = creditTxns, result4= EMITxns)
# 	# return render_template('login.html')




if __name__ == '__main__':
    app.run(debug=True)
