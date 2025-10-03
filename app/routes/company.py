from fastapi import APIRouter, status, Body, Query, Path
from typing import Annotated
from pydantic import ValidationError
from datetime import datetime
from app.models.company import Company
from app.common.schema import ResponseDTO, PaginationDTO
from app.dtos.company import CompanyCreate, CompanyUpdate, BaseCompany
from app.exceptions.company import CompanyAlreadyExistsException, CompanyNotFoundException
from app.conf.security import auth_dependency

company_router = APIRouter(prefix="/api/companies", tags=["Company"])

@company_router.post("/{company_ticker}", status_code=status.HTTP_200_OK, response_model=ResponseDTO[BaseCompany])
async def get_company(company_ticker: Annotated[str, Path()]):
    try:
        existing_company = await Company.get_company(ticker=company_ticker)
        if not existing_company:
            raise CompanyNotFoundException()
        company = Company.to_dto(data=existing_company)
        response = ResponseDTO(message="Company result", status_code=status.HTTP_200_OK, data=company)
        return response
    except ValidationError as e:
        raise e

@company_router.get("/", status_code=status.HTTP_200_OK, response_model=ResponseDTO[list[BaseCompany]])
async def get_companies(
    limit: Annotated[int, Query(gt=0, le=100, description="Number of companies per page")] = 5,
    cursor: Annotated[str | None, Query(description="Last ticker from the previous page")] = None,
    start_date: Annotated[datetime | None, Query()] = None,
    end_date: Annotated[datetime | None, Query()] = None,
):
    try:
        companies = await Company.paginate(limit=limit, cursor=cursor, start_date=start_date, end_date=end_date)
        pagination = PaginationDTO(
            limit=limit,
            total=companies["total"],
            next_cursor=companies["next_cursor"],
        )
        
        response = ResponseDTO(
            message="Companies page",
            status_code=status.HTTP_200_OK,
            data=companies["result"],
            pagination=pagination
        )
        return response
    except ValidationError as e:
        raise e

@company_router.post("/", status_code=status.HTTP_201_CREATED, response_model=ResponseDTO[CompanyCreate])
async def create_company(body: Annotated[CompanyCreate, Body()], crr_auth: auth_dependency):
    try:
        existing_company = await Company.get_company(ticker=body.ticker)
        if existing_company:
            raise CompanyAlreadyExistsException()
        new_company = Company.from_dto(data=body)
        await new_company.insert()
        
        response = ResponseDTO(message="Company created", status_code=status.HTTP_201_CREATED, data=body)
        return response
    except ValidationError as e:
        raise e

@company_router.patch("/{company_ticker}", status_code=status.HTTP_200_OK, response_model=ResponseDTO)
async def update_company(body: Annotated[CompanyUpdate, Body()], company_ticker: Annotated[str, Path()], crr_auth: auth_dependency):
    try:
        existing_company = await Company.get_company(ticker=company_ticker)
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
        response = ResponseDTO(message="Company updated successfully", status_code=status.HTTP_200_OK)
        return response
    except ValidationError as e:
        raise e
    
@company_router.delete("/{company_ticker}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_company(company_ticker: Annotated[str, Path()], crr_auth: auth_dependency):
    try:
        existing_company = await Company.get_company(ticker=company_ticker)
        if not existing_company:
            raise CompanyNotFoundException()
        await existing_company.delete()
    except ValidationError as e:
        raise e
