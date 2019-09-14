# install the requests package using 'pip3 install requests'
import requests
import json

apiKey = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJDQlAiLCJ0ZWFtX2lkIjoiMmYwZDNmZDctMThmMS0zYjdkLWI4ZjEtYmJmNGQxMGNjN2UwIiwiZXhwIjo5MjIzMzcyMDM2ODU0Nzc1LCJhcHBfaWQiOiI2MzYxNjM4NS01YjViLTRmYWYtOWYyNy0zNGU0MjZhYmJkODcifQ.1I1b3Ic7QfbXWVz0Fo1UVDd2gBTMucRJFbKWhW6DYpE'

class Customer:
  def __init__(self, balance = 0, education = 0, transport = 0, bills = 0, entertainment = 0, food = 0, income = 0,
               loans = 0, shopping = 0, other = 0, totalEducation = 0, totalTransport = 0, totalBills = 0,
               totalEntertainment = 0, totalFood = 0, totalIncome = 0, totalLoans = 0, totalShopping = 0, totalOther = 0):
    self.balance = balance

    self.education = education
    self.transport = transport
    self.bills = bills
    self.entertainment = entertainment
    self.food = food
    self.income = income
    self.loans = loans
    self.shopping = shopping
    self.other = other

    self.totalEducation = totalEducation
    self.totalTransport = totalTransport
    self.totalBills = totalBills
    self.totalEntertainment = totalEntertainment
    self.totalFood = totalFood
    self.totalIncome = totalIncome
    self.totalLoans = totalLoans
    self.totalShopping = totalShopping
    self.totalOther = totalOther

class RatioAverages:
    def __init__(self, midHigh, lowMid):
        self.midHigh = midHigh
        self.lowMid = lowMid

class YoungAdultAverage():
    def __init__(self, balance = 0, education = 0, transport = 0, bills = 0, entertainment = 0, food = 0, income = 0,
               loans = 0, shopping = 0, other = 0, totalEducation = 0, totalTransport = 0, totalBills = 0,
               totalEntertainment = 0, totalFood = 0, totalIncome = 0, totalLoans = 0, totalShopping = 0, totalOther = 0):
        self.balance = balance

        self.education = education
        self.transport = transport
        self.bills = bills
        self.entertainment = entertainment
        self.food = food
        self.income = income
        self.loans = loans
        self.shopping = shopping
        self.other = other

        self.totalEducation = totalEducation
        self.totalTransport = totalTransport
        self.totalBills = totalBills
        self.totalEntertainment = totalEntertainment
        self.totalFood = totalFood
        self.totalIncome = totalIncome
        self.totalLoans = totalLoans
        self.totalShopping = totalShopping
        self.totalOther = totalOther

    def __repr__(self):
        return print(self.balance, self.totalEducation, self.totalTransport, self.totalBills, self.totalEntertainment, self.totalFood, self.totalIncome, self.totalLoans, self.totalShopping, self.totalOther)

    def __str__(self):
        return print(self.balance, self.totalEducation, self.totalTransport, self.totalBills, self.totalEntertainment, self.totalFood, self.totalIncome, self.totalLoans, self.totalShopping, self.totalOther)

class StudentAverage():
    def __init__(self, balance = 0, education = 0, transport = 0, bills = 0, entertainment = 0, food = 0, income = 0,
               loans = 0, shopping = 0, other = 0, totalEducation = 0, totalTransport = 0, totalBills = 0,
               totalEntertainment = 0, totalFood = 0, totalIncome = 0, totalLoans = 0, totalShopping = 0, totalOther = 0):
        self.balance = balance

        self.education = education
        self.transport = transport
        self.bills = bills
        self.entertainment = entertainment
        self.food = food
        self.income = income
        self.loans = loans
        self.shopping = shopping
        self.other = other

        self.totalEducation = totalEducation
        self.totalTransport = totalTransport
        self.totalBills = totalBills
        self.totalEntertainment = totalEntertainment
        self.totalFood = totalFood
        self.totalIncome = totalIncome
        self.totalLoans = totalLoans
        self.totalShopping = totalShopping
        self.totalOther = totalOther

    def __repr__(self):
        return print(self.balance, self.totalEducation, self.totalTransport, self.totalBills, self.totalEntertainment, self.totalFood, self.totalIncome, self.totalLoans, self.totalShopping, self.totalOther)

    def __str__(self):
        return print(self.balance, self.totalEducation, self.totalTransport, self.totalBills, self.totalEntertainment, self.totalFood, self.totalIncome, self.totalLoans, self.totalShopping, self.totalOther)


