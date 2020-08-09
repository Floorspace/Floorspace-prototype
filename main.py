from flask import Flask
from flask import render_template
from flask import request
from flask import redirect, url_for, session
import models as dbHandler

app = Flask(__name__)
app.secret_key = 'EasyPayIITIANS'


def setSessionCredentials(username, usertype):
	session['username'] = username
	session['usertype'] = usertype

def storeTransactionDetails(usertxnname, merchantname, txnamount):
	session['usertxnname'] = usertxnname
	session['merchanttxnname'] = merchantname
	session['txnamount'] = txnamount

def getTxnAmount():
	if('txnamount' in session ):
		return session['txnamount']
	return ""

def getUserTxnName():
	if('usertxnname' in session ):
		return session['usertxnname']
	return ""
	
def getMerchantTxnName():
	if('merchanttxnname' in session ):
		return session['merchanttxnname']
	return ""

def getUserNameInCookies():
	if('username' in session and 'usertype' in session and session['username'] != "" and session['usertype'] == "user"):
		return session['username']
	return ""

def getIsUserLoggedin():
	if('username' in session and 'usertype' in session and session['username'] != "" and session['usertype'] == "user"):
		return True
	return False

def getIsMerchantLoggedin():
	if('username' in session and 'usertype' in session and session['username'] != "" and session['usertype'] == "merchant"):
		return True
	return False

def getMerchantNameInCookies():
	if('username' in session and 'usertype' in session and session['username'] != "" and session['usertype'] == "merchant"):
		return session['username']
	return ""

def getErrorString():
	if('errorString' in session ):
		return session['errorString']
	return ""

def setErrorString(error):
	session['errorString'] = error


@app.route('/loginscreen', methods=['POST', 'GET'])
def loginscreen():
	setErrorString("")
	setSessionCredentials("", "")
	if request.method=='POST':
		username = request.form['username']
		password = request.form['password']
		usertype = request.form['usertype']
		if(usertype == "user"):
			if(dbHandler.retrieveUserByUsername(username)):
				if(dbHandler.retrieveUserByUsernamePassword(username, password)):
					setSessionCredentials(username, usertype)
					return redirect(url_for('userhomePage'))
				else:
					if(getErrorString() == ""):
						setErrorString("Invalid password")
					return redirect(url_for('loginpage'))
			else:
				if(getErrorString() == ""):
					setErrorString("User doesn't Exists Please check username")
				return redirect(url_for('loginpage'))
		else:
			if(dbHandler.retrieveMerchantByUsername(username)):
				if(dbHandler.retrieveMerchantByUsernamePassword(username, password)):
					setSessionCredentials(username, usertype)
					return redirect(url_for('merchanthomePage'))
				else:
					if(getErrorString() == ""):
						setErrorString("Invalid password")
					return redirect(url_for('loginpage'))
			else:
				if(getErrorString() == ""):
					setErrorString("Merchant doesn't Exists Please check merchantname")
				return redirect(url_for('loginpage'))
		return render_template('login.html')
	else:
		return render_template('login.html')


@app.route('/signupscreen', methods=['POST', 'GET'])
def signupscreen():
	setErrorString("")
	setSessionCredentials("", "")
	if request.method=='POST':
		username = request.form['username']
		password = request.form['password']
		usertype = request.form['usertype']
		if(usertype == "user"):
			if(dbHandler.retrieveUserByUsername(username)):
				if(getErrorString() == ""):
					setErrorString("User Already Exists Please login")
				return redirect(url_for('loginpage'))
			else:
				dbHandler.insertUser(username, password)
				setSessionCredentials(username, usertype)
				return redirect(url_for('userhomePage'))
		else:
			if(dbHandler.retrieveMerchantByUsername(username)):
				if(getErrorString() == ""):
					setErrorString("Merchant Already Exists login")
				return redirect(url_for('loginpage'))
			else:
				dbHandler.insertMerchant(username, password)
				setSessionCredentials(username, usertype)
				return redirect(url_for('merchanthomePage'))
		return render_template('signup.html')
	else:
		return render_template('signup.html')


@app.route('/merchanthomePage', methods=['GET'])
def merchanthomePage():
	if(getIsMerchantLoggedin()):
		merchantName = getMerchantNameInCookies()
		if merchantName!="":
			merchantCreditTxnList = dbHandler.getAllCreditTransactionsForMerchant(merchantName)
			merchantEMITxnList = dbHandler.getAllEMITransactionsForMerchant(merchantName)
			bankBalance = dbHandler.getMerchantBankBalance(merchantName)
			return render_template('merchant.html', result1 = merchantCreditTxnList, result2 = merchantEMITxnList,result3 = bankBalance)
	return render_template('login.html')

