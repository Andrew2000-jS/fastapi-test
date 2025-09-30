from beanie import Indexed
from pydantic import Field
from typing import Annotated
from .common import CommonDocument
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
    def from_company(cls, data: "Company") -> BaseCompany:
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
            (cls.id == company_id) | (cls.ticker == ticker)
        )
        if not existing_company:
            raise CompanyNotFoundException()
        return existing_company
    