from beanie import Indexed
from beanie.operators import Or
from pydantic import Field
from typing import Annotated, Any
from datetime import datetime
from app.common.model import CommonDocument
from app.dtos.company import BaseCompany
from app.dtos.company import BaseCompany
from app.exceptions.company import CompanyNotFoundException

class Company(CommonDocument):
    """
        Company document representing a company entity in the database.
        
        Stores the ticker, name, country, and address of a company.
    """
    ticker: Annotated[str, Indexed(unique=True)] = Field(...)
    name: str = Field(...)
    country: str = Field(...)
    address: str = Field(...)
    
    class Settings:
        name = "companies"
    
    @classmethod
    def from_dto(cls, data: BaseCompany) -> "Company":
        """
        Create a Company document instance from a BaseCompany DTO.

        Args:
            data (BaseCompany): The data transfer object containing company information.

        Returns:
            Company: A new Company document instance populated with the DTO data.
        """
        return cls(
            ticker=data.ticker,
            name=data.name,
            country=data.country,
            address=data.address
        )

    @classmethod
    def to_dto(cls, data: "Company") -> BaseCompany:
        """
        Convert a Company document instance into a BaseCompany DTO.

        Args:
            data (Company): The Company document instance to convert.

        Returns:
            BaseCompany: A data transfer object containing the company's information.
        """
        return BaseCompany(
            ticker=data.ticker,
            name=data.name,
            country=data.country,
            address=data.address 
        )
        
    @classmethod
    async def get_company(
        cls, 
        company_id: Annotated[int | None, "Company id"] = None, 
        ticker: Annotated[str | None, "Company ticker"] = None,
    ) -> "Company | None":
        """
            Retrieve a company by its ID or ticker.

            This method searches for a company document in the database
            using either the unique company ID or its ticker symbol.

            Args:
                company_id (int): The ID of the company to retrieve.
                ticker (str): The ticker symbol of the company to retrieve.

            Returns:
                BaseCompany | None: A DTO representing the company if found.

            Raises:
                CompanyNotFoundException: If no company with the given ID or ticker exists.
        """
        existing_company = await cls.find_one(
            Or(cls.id == company_id, cls.ticker == ticker)
        )
        return existing_company
    
    @classmethod
    async def paginate(
        cls,
        limit: int = 5,
        cursor: str | None = None,
        start_date: datetime | None = None,
        end_date: datetime | None = None
    ) -> dict[str, Any]:
        """
        Hybrid pagination with date range and cursor (ticker-based).

        Args:
            limit (int): Number of results per page.
            cursor (str, optional): Last ticker from previous page.
            start_date (datetime, optional): Filter companies created from this date.
            end_date (datetime, optional): Filter companies created up to this date.

        Returns:
            dict: {
                "result": List[Company],
                "next_cursor": str | None,
                "total": int
            }
        """
        match_filter = {}
        
        if start_date or end_date:
            match_filter["created_at"] = {}
            if start_date:
                match_filter["created_at"]["$gte"] = start_date
            if end_date:
                match_filter["created_at"]["$lte"] = end_date
        
        if cursor:
            match_filter["ticker"] = {"$gt": cursor} if "ticker" not in match_filter else {"$gt": cursor, **match_filter["ticker"]}

        pipeline = [{"$match": match_filter}] if match_filter else []
        pipeline += [
            {"$sort": {"ticker": 1}},
            {"$limit": limit}
        ]
        total_companies = await cls.count()
        results = await cls.aggregate(pipeline).to_list()
        companies = [cls(**doc) for doc in results]
        
        return {
            "result": companies,
            "next_cursor": str(companies[-1].ticker) if companies else None,
            "total": total_companies
        }