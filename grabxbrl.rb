require 'rubygems' # you need this when xbrlware is installed as gem
require 'edgar'
require 'xbrlware'
require 'open-uri'
require 'nokogiri'
require 'sequel'


# DB = Sequel.connect('sqlite://capstone.db') 

forms = {
	"PIMCO ETF Trust" => "http://www.sec.gov/Archives/edgar/data/1450011/000113322812002191/0001133228-12-002191-index.htm",
	"Vanguard Admiral Funds" => "http://www.sec.gov/Archives/edgar/data/891190/000093247113000028/0000932471-13-000028-index.htm",
	"Vanguard Institutional Index Funds" => "http://www.sec.gov/Archives/edgar/data/862084/000093247113006114/0000932471-13-006114-index.htm",
	"Vanguard FTSE All-World ex-US Index Fund" => "http://www.sec.gov/Archives/edgar/data/857489/000093247113005828/0000932471-13-005828-index.htm",
	"Vanguard Money Market Reserves" => "http://www.sec.gov/Archives/edgar/data/106830/000093247113000042/0000932471-13-000042-index.htm",
	"BlackRock China Fund" => "http://www.sec.gov/Archives/edgar/data/844779/000119312513062585/0001193125-13-062585-index.htm",
	"BlackRock Funds" => "http://www.sec.gov/Archives/edgar/data/844779/000119312513064941/0001193125-13-064941-index.htm",
	"BlackRock Funds II" => "http://www.sec.gov/Archives/edgar/data/1398078/000119312513059237/0001193125-13-059237-index.htm",	
	"Fidelity Advisor Series I" => "http://www.sec.gov/Archives/edgar/data/722574/000072257413000097/0000722574-13-000097-index.htm",
	"Fidelity Advisor Series VII" => "http://www.sec.gov/Archives/edgar/data/315700/000087846712000141/0000878467-12-000141-index.htm"
 }



def downloadMutualFund(url, name)
	dl=Edgar::HTMLFeedDownloader.new()
	download_dir='forms/' + name
	dl.download(url, download_dir)
end

downloadMutualFund("http://www.sec.gov/Archives/edgar/data/849402/000119312513112184/0001193125-13-112184-index.htm", "BlackRock Emerging Markets Fund")

# forms.each do |form, url|
# 	downloadMutualFund(url, form)
# end

#downloadMutualFund("http://www.sec.gov/Archives/edgar/data/820892/000119312513118818/0001193125-13-118818-index.htm", "Nuveen Equity Index Fund")

# def getTerms(instance)
# 	instance = Xbrlware.ins(instance)
# 	item_all=instance.item_all_map # Fetch all facts as map, key is fact name and value is array of facts
# 	item_all.each do |name, items| # iterate
# 		puts " Items for #{name} ..." # Print item name
# 	 	items.each do |item|
# 			ctx = item.context
# 		 #   	puts ctx.period
# 		 #   	dims = ctx.dimensions # get all dimensions as array
# 			dims = ctx.dimensions # get all domains as array
# 			doms = ctx.domains(["dimension_x", "dimension_y"]) # get domains for dimensions dimension_x, dimension_y 
# 			dim_dom=ctx.dimensions_domains # Gets dimensions and corresponding domains in a Hash
# 			# dim_dom.each |dim, dom| do
# 			#  	puts "  Dimension ["+dim+"] Domains ["+dom+"]" # dom is a array containing domains
# 			# end
# 			puts identifier.to_s
# 		end
# 	end
# end

# getTerms("forms/American Mutual Fund/ck0000005506-20121031.xml")

# for i in instances.keys
# 	instance=Xbrlware.ins("forms/#{i}/#{instances.fetch(i)}")
# 	puts i
# 	puts instance
# 	getTerms(instance)
# end

def getTermsAndValues(instances)
	# for fund in instances.keys
	# 	ins=Xbrlware.ins("forms/#{fund}/#{instances.fetch(fund)}")
	# 	filing=urls.fetch(fund)
	# 	doc = Nokogiri::HTML(open(filing))
	# 	rows = doc.css("div#seriesDiv table").css(".contractRow")
	# 	subDate = doc.css("div.formContent").css(".formGrouping")[0].css(".info")[0]	
	# 	data=[ManagementFeesOverAssets, DistributionAndService12b1FeesOverAssets, AcquiredFundFeesAndExpensesOverAssets, ExpensesOverAssets, AnnualReturn2010, AnnualReturn2011, FeeWaiverOrReimbursementOverAssets]
	# #   data=[ManagementFeesOverAssets]
	# 	data.each do |val|
	# 		val.each do |item| 
	# 			ctx=item.context
	# 			cik = 0
	# 			ticker = 'ZZZ'
	# 			classType = 'Class X'
	# 			if fund == 'State Street Emerging Markets Fund' or fund == 'iShares MSCI Brazil Capped Index Fund' or fund == 'Schwab Core Equity Fund' or fund == 'Schwab Dividend Equity Fund' 
	# 				cik = ctx.id[45..54]
	# 			elsif fund == 'PIMCO Emerging Markets Full Spectrum Bond Fund'
	# 				cik = ctx.id[13..22]
	# 			else
	# 				puts "no cik found!"
	# 			end
	# 			i = 0
	# 			while rows[i].css("td").css("a").text != cik and i < rows.size
	# 				i+=1
	# 			end
	# 			row = rows[i].css("td")
	# 			ticker = row[3].text
	# 			classType = row[2].text
	# 			dataset = DB[:Form497]
	# 			tickerID = DB.fetch("SELECT id FROM Ticker WHERE Name = ? AND Class = ?", ticker, classType)
	# #	   		dataset.insert(:SubmissionDate=>subDate.text, :url=>filing, :TickerID=>tickerID)
	# 			DB.transaction do
	# # 				DB[:Ticker].insert(:Name=>ticker, :Class=>classType)
	# 				dataset=dataset.where(:TickerID=>tickerID)
	# 				dataset.update(item.name=>item.value)
	# 			end
	# 			#puts "#{ticker}, #{classType} ; #{item.name}: #{item.value}"
	# 		end
	# 	end
	# end
	# for fund in instances.keys
	# 	ins=Xbrlware.ins("forms/#{fund}/#{instances.fetch(fund)}")
	# 	ctx 


end
