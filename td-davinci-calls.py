# install the requests package using 'pip3 install requests'
import requests
import json
from flask import Flask, request
import os

apiKey = os.environ.get('TD_API_KEY')

app = Flask('TdStudentAnalyzer')

class Customer:
  def __init__(self, total=0, balance=0, education=0, transport=0, bills=0, entertainment=0, food=0,
                 shopping=0, other=0, totalEducation=0, totalTransport=0, totalBills=0, totalEntertainment=0,
                 totalFood=0, totalShopping=0, totalOther=0):
    self.balance = balance
    self.total = total

    self.education = education
    self.transport = transport
    self.bills = bills
    self.entertainment = entertainment
    self.food = food
    self.shopping = shopping
    self.other = other

    self.totalEducation = totalEducation
    self.totalTransport = totalTransport
    self.totalBills = totalBills
    self.totalEntertainment = totalEntertainment
    self.totalFood = totalFood
    self.totalShopping = totalShopping
    self.totalOther = totalOther

class RatioAverages:
    def __init__(self, midHigh, lowMid):
        self.midHigh = midHigh
        self.lowMid = lowMid

class YoungAdultAverage():
    def __init__(self, total=0, balance=0, education=0, transport=0, bills=0, entertainment=0, food=0,
                 shopping=0, other=0, totalEducation=0, totalTransport=0, totalBills=0, totalEntertainment=0,
                 totalFood=0, totalShopping=0, totalOther=0):
        self.balance = balance
        self.total = total

        self.education = education
        self.transport = transport
        self.bills = bills
        self.entertainment = entertainment
        self.food = food
        self.shopping = shopping
        self.other = other

        self.totalEducation = totalEducation
        self.totalTransport = totalTransport
        self.totalBills = totalBills
        self.totalEntertainment = totalEntertainment
        self.totalFood = totalFood
        self.totalShopping = totalShopping
        self.totalOther = totalOther

class StudentAverage():
    def __init__(self, total=0, balance=0, education=0, transport=0, bills=0, entertainment=0, food=0,
                 shopping=0, other=0, totalEducation=0, totalTransport=0, totalBills=0, totalEntertainment=0,
                 totalFood=0, totalShopping=0, totalOther=0):
        self.balance = balance
        self.total = total

        self.education = education
        self.transport = transport
        self.bills = bills
        self.entertainment = entertainment
        self.food = food
        self.shopping = shopping
        self.other = other

        self.totalEducation = totalEducation
        self.totalTransport = totalTransport
        self.totalBills = totalBills
        self.totalEntertainment = totalEntertainment
        self.totalFood = totalFood
        self.totalShopping = totalShopping
        self.totalOther = totalOther


youngAdultCustomers = []
studentCustomers = []

adultAverage = YoungAdultAverage()
studentAverage = StudentAverage()


def getCustomerAccountsBalance(custId):
    response = requests.get('https://api.td-davinci.com/api/simulants/' + custId + '/simulatedaccounts',
    headers = { 'Authorization': apiKey })
    accounts = json.loads(response.text).get('result').get('bankAccounts')
    credits = json.loads(response.text).get('result').get('creditCardAccounts')
    balance=0
    for account in accounts:
        balance += account.get('balance')
    for credit in credits:
        balance -= credit.get('balance')
    return balance


def getCustomerTransactionsById(custId):
    response  = requests.get('https://api.td-davinci.com/api/customers/'+ custId  +'/transactions',
    headers = { 'Authorization': apiKey })
    return response.text


def getTransactionHistory(custId):
    response = requests.post('https://api.td-davinci.com/api/simulants/'+ custId +'/simulatedtransactions/search',
                            headers = {'Authorization': apiKey},
                            json = {'continuationToken': '', 'searchCriteria': [{'key': 'originationDateTime', 'operation': '>', 'value': '2019-09'}]})
    return response.text


def getCustomerById(custId):
    response = requests.get('https://api.td-davinci.com/api/customers/'+ custId +'/transactions',
                            headers = {'Authorization': apiKey})
    return response.text


def rawDataCall(token = ''):
    print(token)
    response = requests.post('https://api.td-davinci.com/api/raw-customer-data',
                             headers={'Authorization': apiKey},
                             json={'continuationToken': token})
    return response.text


def getAllCustomers():
    virtualCustomers = json.loads(rawDataCall())
    i = 0
    while len(virtualCustomers) > 0 and i < 1:
        for virtualCustomer in virtualCustomers.get('result').get('customers'):
            if 23 < virtualCustomer.get('age') < 30:
                youngAdultCustomers.append(virtualCustomer)
            elif 17 < virtualCustomer.get('age') <= 23:
                studentCustomers.append(virtualCustomer)

        virtualCustomers = json.loads(rawDataCall(virtualCustomers.get('result').get('continuationToken')))
        i += 1


