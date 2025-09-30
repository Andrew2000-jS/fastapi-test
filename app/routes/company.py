from fastapi import APIRouter, status, Body, Query, Path
from typing import Annotated
from app.models.company import Company
from app.dtos.common import ResponseDTO
from app.dtos.company import CompanyCreate, CompanyUpdate, BaseCompany
from app.exceptions.company import CompanyAlreadyExistsException, CompanyNotFoundException
from app.conf.security import auth_dependency

company_router = APIRouter(prefix="/company", tags=["Company"])

@company_router.post("/{company_ticker}", status_code=status.HTTP_200_OK, response_model=ResponseDTO[BaseCompany])
async def get_company(company_ticker: Annotated[str, Path()]):
    existing_company = await Company.get_company(ticker=company_ticker)
    if not existing_company:
        raise CompanyNotFoundException()
    company = Company.from_company(data=existing_company)
    return company

@company_router.get("/", status_code=status.HTTP_200_OK, response_model=ResponseDTO[list[BaseCompany]])
async def get_companies(skip: Annotated[int, Query()], limit: Annotated[int, Query()]):
    company_list = await Company.find_many(skip=skip, limit=limit).to_list()
    return ResponseDTO(message="All companies", data=company_list)

@company_router.post("/", status_code=status.HTTP_201_CREATED, response_model=ResponseDTO[CompanyCreate])
async def create_company(body: Annotated[CompanyCreate, Body()], crr_auth: auth_dependency):
    existing_company = await Company.get_company(ticker=body.ticker)
    if not existing_company:
        raise CompanyAlreadyExistsException()
    new_company = Company.from_dto(data=body)
    await new_company.insert()
    return ResponseDTO(message="Company created", data=body)

@company_router.patch("/{company_ticker}", status_code=status.HTTP_200_OK, response_model=ResponseDTO)
async def update_company(body: Annotated[CompanyUpdate, Body()], company_ticker: Annotated[str, Path()], crr_auth: auth_dependency):
    existing_company = await Company.get_company(ticker=body.ticker)
    if not existing_company:
        raise CompanyAlreadyExistsException()
    
    await existing_company.update({
        "$set": {
            Company.ticker: body.ticker if body.ticker else existing_company.ticker,
            Company.name: body.name if body.name else existing_company.name,
            Company.country: body.country if body.country else existing_company.country,
            Company.address: body.address if body.address else existing_company.address
        }
    })

@company_router.delete("/{company_ticker}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_company(company_ticker: Annotated[str, Path()], crr_auth: auth_dependency):
    existing_company = await Company.get_company(ticker=company_ticker)
    if not existing_company:
        raise CompanyAlreadyExistsException()
    await existing_company.delete()
