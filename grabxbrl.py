from Capstone.database import db_session 
from Capstone.models import Registrant, Series, InvestorClass, Term, Registrant_Document, Registrant_Document_Term
import requests
import csv
import StringIO
import re
from sqlalchemy import select
from bs4 import BeautifulSoup
import sqlite3

# conn = sqlite3.connect('capstone.db')
# conn.text_factory = str

# html = {
# 	  	"Vanguard Emerging Markets Stock Index Fund" : "http://www.sec.gov/Archives/edgar/data/857489/000093247113005828/0000932471-13-005828-index.htm",
# 	  	"PIMCO Emerging Markets Full Spectrum Bond Fund" : "http://www.sec.gov/Archives/edgar/data/810893/000113322813000474/0001133228-13-000474-index.htm",
# 	  	"Schwab Fundamental Emerging Markets Large Company Index Fund" : "http://www.sec.gov/Archives/edgar/data/904333/000119312513107097/0001193125-13-107097-index.htm",
# 	  	"Fidelity Advisor Emerging Markets Fund" : "http://www.sec.gov/Archives/edgar/data/729218/000088019513000008/0000880195-13-000008-index.htm",
# 	  	"Templeton Emerging Markets Small Cap Fund" : "http://www.sec.gov/Archives/edgar/data/916488/000137949112000682/0001379491-12-000682-index.htm",
# 	  	"T. Rowe Price Institutional Emerging Markets Bond Fund" : "http://www.sec.gov/Archives/edgar/data/852254/000087183912000129/0000871839-12-000129-index.htm",
# 	  	"JPMorgan Total Emerging Markets Fund" : "http://www.sec.gov/Archives/edgar/data/1217286/000119312513114406/0001193125-13-114406-index.htm",
# 	  	"Oppenheimer Emerging Markets Debt Fund" : "http://www.sec.gov/Archives/edgar/data/1488175/000113322812002055/0001133228-12-002055-index.htm",
# 	  	"DFA Emerging Markets Core Equity Portfolio" : "http://www.sec.gov/Archives/edgar/data/355437/000119312513115506/0001193125-13-115506-index.htm",
# 	  	"MFS Emerging Markets Equity Fund" : "http://www.sec.gov/Archives/edgar/data/783740/000110465912070005/0001104659-12-070005-index.htm",
# 	  	"Nuveen Tradewinds Emerging Markets Fund" : "http://www.sec.gov/Archives/edgar/data/1041673/000119312512512683/0001193125-12-512683-index.htm",
# 	  	"Wells Fargo Advantage Emerging Markets Equity Fund" : "http://www.sec.gov/Archives/edgar/data/1081400/000108140013000079/0001081400-13-000079-index.htm",
# 	  	"Lord Abbett Emerging Markets Currency Fund" : "http://www.sec.gov/Archives/edgar/data/829901/000093041313003015/0000930413-13-003015-index.htm",
# 	  	"American Century Emerging Markets Fund" : "http://www.sec.gov/Archives/edgar/data/872825/000143774913004538/0001437749-13-004538-index.htm",
# 	  	"BlackRock Emerging Markets Fund" : "http://www.sec.gov/Archives/edgar/data/849402/000119312513112184/0001193125-13-112184-index.htm"
# 	   }

html = {
	"Vanguard Admiral Funds" : "http://www.sec.gov/Archives/edgar/data/891190/000093247113000028/0000932471-13-000028-index.htm",
	"Vanguard Institutional Index Funds" : "http://www.sec.gov/Archives/edgar/data/862084/000093247113006114/0000932471-13-006114-index.htm",
	"Vanguard FTSE All-World ex-US Index Fund" : "http://www.sec.gov/Archives/edgar/data/857489/000093247113005828/0000932471-13-005828-index.htm",
	"Vanguard Money Market Reserves" : "http://www.sec.gov/Archives/edgar/data/106830/000093247113000042/0000932471-13-000042-index.htm",
	"BlackRock China Fund" : "http://www.sec.gov/Archives/edgar/data/844779/000119312513062585/0001193125-13-062585-index.htm",
	# "BlackRock Funds" : "http://www.sec.gov/Archives/edgar/data/844779/000119312513064941/0001193125-13-064941-index.htm",
	"BlackRock Funds III" : "http://www.sec.gov/Archives/edgar/data/893818/000119312513228010/0001193125-13-228010-index.htm",
	"BlackRock Flexible Equity Fund" : "http://www.sec.gov/Archives/edgar/data/844779/000119312513062612/0001193125-13-062612-index.htm",
	"BlackRock Global SmallCap Fund" : "http://www.sec.gov/Archives/edgar/data/922457/000119312512467554/0001193125-12-467554-index.htm",
	"BlackRock Basic Value Fund" : "http://www.sec.gov/Archives/edgar/data/216557/000119312512467518/0001193125-12-467518-index.htm",
	"BlackRock Capital Appreciation Fund" : "http://www.sec.gov/Archives/edgar/data/887509/000119312513054783/0001193125-13-054783-index.htm",
	"BlackRock Focus Growth Fund" : "http://www.sec.gov/Archives/edgar/data/1097293/000119312513019037/0001193125-13-019037-index.htm",
	"Fidelity Advisor Series I" : "http://www.sec.gov/Archives/edgar/data/722574/000072257413000097/0000722574-13-000097-index.htm",
	"Fidelity Advisor Series VII" : "http://www.sec.gov/Archives/edgar/data/315700/000087846712000141/0000878467-12-000141-index.htm",
	"Schwab Capital Trust" : "http://www.sec.gov/Archives/edgar/data/869365/000119312513150741/0001193125-13-150741-index.htm",
	"Charles Schwab Family Of Funds" : "http://www.sec.gov/Archives/edgar/data/857156/000119312513222604/0001193125-13-222604-index.htm",
	"BlackRock Bond Index Fund" : "http://www.sec.gov/Archives/edgar/data/893818/000119312513225868/0001193125-13-225868-index.htm",
	"BlackRock Emerging Markets Fund" : "http://www.sec.gov/Archives/edgar/data/849402/000119312513112184/0001193125-13-112184-index.htm"
}

