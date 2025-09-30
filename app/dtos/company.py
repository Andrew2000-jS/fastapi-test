from pydantic import BaseModel, Field

class BaseCompany(BaseModel):
    ticker: str = Field(
        ...,
        title="Ticker Symbol",
        description="Unique identifier for the company, usually a short abbreviation or symbol."
    )
    name: str = Field(
        ...,
        title="Company Name",
        description="Official name of the company."
    )
    country: str = Field(
        ...,
        title="Country",
        description="Country where the company is registered or primarily operates.",
        examples=["United States"]
    )
    address: str = Field(
        ...,
        title="Address",
        description="Full address of the company's headquarters or main office.",
        examples=["Miami street 123"]
    )
    
class CompanyCreate(BaseCompany):
    pass
    
class CompanyUpdate(BaseModel):
    ticker: str | None | None = Field(
        default=None,
        title="Ticker Symbol",
        description="Unique identifier for the company, usually a short abbreviation or symbol."
    )
    name: str | None = Field(
        default=None,
        title="Company Name",
        description="Official name of the company."
    )
    country: str | None = Field(
        default=None,
        title="Country",
        description="Country where the company is registered or primarily operates.",
        examples=["United States"]
    )
    address: str | None = Field(
        default=None,
        title="Address",
        description="Full address of the company's headquarters or main office.",
        examples=["Miami street 123"]
    )
    
class CompanyList(BaseModel):
    companies: list[BaseCompany] = Field(
        ...,
        title="Companies",
        description="A list of company records returned in the current query."
    )
    page: int = Field(
        ...,
        title="Page Number",
        description="The current page number of the paginated results."
    )
    total: int = Field(
        ...,
        title="Total Records",
        description="The total number of companies available in the database."
    )
    limit: int = Field(
        ...,
        title="Limit",
        description="The maximum number of companies returned per page."
    )
    skip: int = Field(
        ...,
        title="Skip",
        description="The number of records skipped before starting to collect the results."
    )
