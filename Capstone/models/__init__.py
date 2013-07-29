from sqlalchemy import Column, Integer, String, Table, ForeignKey, DateTime, Boolean, Date, Float, Text
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.associationproxy import association_proxy
from Capstone.database import Base


class Issuer(Base):
    __tablename__ = 'Issuer'
    id = Column(Integer, primary_key=True)
    Name = Column(String(50))
    City = Column(String(50))
    Country = Column(String(50))
    FormD = relationship("FormD", backref="Issuer")
#     RegionID = Column(Integer, ForeignKey("Region.id"))
    TierID = Column(Integer)
    # def cleanName(self):
#         return  


class Tier(Base):
    __tablename__ = 'Tier'
    id = Column(Integer, primary_key=True)
    TierName = Column(String(50))
	
class FormD(Base):
    __tablename__ = 'FormD'
    id = Column(Integer, primary_key=True)
    IssuerID = Column(Integer, ForeignKey('Issuer.id'))
    url = Column(String(100))
    SubmissionDate = Column(DateTime)
    IndustryGroupType = Column(String(50))
    InvestmentFundType = Column(String(50))
    Amended = Column(Boolean)
    DateOfFirstSale = Column(Date)
    IsDateOfFirstSaleYetToOccur = Column(Boolean)
    MinimumInvestmentAccepted = Column(Integer)
    TotalOfferingAmount = Column(Integer)
    IsTotalOfferingAmountIndefinite = Column(Boolean)
    TotalAmountSold = Column(Integer)
    TotalRemaining = Column(Integer)
    IsTotalRemainingIndefinite = Column(Boolean)

class Series(Base):
    __tablename__ = 'Series'
    id = Column(Integer, primary_key=True)
    Name = Column(String(50))
    SECid = Column(String(10))
    Registrant_DocumentID = Column(Integer, ForeignKey('Registrant_Document.id'))
    Registrant_Document = relationship("Registrant_Document", backref="Serieses")

class Registrant(Base):
    __tablename__ = 'Registrant'
    id = Column(Integer, primary_key=True)
    Name = Column(String(50))

class InvestorClass(Base):
    __tablename__ = 'InvestorClass'
    id = Column(Integer, primary_key=True)
    Name = Column(String(50))
    Ticker = Column(String(10))
    Class = Column(String(50))
    SeriesID = Column(Integer, ForeignKey('Series.id'))
    Series = relationship("Series", backref="SeriesClass")
    SECid = Column(String(10))

class BloombergData(Base):
    __tablename__ = 'BloombergData'
    id = Column(Integer, primary_key=True)
    InvestorClass = relationship('InvestorClass', backref='ClassBloombergData')
    InvestorClassID = Column(Integer, ForeignKey('InvestorClass.id'))
    Managers = Column(String(100))
    NetAssetValue = Column(Float)
    NetAssetValueDate = Column(String(50))
    Assets = Column(Float)
    AssetsDate = Column(String(50))
    YearToDate = Column(Float)
    
class Term(Base):
    __tablename__ = 'Term'
    id = Column(Integer, primary_key=True)
    Name = Column(String(50))

class Registrant_Document(Base):
    __tablename__ = 'Registrant_Document'
    id = Column(Integer, primary_key=True)
    RegistrantID = Column(Integer, ForeignKey('Registrant.id'))
    Registrant = relationship("Registrant", backref="Documents")
    Type = Column(String(50))
    AmendmentFlag = Column(String(50))
    CreationDate = Column(Date)
    EffectiveDate = Column(String(50))
    ProspectusDate = Column(Date)

class Registrant_Document_Term(Base):
    __tablename__ = 'Registrant_Document_Term'
    id = Column(Integer, primary_key=True)
    TermID = Column(Integer, ForeignKey('Term.id'))
    Term = relationship("Term", backref="InvestorClasses")
    Registrant_DocumentID = Column(Integer, ForeignKey('Registrant_Document.id'))
    Registrant_Document = relationship("Registrant_Document", backref="Terms")
    SeriesID = Column(Integer, ForeignKey('Series.id'))
    Series = relationship("Series", backref="Terms")
    InvestorClassID = Column(Integer, ForeignKey('InvestorClass.id'))
    InvestorClass = relationship("InvestorClass", backref="Terms")    
    Value = Column(Text)
    UnitRef = Column(String(50))
    Decimal = Column(String(50))
    Precision = Column(String(50))
    Language = Column(String(50))
    ContextRef = Column(String(500))    
