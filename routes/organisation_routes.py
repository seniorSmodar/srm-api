from fastapi import APIRouter, Depends, HTTPException
from routes.auth_routes import oauth2_scheme
from sqlalchemy.orm import session
from database.schemas import *
from utils import utils
from models import organisation
from models import user
from typing import List

router = APIRouter()

@router.post("/") 
def create_org(request: organisation.organisation, db: session = Depends(utils.get_db), token = Depends(oauth2_scheme)):
    user_id = utils.encode_token(token)['id']
    new_org = Organisation(
        name = request.name,
        description = request.description
    )
    db.add(new_org)
    db.commit()
    db.refresh(new_org)
    new_empl = Employee(
        title = "Создатель",
        user_id = user_id,
        org_id = new_org.id,
        write = True,
        chek = True,
        delete = True
    )
    db.add(new_empl)
    db.commit()
    organisation = db.query(Organisation).filter(Organisation.name == request.name).first()
    return organisation

@router.get("/")
def fetch_org(db: session = Depends(utils.get_db), token = Depends(oauth2_scheme)):
    user_id = utils.encode_token(token)['id']
    user = db.query(User).filter(User.id == user_id).first()
    org_list = []
    for empl in user.employee:
        empl_id = empl.__dict__['org_id']
        organisation = db.query(Organisation).filter(Organisation.id == empl_id).first()
        org_list.append(organisation)
    return org_list

@router.put("/{id}")
def update_org(id: int, request: organisation.organisation, db: session = Depends(utils.get_db), token = Depends(oauth2_scheme)):
    user_id = utils.encode_token(token)['id']
    organisation = db.query(Organisation).filter(Organisation.id == id).first()
    employee = utils.employee_from_org(db, user_id, id)
    if not employee:
        raise HTTPException(
             status_code=404,
             detail="permission denaid"
        )
    if not employee['delete']:
        raise HTTPException(
            status_code=404,
            detail="permission denaid"
        )
    organisation.name = request.name
    organisation.description = request.description
    db.commit()
    organisation = db.query(Organisation).filter(Organisation.id == id).first()
    return organisation


@router.post("/employee/{org_id}")
def create_users_for_org(org_id: int, request: List[user.user], db: session = Depends(utils.get_db), token = Depends(oauth2_scheme)):
    user_id = utils.encode_token(token)['id']
    employee = utils.employee_from_org(db, user_id, org_id)
    user_list = []
    if not employee:
        raise HTTPException(
            status_code=404,
            detail="permission denaid"
        )
    if not employee['write']:
        raise HTTPException(
            status_code=404,
            detail="permission denaid"
        )
    for user in request:
        new_user = User(
            username=user.username,
            password_hash=utils.getPasswordHash(user.password),
            first_name=user.first_name,
            last_name=user.last_name
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        user_list.append(new_user)
        new_empl = Employee(
            title="User",
            user_id=new_user.id,
            org_id=org_id,
            write=False,
            chek=True,
            delete=False
        )
        db.add(new_empl)
        db.commit()
    return user_list

@router.get("/employee/{org_id}")
def fetch_users(org_id: int, db: session = Depends(utils.get_db), token = Depends(oauth2_scheme)):
    user_id = utils.encode_token(token)['id']
    employee = utils.employee_from_org(db, user_id, org_id)
    if not employee:
        raise HTTPException(
            status_code=404,
            detail="permission denaid"
        )
    if not employee['chek']:
        raise HTTPException(
            status_code=404,
        )
    organisation = db.query(Organisation).filter(Organisation.id == org_id).first()
    user_list = []
    for empl in organisation.employees:
        usr_id = empl.__dict__['user_id']
        user = db.query(User).filter(User.id == usr_id).first()
        user_list.append(user)
    return user_list

@router.put("/employee/{org_id}/{user_id}")
def change_employee(org_id:int, user_id:int, request:organisation.employee,db: session = Depends(utils.get_db), token = Depends(oauth2_scheme)):
    user_id = utils.encode_token(token)['id']
    employee = utils.employee_from_org(db, user_id, org_id)
    if not employee:
        raise HTTPException(
            status_code=404,
            detail="permission denaid"
        )
    if not employee['write']:
        raise HTTPException(
            status_code=404,
        )
    employee = db.query(Employee).filter(Employee.user_id == user_id and Employee.org_id == org_id).first()
    employee.title = request.title
    employee.write = request.write
    employee.chek = request.chek
    employee.delete = request.delete
    db.commit()
    db.refresh(employee)
    return employee

@router.delete("/employee/{org_id}/{user_id}")
def delete_employee(org_id: int, user_id: int, db: session = Depends(utils.get_db), token = Depends(oauth2_scheme)):
    user_id = utils.encode_token(token)['id']
    employee = utils.employee_from_org(db, user_id, org_id)
    if not employee:
        raise HTTPException(
            status_code=404,
            detail="permission denaid"
        )
    if not employee['delete']:
        raise HTTPException(
            status_code=404,
        )
    empl = db.query(Employee).filter(Employee.user_id == user_id and Employee.org_id == org_id).first()
    db.delete(empl)
    db.commit()
    return True


@router.get("/services/{org_id}")
def fetch_services(org_id: int, db: session = Depends(utils.get_db), token = Depends(oauth2_scheme)):
    user_id = utils.encode_token(token)['id']
    employee = utils.employee_from_org(db, user_id, org_id)
    if not employee:
        raise HTTPException(
            status_code=404,
            detail="permission denaid"
        )
    if not employee['chek']:
        raise HTTPException(
            status_code=404,
            detail="permission denaid"
        )
    services = db.query(Service).filter(Service.org_id == org_id).all()
    return services

@router.post("/service/{org_id}")
def create_service(org_id: int, request: organisation.service, db: session = Depends(utils.get_db), token = Depends(oauth2_scheme)):
    user_id = utils.encode_token(token)['id']
    employee = utils.employee_from_org(db, user_id, org_id)
    if not employee:
        raise HTTPException(
            status_code=404,
            detail="permission denaid"
        )
    if not employee['write']:
        raise HTTPException(
            status_code=404,
            detail="permission denaid"
        )
    new_service = Service(
        org_id = org_id,
        title = request.title,
        description = request.description
    )
    db.add(new_service)
    db.commit()
    db.refresh(new_service)
    return new_service

@router.put("/service/{org_id}/{service_id}")
def change_service(service_id: int, org_id: int, request: organisation.service, db: session = Depends(utils.get_db), token = Depends(oauth2_scheme)):
    user_id = utils.encode_token(token)['id']
    employee = utils.employee_from_org(db, user_id, org_id)
    if not employee:
        raise HTTPException(
            status_code=404,
            detail="permission denaid"
        )
    if not employee['write']:
        raise HTTPException(
            status_code=404,
            detail="permission denaid"
        )
    service = db.query(Service).filter(Service.id == service_id).first()
    service.title = request.title
    service.description = request.description
    db.commit()
    service = db.query(Service).filter(Service.id == service_id).first()
    return service

@router.delete("/service/{org_id}/{service_id}")
def delete_service(org_id: int, service_id: int, db: session = Depends(utils.get_db), token = Depends(oauth2_scheme)):
    user_id = utils.encode_token(token)['id']
    employee = utils.employee_from_org(db, user_id, org_id)
    if not employee:
        raise HTTPException(
            status_code=404,
            detail="permission denaid"
        )
    if not employee['delete']:
        raise HTTPException(
            status_code=404,
            detail="permission denaid"
        )
    service = db.query(Service).filter(Service.id == service_id).first()
    db.delete(service)
    db.commit()
    return True