# filings = {
# 	  	"Vanguard Admiral Funds" : "/Users/jeffca/documents/blackrock/flask_base/forms/Vanguard Admiral Funds/Vanguard Admiral Funds.csv",
# 	  	"Vanguard Institutional Index Funds" : "/Users/jeffca/documents/blackrock/flask_base/forms/Vanguard Institutional Index Funds/Vanguard Institutional Index Funds.csv",
# 	  	"Vanguard Money Market Reserves" : "/Users/jeffca/documents/blackrock/flask_base/forms/Vanguard Money Market Reserves/Vanguard Money Market Reserves.csv",
# 		"Vanguard FTSE All-World ex-US Index Fund" : "/Users/jeffca/documents/blackrock/flask_base/forms/Vanguard FTSE All-World ex-US Index Fund/Vanguard FTSE All-World ex-US Index Fund.csv",
# 	 	# "BlackRock Funds" : "/Users/jeffca/documents/blackrock/flask_base/forms/BlackRock Funds/BlackRock Funds.csv",
# 	 	"BlackRock China Fund" : "/Users/jeffca/documents/blackrock/flask_base/forms/BlackRock China Fund/BlackRock China Fund.csv",
# 	 	"Fidelity Advisor Series VII" : "/Users/jeffca/documents/blackrock/flask_base/forms/Fidelity Advisor Series VII/Fidelity Advisor Series VII.csv",
# 		"Fidelity Advisor Series I" : "/Users/jeffca/documents/blackrock/flask_base/forms/Fidelity Advisor Series I/Fidelity Advisor Series I.csv",
# 	 	"BlackRock Flexible Equity Fund" : "/Users/jeffca/documents/blackrock/flask_base/forms/BlackRock Flexible Equity Fund/BlackRock Flexible Equity Fund.csv",
# 	 	"BlackRock Global SmallCap Fund" : "/Users/jeffca/documents/blackrock/flask_base/forms/BlackRock Global SmallCap Fund/BlackRock Global SmallCap Fund.csv",
# 	 	"Charles Schwab Family Of Funds" : "/Users/jeffca/documents/blackrock/flask_base/forms/Charles Schwab Family Of Funds/Charles Schwab Family Of Funds.csv",
# 	 	"Schwab Capital Trust" : "/Users/jeffca/documents/blackrock/flask_base/forms/Schwab Capital Trust/Schwab Capital Trust.csv",
# 	 	"BlackRock Capital Appreciation Fund" : "/Users/jeffca/documents/blackrock/flask_base/forms/BlackRock Capital Appreciation Fund/BlackRock Capital Appreciation Fund.csv",
# 	 	"BlackRock Focus Growth Fund" : "/Users/jeffca/documents/blackrock/flask_base/forms/BlackRock Focus Growth Fund/BlackRock Focus Growth Fund.csv"
# 	 }

filings = {
	"BlackRock Bond Index Fund" : "/Users/jeffca/documents/blackrock/flask_base/forms/BlackRock Bond Index Fund/BlackRock Bond Index Fund.csv",
	"BlackRock Emerging Markets Fund" : "/Users/jeffca/documents/blackrock/flask_base/forms/BlackRock Emerging Markets Fund/BlackRock Emerging Markets Fund.csv"
}

