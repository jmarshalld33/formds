from Capstone import app
from functools import wraps
from flask import Flask, render_template, request, Response, jsonify
from Capstone.database import db_session 
from Capstone.models import *
import datetime 
from datetime import timedelta
from sqlalchemy import or_
import locale
from collections import OrderedDict

locale.setlocale( locale.LC_ALL, '' )

def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    return username == 'blk' and password == '4747'

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated



@app.route('/logintest')
def login():
	return render_template('logintest.html')
	
@app.route('/')
@requires_auth
def home():	
	return render_template('home.html')

@app.route('/about')
@requires_auth
def about():
	return render_template('about.html')

@app.route('/formd', methods=["POST", "GET"])
@requires_auth
def formd():
	dates = {}
	dates["today"] = datetime.datetime.now()
	dates["lastweek"] = datetime.datetime.now() - timedelta(days = 7)
	dates["lastmonth"] = datetime.datetime.now() - timedelta(days = 31)
	if request.method == 'POST':
		date = request.form['date_select'][0:10]
		if request.form['offering_select'] != 'Indefinite' and request.form['offering_select'] != 'all':
			(offeringLowerBound, offeringHigherBound) = request.form['offering_select'].split('-')
		amended = request.form['new_amended_select']
		investmentType = request.form['investment_type_select']
		tier = request.form['tier_select']
		sold = request.form['sold_select']
		city = request.form['city_select']
		
		formds = FormD.query.all()
		if request.form['tier_select'] == 'all':
			if request.form['investment_type_select'] != 'all':
				if request.form['offering_select'] != 'Indefinite' and request.form['offering_select'] != 'all':
					if amended == 'new':
						formds = FormD.query.filter(FormD.SubmissionDate >= date, FormD.TotalOfferingAmount >= offeringLowerBound,
						FormD.TotalOfferingAmount <= offeringHigherBound, FormD.Amended == 0, FormD.InvestmentFundType == investmentType)
					elif amended == 'amended':
						formds = FormD.query.filter(FormD.SubmissionDate >= date, FormD.TotalOfferingAmount >= offeringLowerBound,
						FormD.TotalOfferingAmount <= offeringHigherBound, FormD.Amended == 1, FormD.InvestmentFundType == investmentType)
					else:
						formds = FormD.query.filter(FormD.SubmissionDate >= date, FormD.TotalOfferingAmount >= offeringLowerBound,
						FormD.TotalOfferingAmount <= offeringHigherBound, FormD.InvestmentFundType == investmentType)
				elif request.form['offering_select'] == 'Indefinite':
					if amended == 'new':
						formds = FormD.query.filter(FormD.SubmissionDate >= date, FormD.IsTotalOfferingAmountIndefinite == 1, FormD.Amended == 0, FormD.InvestmentFundType == investmentType)
					elif amended == 'amended':
						formds = FormD.query.filter(FormD.SubmissionDate >= date, FormD.IsTotalOfferingAmountIndefinite == 1, FormD.Amended == 1, FormD.InvestmentFundType == investmentType)
					else:
						formds = FormD.query.filter(FormD.SubmissionDate >= date, FormD.IsTotalOfferingAmountIndefinite == 1, FormD.InvestmentFundType == investmentType)
				else:
					if amended == 'new':
						formds = FormD.query.filter(FormD.SubmissionDate >= date, FormD.Amended == 0, FormD.InvestmentFundType == investmentType)
					elif amended == 'amended':
						formds = FormD.query.filter(FormD.SubmissionDate >= date, FormD.Amended == 1, FormD.InvestmentFundType == investmentType)
					else:
						formds = FormD.query.filter(FormD.SubmissionDate >= date, FormD.InvestmentFundType == investmentType)
			else:
				if request.form['offering_select'] != 'Indefinite' and request.form['offering_select'] != 'all':
					if amended == 'new':
						formds = FormD.query.filter(FormD.SubmissionDate >= date, FormD.TotalOfferingAmount >= offeringLowerBound,
						FormD.TotalOfferingAmount <= offeringHigherBound, FormD.Amended == 0)
					elif amended == 'amended':
						formds = FormD.query.filter(FormD.SubmissionDate >= date, FormD.TotalOfferingAmount >= offeringLowerBound,
						FormD.TotalOfferingAmount <= offeringHigherBound, FormD.Amended == 1)
					else:
						formds = FormD.query.filter(FormD.SubmissionDate >= date, FormD.TotalOfferingAmount >= offeringLowerBound,
						FormD.TotalOfferingAmount <= offeringHigherBound)
				elif request.form['offering_select'] == 'Indefinite':
					if amended == 'new':
						formds = FormD.query.filter(FormD.SubmissionDate >= date, FormD.IsTotalOfferingAmountIndefinite == 1, FormD.Amended == 0)
					elif amended == 'amended':
						formds = FormD.query.filter(FormD.SubmissionDate >= date, FormD.IsTotalOfferingAmountIndefinite == 1, FormD.Amended == 1)
					else:
						formds = FormD.query.filter(FormD.SubmissionDate >= date, FormD.IsTotalOfferingAmountIndefinite == 1)
				else:
					if amended == 'new':
						formds = FormD.query.filter(FormD.SubmissionDate >= date, FormD.Amended == 0)
					elif amended == 'amended':
						formds = FormD.query.filter(FormD.SubmissionDate >= date, FormD.Amended == 1)
					else:
						formds = FormD.query.filter(FormD.SubmissionDate >= date)
		else:			 
			if request.form['investment_type_select'] != 'all':
				if request.form['offering_select'] != 'Indefinite' and request.form['offering_select'] != 'all':
					if amended == 'new':
						formds = FormD.query.filter(FormD.SubmissionDate >= date, FormD.TotalOfferingAmount >= offeringLowerBound,
						FormD.TotalOfferingAmount <= offeringHigherBound, FormD.Amended == 0, FormD.InvestmentFundType == investmentType, FormD.IssuerID.in_([iss.id for iss in Issuer.query.filter(Issuer.TierID == tier)]))
					elif amended == 'amended':
						formds = FormD.query.filter(FormD.SubmissionDate >= date, FormD.TotalOfferingAmount >= offeringLowerBound,
						FormD.TotalOfferingAmount <= offeringHigherBound, FormD.Amended == 1, FormD.InvestmentFundType == investmentType, FormD.IssuerID.in_([iss.id for iss in Issuer.query.filter(Issuer.TierID == tier)]))
					else:
						formds = FormD.query.filter(FormD.SubmissionDate >= date, FormD.TotalOfferingAmount >= offeringLowerBound,
						FormD.TotalOfferingAmount <= offeringHigherBound, FormD.InvestmentFundType == investmentType, FormD.IssuerID.in_([iss.id for iss in Issuer.query.filter(Issuer.TierID == tier)]))
				elif request.form['offering_select'] == 'Indefinite':
					if amended == 'new':
						formds = FormD.query.filter(FormD.SubmissionDate >= date, FormD.IsTotalOfferingAmountIndefinite == 1, FormD.Amended == 0, 
						FormD.InvestmentFundType == investmentType, FormD.IssuerID.in_([iss.id for iss in Issuer.query.filter(Issuer.TierID == tier)]))
					elif amended == 'amended':
						formds = FormD.query.filter(FormD.SubmissionDate >= date, FormD.IsTotalOfferingAmountIndefinite == 1, FormD.Amended == 1,
						FormD.InvestmentFundType == investmentType, FormD.IssuerID.in_([iss.id for iss in Issuer.query.filter(Issuer.TierID == tier)]))
					else:
						formds = FormD.query.filter(FormD.SubmissionDate >= date, FormD.IsTotalOfferingAmountIndefinite == 1, 
						FormD.InvestmentFundType == investmentType, FormD.IssuerID.in_([iss.id for iss in Issuer.query.filter(Issuer.TierID == tier)]))
				else:
					if amended == 'new':
						formds = FormD.query.filter(FormD.SubmissionDate >= date, FormD.Amended == 0, 
						FormD.InvestmentFundType == investmentType, FormD.IssuerID.in_([iss.id for iss in Issuer.query.filter(Issuer.TierID == tier)]))
					elif amended == 'amended':
						formds = FormD.query.filter(FormD.SubmissionDate >= date, FormD.Amended == 1,
						FormD.InvestmentFundType == investmentType, FormD.IssuerID.in_([iss.id for iss in Issuer.query.filter(Issuer.TierID == tier)]))
					else:
						formds = FormD.query.filter(FormD.SubmissionDate >= date, 
						FormD.InvestmentFundType == investmentType, FormD.IssuerID.in_([iss.id for iss in Issuer.query.filter(Issuer.TierID == tier)]))
			else:
				if request.form['offering_select'] != 'Indefinite' and request.form['offering_select'] != 'all':
					if amended == 'new':
						formds = FormD.query.filter(FormD.SubmissionDate >= date, FormD.TotalOfferingAmount >= offeringLowerBound,
						FormD.TotalOfferingAmount <= offeringHigherBound, FormD.Amended == 0, FormD.InvestmentFundType == investmentType, FormD.IssuerID.in_([iss.id for iss in Issuer.query.filter(Issuer.TierID == tier)]))
					elif amended == 'amended':
						formds = FormD.query.filter(FormD.SubmissionDate >= date, FormD.TotalOfferingAmount >= offeringLowerBound,
						FormD.TotalOfferingAmount <= offeringHigherBound, FormD.Amended == 1, FormD.InvestmentFundType == investmentType,  FormD.IssuerID.in_([iss.id for iss in Issuer.query.filter(Issuer.TierID == tier)]))
					else:
						formds = FormD.query.filter(FormD.SubmissionDate >= date, FormD.TotalOfferingAmount >= offeringLowerBound,
						FormD.TotalOfferingAmount <= offeringHigherBound, FormD.InvestmentFundType == investmentType, FormD.IssuerID.in_([iss.id for iss in Issuer.query.filter(Issuer.TierID == tier)]))
				elif request.form['offering_select'] == 'Indefinite':
					if amended == 'new':
						formds = FormD.query.filter(FormD.SubmissionDate >= date, FormD.IsTotalOfferingAmountIndefinite == 1, FormD.Amended == 0,
						FormD.InvestmentFundType == investmentType, FormD.IssuerID.in_([iss.id for iss in Issuer.query.filter(Issuer.TierID == tier)]))
					elif amended == 'amended':
						formds = FormD.query.filter(FormD.SubmissionDate >= date, FormD.IsTotalOfferingAmountIndefinite == 1, FormD.Amended == 1,
						FormD.InvestmentFundType == investmentType, FormD.IssuerID.in_([iss.id for iss in Issuer.query.filter(Issuer.TierID == tier)]))
					else:
						formds = FormD.query.filter(FormD.SubmissionDate >= date, FormD.IsTotalOfferingAmountIndefinite == 1, FormD.InvestmentFundType == investmentType, FormD.IssuerID.in_([iss.id for iss in Issuer.query.filter(Issuer.TierID == tier)]))
				else:
					if amended == 'new':
						formds = FormD.query.filter(FormD.SubmissionDate >= date, FormD.Amended == 0,
						FormD.InvestmentFundType == investmentType, FormD.IssuerID.in_([iss.id for iss in Issuer.query.filter(Issuer.TierID == tier)]))
					elif amended == 'amended':
						formds = FormD.query.filter(FormD.SubmissionDate >= date, FormD.Amended == 1,
						FormD.InvestmentFundType == investmentType, FormD.IssuerID.in_([iss.id for iss in Issuer.query.filter(Issuer.TierID == tier)]))
					else:
						formds = FormD.query.filter(FormD.SubmissionDate >= date, FormD.InvestmentFundType == investmentType, FormD.IssuerID.in_([iss.id for iss in Issuer.query.filter(Issuer.TierID == tier)]))
		if sold != '':
 			formds = FormD.query.filter(FormD.TotalAmountSold >= sold)
 		if city != '':
 			formds = FormD.query.filter(FormD.IssuerID.in_([iss.id for iss in Issuer.query.filter(Issuer.City == city)]))	

		for formd in formds:
			if formd.IsTotalOfferingAmountIndefinite == 0:
				formd.TotalOfferingAmount = locale.currency(formd.TotalOfferingAmount, grouping=True)
				formd.TotalRemaining = locale.currency(formd.TotalRemaining, grouping=True)
			formd.TotalAmountSold = locale.currency(formd.TotalAmountSold, grouping=True)
			formd.SubmissionDate = formd.SubmissionDate.strftime("%b %d, %Y")
		formds = formds.order_by(FormD.SubmissionDate.desc())
		return render_template('formd.html', dates = dates, formds = formds)
	else:
		return render_template('formd.html', dates = dates)

