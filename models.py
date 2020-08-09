import sqlite3 as sql
import time

def insertUser(username,password):
    con = sql.connect("database.db")
    cur = con.cursor()
    cur.execute("INSERT INTO users (username,password) VALUES (?,?)", (username,password))
    con.commit()
    con.close()

def retrieveUserByUsernamePassword(username, password):
	con = sql.connect("database.db")
	cur = con.cursor()
	statement = "SELECT * FROM users where username = '" + username + "' and password = '" + password + "'"
	cur.execute(statement)
	users = cur.fetchall()
	con.close()
	if(len(users) == 1):
		return True
	return False

def retrieveUserByUsername(username):
	con = sql.connect("database.db")
	cur = con.cursor()
	statement = "SELECT * FROM users where username = '" + username + "'"    #need to do case insenstive check
	cur.execute(statement)
	users = cur.fetchall()
	con.close()
	if(len(users) == 1):
		return True
	return False

def getUserLimtsAndUsage(username):
	con = sql.connect("database.db")
	cur = con.cursor()
	statement = "SELECT credit_used,credit_limit,EMI_used,EMI_limit FROM users where username = '" + username + "'"    #need to do case insenstive check
	cur.execute(statement)
	userLimitsAndUsage = cur.fetchall()
	con.close()
	return userLimitsAndUsage

def getMerchantBankBalance(username):
	con = sql.connect("database.db")
	cur = con.cursor()
	statement = "SELECT merchantBankBalance FROM merchants where username = '" + username + "'"    #need to do case insenstive check
	cur.execute(statement)
	bankBalance = cur.fetchall()
	con.close()
	return bankBalance

def retrieveMerchantByUsernamePassword(username, password):
	con = sql.connect("database.db")
	cur = con.cursor()
	statement = "SELECT * FROM merchants where username = '" + username + "' and password = '" + password + "'"
	print(statement)
	cur.execute(statement)
	users = cur.fetchall()
	con.close()
	if(len(users) == 1):
		return True
	return False

def retrieveMerchantByUsername(username):
	con = sql.connect("database.db")
	cur = con.cursor()
	statement = "SELECT * FROM merchants where username = '" + username + "'" #need to do case insenstive check
	print(statement)
	cur.execute(statement)
	users = cur.fetchall()
	con.close()
	if(len(users) == 1):
		return True
	return False

def retrieveNearbyMerchants():
	con = sql.connect("database.db")
	cur = con.cursor()
	statement = "SELECT * FROM merchants"
	print(statement)
	cur.execute(statement)
	merchants = cur.fetchall()
	con.close()
	return merchants



def insertMerchant(username,password):
    con = sql.connect("database.db")
    cur = con.cursor()
    cur.execute("INSERT INTO merchants (username,password) VALUES (?,?)", (username,password))
    con.commit()
    con.close()


def getAllCreditTransactionsForMerchant(merchantname):
	merchantname = merchantname.strip() #need to see why
	con = sql.connect("database.db")
	cur = con.cursor()
	statement = "SELECT * FROM transaction_history where merchantname = +'" + merchantname + "'"
	print(statement)
	cur.execute(statement)
	merchant_transactions =  cur.fetchall()
	con.close()
	return merchant_transactions

def getAllEMITransactionsForMerchant(merchantname):
	merchantname = merchantname.strip() #need to see why
	con = sql.connect("database.db")
	cur = con.cursor()
	statement = "SELECT username,product_cost,txn_time FROM user_EMI_txn_list where merchantname = +'" + merchantname + "'"
	print(statement)
	cur.execute(statement)
	merchant_transactions =  cur.fetchall()
	con.close()
	return merchant_transactions


def getAllCreditTransactionsForUser(username):
	username = username.strip() #need to see why
	con = sql.connect("database.db")
	cur = con.cursor()
	statement = "SELECT merchantname,txnAmount,txnDate FROM transaction_history where username = +'" + username + "'"
	print(statement)
	cur.execute(statement)
	user_transactions =  cur.fetchall()
	con.close()
	return user_transactions

def getAllEMITransactionsForUser(username):
	username = username.strip() #need to see why
	con = sql.connect("database.db")
	cur = con.cursor()
	statement = "SELECT merchantname,product_name,product_cost,txn_time,num_of_months,processing_fee FROM user_EMI_txn_list where username = +'" + username + "'"
	print(statement)
	cur.execute(statement)
	user_transactions =  cur.fetchall()
	con.close()
	return user_transactions



def transfer_money(username, merchantname,txnAmount):
	con = sql.connect("database.db")
	cur = con.cursor()
	get_user_limits_statement = "select credit_used,credit_limit from users where username = '" + username +"'"
	cur.execute(get_user_limits_statement)
	user_limits =  cur.fetchall()
	userCreditUsed = int(user_limits[0][0])
	userCreditLimit= int(user_limits[0][1])
	if userCreditUsed+int(txnAmount)>userCreditLimit:
		return False
	credit_merchant_money_statement =  "UPDATE merchants SET merchantBankBalance = merchantBankBalance +" + txnAmount + " where username= '" + merchantname +"'"
	debit_user_money_statement =  "UPDATE users SET credit_used = credit_used + " + txnAmount + " where username= '" + username +"'"
	cur.execute(credit_merchant_money_statement)
	con.commit()
	cur.execute(debit_user_money_statement)
	con.commit()
	cur.execute("INSERT into transaction_history VALUES(?,?,?,?)", (username,merchantname,txnAmount,time.time()))
	con.commit()
	con.close()
	return True




def transfer_EMI_money(username, merchantname,productname,numOfMonths,productCost):
	con = sql.connect("database.db")
	cur = con.cursor()
	get_user_limits_statement = "select EMI_used,EMI_limit from users where username = '" + username +"'"
	cur.execute(get_user_limits_statement)
	user_limits =  cur.fetchall()
	userEMIUsed = int(user_limits[0][0])
	userEMILimit= int(user_limits[0][1])
	if userEMIUsed+int(productCost)>userEMILimit:
		return False
	credit_merchant_money_statement =  "UPDATE merchants SET merchantBankBalance = merchantBankBalance +" + productCost + " where username= '" + merchantname +"'"
	debit_user_money_statement =  "UPDATE users SET EMI_used = EMI_used + " + productCost + " where username= '" + username +"'"
	cur.execute(credit_merchant_money_statement)
	con.commit()
	cur.execute(debit_user_money_statement)
	con.commit()
	processingFee = (int(numOfMonths)*int(productCost))/100
	cur.execute("INSERT into user_EMI_txn_list VALUES(?,?,?,?,?,?,?)", (username,merchantname,productname,time.time(),numOfMonths,productCost,processingFee))
	con.commit()
	con.close()
	return True