for filing in filings.keys():
	reg = Registrant()
	doc = Registrant_Document()
	db_session.add(reg)
	db_session.add(doc)
	db_session.commit()
	doc.Registrant = reg
	# url = "http://localhost:8080/rest/xbrl/view?file=" + filings[filing] + "&view=facts&media=csv"
	# data = requests.get(url).text
	# f = StringIO.StringIO(data)
	f = open("forms/" + filing + "/" + filing + '.csv' , 'r')
	reader = csv.reader(f, delimiter=',')	
	r2 = requests.get(html[filing])
	print 'parsing ' + html[filing]
	doc.url = html[filing]
	soup = BeautifulSoup(r2.text)
	for row in reader:
		if row[0] == 'Label':
			continue
		if row[0] == 'Registrant Name' or 'Effective' in row[0] or 'Objective' in row[0] or 'objective' in row[0] or 'Narrative' in row[0] or '[Text Block]' in row[0] or 'Annual Return' in row[0] or '200' in row[0] or 'Inception' in row[0] or 'Fee' in row[0] or 'Expense' in row[0]:
			rdt = Registrant_Document_Term()
			context = row[1]
			series_match = re.search(r"S\d{9}", context)
			fund_match = re.search(r"C\d{9}", context)	
			if series_match:
				seriesInXLS = series_match.group()
				# seriesInfo = soup.find("table", { "class" : "tableSeries" }).find("td", {"class" : "seriesName"}).find("a")
				htmlSeries = soup.find("table", { "class" : "tableSeries" }).find_all("td", {"class" : "seriesName"})
				# print seriesInfo.text + ' is the a tag in the HTML'
				if Series.query.filter(Series.SECid == seriesInXLS).count() == 0:
					s = Series()				
					s.SECid = seriesInXLS
					s.Registrant_Document = doc
					for ser in htmlSeries:
						if ser.a.text == seriesInXLS: 
							parent = ser.parent
							title = parent.find_all("td")
							s.Name = title[2].text.title()
					db_session.add(s)
					db_session.commit()
					rdt.Series = s
				else:
					s = Series.query.filter(Series.SECid == seriesInXLS).first()
					rdt.Series = s 
			if fund_match:
				fundInXLS = fund_match.group()
				seriesInXLS = series_match.group()
				htmlSeries = soup.find("table", { "class" : "tableSeries" }).find_all("tr", {"class" : "contractRow"})
				if InvestorClass.query.filter(InvestorClass.SECid == fundInXLS).count() == 0:
					ic = InvestorClass()
					ic.Series = Series.query.filter(Series.SECid == seriesInXLS).first()
					ic.SECid = fundInXLS
					for ser in htmlSeries:
						if ser.a.text == fundInXLS:						
							c = ser.find_all("td")						
							ic.Class = c[2].text
							ic.Ticker = c[3].text
					db_session.add(ic)
					db_session.commit()
					rdt.InvestorClass = ic
				else:
					ic = InvestorClass.query.filter(InvestorClass.SECid == fundInXLS).first()
					rdt.InvestorClass = ic
			if Term.query.filter(Term.Name == row[0]).count() == 0:
				t = Term()
				t.Name = row[0]
				db_session.add(t)
				db_session.commit()
				print 'added a new term: ' + row[0]
			t = Term.query.filter(Term.Name == row[0]).first()
			if row[0] == 'Investment objective' or row[0] == 'Objective, Primary [Text Block]':
				t = Term.query.filter(Term.id == 11).first()
			if row[0] == 'StrategyNarrative':
				t = Term.query.filter(Term.id == 13).first()
			if row[0] == 'Risk Narrative':
				t = Term.query.filter(Term.id == 29).first()
			if row[0] == '12b-1 Distribution Fee':
				t = Term.query.filter(Term.id == 118).first()
			if row[0] == 'Expenses (as a percentage of Assets)':
				t = Term.query.filter(Term.id == 261).first()
			if row[0] == 'Other Expenses (as a percentage of Assets):':
				t = Term.query.filter(Term.id == 119).first()
			if row[0] == 'Since Inception Date' or row[0] == 'Annual Return Inception Date':
				t = Term.query.filter(Term.id == 152).first()
			if '200' in row[0]:
				if '2002' in row[0]:
					t = Term.query.filter(Term.id == 277).first()
				elif '2003' in row[0]:
					t = Term.query.filter(Term.id == 130).first()
				elif '2004' in row[0]:
					t = Term.query.filter(Term.id == 131).first()
				elif '2005' in row[0]:
					t = Term.query.filter(Term.id == 132).first()
				elif '2006' in row[0]:
					t = Term.query.filter(Term.id == 133).first()
				elif '2007' in row[0]:
					t = Term.query.filter(Term.id == 134).first()
				elif '2008' in row[0]:
					t = Term.query.filter(Term.id == 135).first()
				elif '2009' in row[0]:
					t = Term.query.filter(Term.id == 136).first()
				elif '2010' in row[0]:
					t = Term.query.filter(Term.id == 137).first()
				elif '2011' in row[0]:
					t = Term.query.filter(Term.id == 90).first()
				elif '2012' in row[0]:
					t = Term.query.filter(Term.id == 138).first()
			rdt.Term = t
			rdt.Registrant_Document = doc
			rdt.ContextRef = row[1]
			rdt.UnitRef = row[2]
			rdt.Decimal = row[3]
			rdt.Precision = row[4]
			rdt.Language = row[5]
			rdt.Value = row[6].decode('utf-8')
			db_session.add(rdt)
			db_session.commit()
	effectiveDate = Registrant_Document_Term.query.filter(Registrant_Document_Term.TermID == 4, Registrant_Document_Term.Registrant_Document == doc).first()
	doc.EffectiveDate = effectiveDate.Value
	db_session.commit()