@app.route('/form497', methods=["POST", "GET"])
@requires_auth
def form497():
	funds = Series.query.all()
	fundNames = []
	for f in funds:
		fundNames.append(f.Name)
	if request.method == 'POST':
		fundName = request.form['fund_select']
		series = Series.query.filter(Series.Name == fundName).first()
		if series != None:			
			investorClasses = InvestorClass.query.filter(InvestorClass.Series == series)
			fundFees = {}
		 	fundExpenses = {}
		 	returns = {}
			for i in investorClasses:
				vals = []
				a = Registrant_Document_Term.query.filter(Registrant_Document_Term.TermID == 168, Registrant_Document_Term.InvestorClass == i).first()
				d = Registrant_Document_Term.query.filter(Registrant_Document_Term.TermID == 118, Registrant_Document_Term.InvestorClass == i).first()
				fwaiver = Registrant_Document_Term.query.filter(Registrant_Document_Term.TermID == 271, Registrant_Document_Term.InvestorClass == i).first()
				mf = Registrant_Document_Term.query.filter(Registrant_Document_Term.TermID == 265, Registrant_Document_Term.InvestorClass == i).first()
				rf = Registrant_Document_Term.query.filter(Registrant_Document_Term.TermID == 239, Registrant_Document_Term.InvestorClass == i).first()
				if a != None:
					vals.append(a.Value)
				else:
					vals.append('n/a')
				if d != None:
					vals.append(d.Value)
				else:
					vals.append('n/a')
				if fwaiver != None:
					vals.append(fwaiver.Value)
				else:
					vals.append('n/a')				
				if mf != None:
					vals.append(mf.Value)
				else:
					vals.append('n/a')								
				if rf != None:
					vals.append(rf.Value)
				else:
					vals.append('n/a')									
				fundFees[i] = vals
				expenseVals = []
				e = Registrant_Document_Term.query.filter(Registrant_Document_Term.TermID == 261, Registrant_Document_Term.InvestorClass == i).first()
				me = Registrant_Document_Term.query.filter(Registrant_Document_Term.TermID == 247, Registrant_Document_Term.InvestorClass == i).first()
				oe = Registrant_Document_Term.query.filter(Registrant_Document_Term.TermID == 119, Registrant_Document_Term.InvestorClass == i).first()
				te = Registrant_Document_Term.query.filter(Registrant_Document_Term.TermID == 120, Registrant_Document_Term.InvestorClass == i).first()
				if e != None:
					expenseVals.append(e.Value)
				else:
					expenseVals.append('n/a')
				if me != None:
					expenseVals.append(me.Value)
				else:
					expenseVals.append('n/a')
				if oe != None:
					expenseVals.append(oe.Value)
				else:
					expenseVals.append('n/a')			
				if te != None:
					expenseVals.append(te.Value)
				else:
					expenseVals.append('n/a')			
				fundExpenses[i] = expenseVals
				annualReturns = Registrant_Document_Term.query.filter(Registrant_Document_Term.TermID.in_([277, 130, 131, 132, 133, 134, 135, 136, 137, 90, 138]), Registrant_Document_Term.InvestorClass == i).all()		
				yrs = []
				temps = {}
				for annualReturn in annualReturns:
					temp = annualReturn.Value
					termName = Term.query.filter(Term.id == annualReturn.TermID).first()
					yr = termName.Name[len(termName.Name) - 4:]
					yrs.append(yr)
					temps[yr] = temp
				yrs = sorted(yrs)
				orderedReturns = OrderedDict()
				for y in yrs:
					orderedReturns[y] = temps[y]
				returns[i.Class] = orderedReturns
			inceptionDate = Registrant_Document_Term.query.filter(Registrant_Document_Term.TermID == 152, Registrant_Document_Term.Series == series).first()
			if inceptionDate != None:
				inceptionDate = inceptionDate.Value
				inceptionMonthDay = inceptionDate[5:]
				inceptionYear = inceptionDate[:4]
				inceptionDate = inceptionMonthDay + '-' + inceptionYear
			else:
				inceptionDate = ''	
			strat = Registrant_Document_Term.query.filter(Registrant_Document_Term.TermID == 13, Registrant_Document_Term.Series == series).first()
			strat = strat.Value
			strat = strat.replace("\"", "&quot;")
			risk = Registrant_Document_Term.query.filter(Registrant_Document_Term.TermID == 29, Registrant_Document_Term.Series == series).first()
			risk = risk.Value
			risk = risk.replace("\"", "&quot;")
			riskIntro = risk[:205]
			introStrat = strat.split('</p>')
			introStrat = introStrat[0]
			introStrat = introStrat[:524]
			obj = Registrant_Document_Term.query.filter(Registrant_Document_Term.TermID.in_([11, 98]), Registrant_Document_Term.Series == series).first() 
			obj = obj.Value
			exp = Registrant_Document_Term.query.filter(Registrant_Document_Term.TermID == 33, Registrant_Document_Term.Series == series).first()
			performance = Registrant_Document_Term.query.filter(Registrant_Document_Term.TermID == 32, Registrant_Document_Term.Series == series).first()
			returnSinceInception = Registrant_Document_Term.query.filter(Registrant_Document_Term.TermID == 151, Registrant_Document_Term.Series == series).first()
			if returnSinceInception != None:
				returnSinceInception = returnSinceInception.Value
			else:
				returnSinceInception = ''
			doc = Registrant_Document.query.filter(Registrant_Document.id == series.Registrant_DocumentID).first()
			effectiveDate = doc.EffectiveDate
			effectiveDateYear = effectiveDate[:4]
			effectiveDateMonthDay = effectiveDate[5:]
			effectiveDate = effectiveDateMonthDay + '-' + effectiveDateYear
			return render_template('form497.html', strat = strat, introStrat = introStrat, fundName = fundName, obj = obj, exp = exp, performance=performance,
									fundFees=fundFees, investorClasses=investorClasses, fundExpenses=fundExpenses, risk=risk, riskIntro=riskIntro, returns=returns,
									fundNames=fundNames, inceptionDate=inceptionDate, returnSinceInception=returnSinceInception, effectiveDate =effectiveDate)
		else:
			noSeries = 1
			return render_template('form497.html', noSeries=noSeries)
	else:
		return render_template('form497.html', fundNames=fundNames)


# @app.route('/mutualfundapi/<name>')
# def returnMutualFundFromCompany(name):
# 	funds = InvestorClass.query.filter(InvestorClass.Series == name)
# 	f = []
# 	for fund in funds:
# 		f.append({ 'name':fund.Name, 'classType':fund.Class })
# 	return jsonify(results=f)

# @app.route('/seriesapi/<name>')
# def returnSeriesFromCompany(name):
# 	serieses = Registrant_Document_Term.query.filter(Series.Name == name)


@app.route('/feedback')
def feedback():
	return render_template('feedback.html')