@app.route('/paycredit', methods=['POST'])
def pay():
	if(getIsUserLoggedin()):
		if request.method=='POST':
			userName = request.form['userId']
			merchantName = request.form['merchantId']
			amount = request.form['amount'] 
			userName = getUserNameInCookies()
			print("merchant name" + merchantName)
			print("user name" + userName)
			if merchantName!="" and userName!="":
				transaction_status = dbHandler.transfer_money(userName,merchantName, amount)
				merchantList = dbHandler.retrieveNearbyMerchants()
				userCreditLimits = dbHandler.getUserLimtsAndUsage(userName)
				creditTxns = dbHandler.getAllCreditTransactionsForUser(userName)
				EMITxns = dbHandler.getAllEMITransactionsForUser(userName)
				return render_template('user.html', result = merchantList, result2 = userCreditLimits, result3 = creditTxns, result4= EMITxns)
	return render_template('login.html')


@app.route('/tenureEMI', methods=['POST'])
def tenureEMI():
	if(getIsUserLoggedin()):
		if request.method=='POST':
			userName = request.form['userId']
			merchantName = request.form['merchantId']
			amount = request.form['amount'] 
			userName = getUserNameInCookies()
			print("merchant name before" + merchantName)
			print("user name before" + userName)
			if merchantName!="" and userName!="":
				storeTransactionDetails(userName,merchantName,amount)
				print("userName"+userName)
				print("merchantName"+merchantName)
				print("amount"+amount)
				return render_template('emipay.html')	
	return render_template('login.html')

@app.route('/payEMI', methods=['POST'])
def payEMI():
	if(getIsUserLoggedin()):
		if request.method=='POST':
			txnamount = getTxnAmount()
			userName = getUserTxnName()
			merchantName = getMerchantTxnName()
			productName = request.form['productName']
			numOfEMIMonths = request.form['numOfEMIMonths']
			print("merchant name after" + merchantName)
			print("user name after" + userName)
			if merchantName!="" and userName!="":
				transaction_status = dbHandler.transfer_EMI_money(userName, merchantName,productName,numOfEMIMonths,txnamount)
				merchantList = dbHandler.retrieveNearbyMerchants()
				userCreditLimits = dbHandler.getUserLimtsAndUsage(userName)
				creditTxns = dbHandler.getAllCreditTransactionsForUser(userName)
				EMITxns = dbHandler.getAllEMITransactionsForUser(userName)
				return render_template('user.html', result = merchantList, result2 = userCreditLimits, result3 = creditTxns, result4= EMITxns)
	return render_template('login.html')



@app.route('/user', methods=['GET'])
def userhomePage():
	if(getIsUserLoggedin()):
		username = getUserNameInCookies()
		if username!="":
			merchantList = dbHandler.retrieveNearbyMerchants()
			userCreditLimits = dbHandler.getUserLimtsAndUsage(username)
			creditTxns = dbHandler.getAllCreditTransactionsForUser(username)
			EMITxns = dbHandler.getAllEMITransactionsForUser(username)
			return render_template('user.html', result1 = merchantList, result2 = userCreditLimits, result3 = creditTxns, result4= EMITxns)
	return render_template('login.html')



@app.route('/loginpage', methods=['GET'])
def loginpage():
	localErrorString = getErrorString()
	setErrorString("")
	return render_template('login.html', error = localErrorString)

@app.route('/signuppage', methods=['GET'])
def signuppage():
	setErrorString("")
	return render_template('signup.html')


@app.route('/order/<name>', methods=['GET', 'POST'])
def order(name):
	if(getIsUserLoggedin() == False):
		return render_template('login.html')
	params = {}
	if request.method=='POST':
		params['status'] = 'success'
	
	params['merchant'] = name
	params['userId'] = session['username']
	return render_template('order.html', result = params)


@app.route('/upi', methods=['GET', 'POST'])
def upiPay():
	if(getIsUserLoggedin() == False):
		return render_template('login.html')
	params = {}
	if request.method=='POST':
		params['status'] = 'success'

	params['userId'] = session['username']	
	#params['merchant'] = name

	upis  = []
	upis.append('abc@sbi')
	upis.append('abc@hsbc')
	upis.append('abc@hdfc')
	return render_template('upiPay.html', result = upis)

@app.route('/otp', methods=['GET', 'POST'])
def getOtp():
	if(getIsUserLoggedin() == False):
		return render_template('login.html')

	return render_template('otp.html')


if __name__ == '__main__':
    app.run(debug=True)
