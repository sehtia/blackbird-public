from dataclasses import dataclass, field
from typing import List


@dataclass
class CompanyFundingData:
    funding_amount: int = 0
    funding_category: str = ""
    funding_date: str = ""
    funding_type: str = ""
    funding_investors: str = ""

    def to_tuple(self):
        return self.funding_amount, self.funding_category, self.funding_date, self.funding_type, self.funding_investors


@dataclass
class CompanyData:
    company_url: str = ""
    twitter_url: str = ""
    year_founded: str = ""
    industries: List = field(default_factory=lambda: [])
    funding: List[CompanyFundingData] = field(default_factory=list)
    city: str = ""
    street_address: str = ""

    def to_tuple(self):
        return self.company_url, self.twitter_url, self.year_founded, self.industries, self.funding, self.city, self.street_address