def initialiseModel():
    getAllCustomers()

    for adult in youngAdultCustomers:
        balance = getCustomerAccountsBalance(adult.get('id'))
        adultAverage.balance += balance
        adultAverage.total += balance
        transactions = json.loads(getTransactionHistory(adult.get('id')))
        for transaction in transactions.get('result'):
            amount = abs(transaction.get('currencyAmount'))
            adultAverage.total += amount
            tagType = transaction.get('categoryTags')[0]
            if tagType == 'Food and Dining':
                adultAverage.totalFood += amount
            elif tagType == 'Education':
                adultAverage.totalEducation += amount
            elif tagType == 'Auto and Transport':
                adultAverage.totalTransport += amount
            elif tagType == 'Bills and Utilities':
                adultAverage.totalBills += amount
            elif tagType == 'Entertainment':
                adultAverage.totalEntertainment += amount
            elif tagType == 'Shopping':
                adultAverage.totalShopping += amount
            elif tagType != 'Transfer':
                adultAverage.totalOther += amount

    adultAverage.food = adultAverage.totalFood / adultAverage.total
    adultAverage.education = adultAverage.totalEducation / adultAverage.total
    adultAverage.transport = adultAverage.totalTransport / adultAverage.total
    adultAverage.bills = adultAverage.totalBills / adultAverage.total
    adultAverage.entertainment = adultAverage.entertainment / adultAverage.total
    adultAverage.shopping = adultAverage.shopping / adultAverage.total
    adultAverage.other = adultAverage.other / adultAverage.total

    for student in studentCustomers:
        balance = getCustomerAccountsBalance(student.get('id'))
        studentAverage.balance += balance
        studentAverage.total += balance
        transactions = json.loads(getTransactionHistory(student.get('id')))
        for transaction in transactions.get('result'):
            amount = abs(transaction.get('currencyAmount'))
            studentAverage.total += amount
            tagType = transaction.get('categoryTags')[0]
            if tagType == 'Food and Dining':
                studentAverage.totalFood += amount
            elif tagType == 'Education':
                studentAverage.totalEducation += amount
            elif tagType == 'Auto and Transport':
                studentAverage.totalTransport += amount
            elif tagType == 'Bills and Utilities':
                studentAverage.totalBills += amount
            elif tagType == 'Entertainment':
                studentAverage.totalEntertainment += amount
            elif tagType == 'Shopping':
                studentAverage.totalShopping += amount
            elif tagType != 'Transfer':
                studentAverage.totalOther += amount

    studentAverage.food = studentAverage.totalFood / studentAverage.total
    studentAverage.education = studentAverage.totalEducation / studentAverage.total
    studentAverage.transport = studentAverage.totalTransport / studentAverage.total
    studentAverage.bills = studentAverage.totalBills / studentAverage.total
    studentAverage.entertainment = studentAverage.entertainment / studentAverage.total
    studentAverage.shopping = studentAverage.shopping / studentAverage.total
    studentAverage.other = studentAverage.other / studentAverage.total


@app.route('/processCustomer', methods=['POST'])
def parseCustomer():
    loggedInCustID = request.json.get('custId')
    currentCustomer = Customer()

    currentCustomer.balance = getCustomerAccountsBalance(loggedInCustID)
    currentCustomer.total = currentCustomer.balance
    transactions = json.loads(getTransactionHistory(loggedInCustID))
    for transaction in transactions.get('result'):
        amount = abs(transaction.get('currencyAmount'))
        currentCustomer.total += amount
        tagType = transaction.get('categoryTags')[0]
        if tagType == 'Food and Dining':
            currentCustomer.totalFood += amount
        elif tagType == 'Education':
            currentCustomer.totalEducation += amount
        elif tagType == 'Auto and Transport':
            currentCustomer.totalTransport += amount
        elif tagType == 'Bills and Utilities':
            currentCustomer.totalBills += amount
        elif tagType == 'Entertainment':
            currentCustomer.totalEntertainment += amount
        elif tagType == 'Shopping':
            currentCustomer.totalShopping += amount
        elif tagType != 'Transfer':
            currentCustomer.totalOther += amount

    currentCustomer.food = currentCustomer.totalFood / currentCustomer.total
    currentCustomer.education = currentCustomer.totalEducation / currentCustomer.total
    currentCustomer.transport = currentCustomer.totalTransport / currentCustomer.total
    currentCustomer.bills = currentCustomer.totalBills / currentCustomer.total
    currentCustomer.entertainment = currentCustomer.totalEntertainment / currentCustomer.total
    currentCustomer.shopping = currentCustomer.totalShopping / currentCustomer.total
    currentCustomer.other = currentCustomer.totalOther / currentCustomer.total

    return json.dumps({'adultAverage': adultAverage.__dict__, 'studentAverage': studentAverage.__dict__, 'currentCustomer': currentCustomer.__dict__})


@app.route('/transactionsByTags', methods=['POST'])
def transactionsByTags():
    custId = request.json.get('custId')
    tag = request.json.get('tag')

    transactions = json.loads(getTransactionHistory(custId))
    transactionsToReturn = []

    for transaction in transactions.get('result'):
        type = transaction.get('categoryTags')[0]
        if type == tag:
            transactionsToReturn.append(transaction)

    return json.dumps(transactionsToReturn)


if __name__ == '__main__':
    initialiseModel()
    print('model ready')
    app.run(host='0.0.0.0', port= 8080)