youngAdultCustomers = []
studentCustomers = []

def getCustomerAccountsBalance(custId):
    response = requests.get('https://api.td-davinci.com/api/simulants/' + custId + '/simulatedaccounts',
    headers = { 'Authorization': apiKey })
    accounts = json.loads(response.text).get('result').get('bankAccounts')
    credits = json.loads(response.text).get('result').get('creditCardAccounts')
    balance = 0
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

def getTransactionByTag(custId, tag):
    response = requests.post('https://api.td-davinci.com/api/simulants/' + custId + '/simulatedtransactions/search',
                             headers={'Authorization': apiKey},
                             json={'continuationToken': '', 'searchCriteria': [
                                   {'key': 'originationDateTime', 'operation': '>', 'value': '2019-09'},
                                   {'key': 'tags', 'operation': '=', 'value': tag}]})
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
    while len(virtualCustomers)>0 and i < 2:
        for virtualCustomer in virtualCustomers.get('result').get('customers'):
            if virtualCustomer.get('age') < 30 and virtualCustomer.get('age') > 23:
                youngAdultCustomers.append(virtualCustomer)
            elif virtualCustomer.get('age') <= 23 and virtualCustomer.get('age') > 17:
                studentCustomers.append(virtualCustomer)

        virtualCustomers = json.loads(rawDataCall(virtualCustomers.get('result').get('continuationToken')))
        i+=1


def parseCustomers(loggedInCustID):
    getAllCustomers()

    print(len(youngAdultCustomers))
    print(len(studentCustomers))

    adultAverage = YoungAdultAverage();

    for adult in youngAdultCustomers:
        print(adult)
        balance = getCustomerAccountsBalance(adult.get('id'))
        transactions = json.loads(getTransactionHistory(adult.get('id')))
        for transaction in transactions.get('result'):
            amount = transaction.get('currencyAmount')
            type = transaction.get('categoryTags')[0]
            if type == 'Food and Dining':
                adultAverage.totalFood += amount
            elif type == 'Education':
                adultAverage.totalEducation += amount
            elif type == 'Auto and Transport':
                adultAverage.totalTransport += amount
            elif type == 'Bills and Utilities':
                adultAverage.totalBills += amount
            elif type == 'Entertainment':
                adultAverage.totalEntertainment += amount
            elif type == 'Shopping':
                adultAverage.totalShopping += amount
            else:
                adultAverage.totalOther += amount
        adultAverage.balance += balance

    studentAverage = StudentAverage();

    for student in studentCustomers:
        print(student)
        balance = getCustomerAccountsBalance(student.get('id'))
        transactions = json.loads(getTransactionHistory(student.get('id')))
        for transaction in transactions.get('result'):
            amount = transaction.get('currencyAmount')
            type = transaction.get('categoryTags')[0]
            if type == 'Food and Dining':
                studentAverage.totalFood += amount
            elif type == 'Education':
                studentAverage.totalEducation += amount
            elif type == 'Auto and Transport':
                studentAverage.totalTransport += amount
            elif type == 'Bills and Utilities':
                studentAverage.totalBills += amount
            elif type == 'Entertainment':
                studentAverage.totalEntertainment += amount
            elif type == 'Shopping':
                studentAverage.totalShopping += amount
            else:
                studentAverage.totalOther += amount
        studentAverage.balance += balance

    print(adultAverage, studentAverage)

def transactionsByTags(custId, tag):
    print(getTransactionByTag(custId, tag))
    return getTransactionByTag(custId, tag)
