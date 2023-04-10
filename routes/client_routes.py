from fastapi import APIRouter, Depends, HTTPException
from routes.auth_routes import oauth2_scheme
from sqlalchemy.orm import session
from database.schemas import *
from utils import utils
from models import organisation
from models import user
from models import client
from typing import List

router = APIRouter()

@router.get("/{org_id}")
def fetch_client(org_id: int, db: session = Depends(utils.get_db), token = Depends(oauth2_scheme)):
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
    clients = db.query(Client).filter(Client.org_id == org_id).all()
    return clients

@router.post("/{org_id}")
def create_clients(org_id: int, request: List[client.clint], db: session = Depends(utils.get_db), token = Depends(oauth2_scheme)):
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
    client_list = []
    for client in request:
        new_client = Client(
            org_id = org_id,
            first_name = client.first_name,
            middle_name = client.middle_name,
            last_name = client.last_name,
            is_potentincial = client.is_potentincial,
            source = client.source,
            email = client.email,
            phone = client.phone,
            address = client.address
        )
        db.add(new_client)
        db.commit()
        db.refresh(new_client)
        client_list.append(new_client)
    return client_list

@router.put("/{org_id}/{client_id}")
def change_client(org_id: int, client_id: int, request: client.clint,  db: session = Depends(utils.get_db), token = Depends(oauth2_scheme)):
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
    client = db.query(Client).filter(Client.id == client_id).first()
    client.first_name = request.first_name
    client.middle_name = request.middle_name
    client.last_name = request.last_name
    client.email = request.email
    client.source = request.source
    client.phone = request.phone
    client.address = request.address
    client.is_potentincial = request.is_potentincial
    db.commit()
    db.refresh(client)
    return client

@router.delete("/{org_id}/{client_id}")
def delete_client(org_id: int, client_id: int, db: session = Depends(utils.get_db), token = Depends(oauth2_scheme)):
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
    client = db.query(Client).filter(Client.id == client_id).first()
    db.delete(client)
    db.commit()
    return True


@router.get("/topics/{org_id}")
def fetch_topics(org_id: int, db: session = Depends(utils.get_db), token = Depends(oauth2_scheme)):
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
    topics = db.query(Topic).filter(Topic.org_id == org_id).all()
    return topics

@router.post("/topic/{org_id}")
def create_topic(org_id: int, request:client.topic, db: session = Depends(utils.get_db), token = Depends(oauth2_scheme)):
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
    new_topic = Topic(
        org_id=org_id,
        service_id=request.service_id,
        empl_id=user_id,
        title=request.title,
        description=request.description,
        status=request.status,
        created_date=request.created_date
    )
    db.add(new_topic)
    db.commit()
    db.refresh(new_topic)
    return new_topic

@router.put("/topic/{org_id}/{topic_id}")
def change_topic(org_id: int, topic_id:int, request:client.topic, db: session = Depends(utils.get_db), token = Depends(oauth2_scheme)):
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
    topic = db.query(Topic).filter(Topic.id == topic_id).first()
    topic.service_id = request.service_id
    topic.client_id = request.title
    topic.title = request.title
    topic.status = request.status
    topic.description = request.description
    topic.created_date = request.created_date
    db.commit()
    db.refresh(topic)
    return topic
    
@router.delete("/topic/{org_id}/{topic_id}")
def delete_topic(org_id: int, topic_id:int, db: session = Depends(utils.get_db), token = Depends(oauth2_scheme)):
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
    topic = db.query(Topic).filter(Topic.id == topic_id).first()
    db.delete(topic)
    db.commit()
    return True    


@router.put("/advice/{org_id}/{id}")
def fetch_advices(org_id: int,id:int,request:client.advice, db: session = Depends(utils.get_db), token = Depends(oauth2_scheme)):
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
    advice =db.query(Advice).filter(Advice.id == id).first()
    advice.title=request.title
    advice.description=request.description
    db.commit()
    db.refresh(client)
    return client
    


@router.delete("/advice/{org_id}/{id}")
def delete_advice(org_id: int,id:int, db: session = Depends(utils.get_db), token = Depends(oauth2_scheme)):
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
    advice =db.query(Advice).filter(Advice.id == id).first()

    db.delete(advice)
    db.commit()
    return True    

    



@router.get("/advices/{org_id}")
def fetch_advices(org_id: int, db: session = Depends(utils.get_db), token = Depends(oauth2_scheme)):
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
    advices = db.query(Advice).filter(Advice.org_id == org_id).all()
    return advices

@router.post("/advice/{org_id}")
def create_advice(org_id: int, request:client.advice, db: session = Depends(utils.get_db), token = Depends(oauth2_scheme)):
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
    new_advice = Advice(
        org_id=org_id,
        title=request.title,
        description=request.description
    )     
    db.add(new_advice)
    db.commit()
    db.refresh(new_advice)
    return new_advice
@router.get("/analitics/{org_id}")
def getAnal(org_id:int,db:session=Depends(utils.get_db),token=Depends(oauth2_scheme)):
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
        topics = db.query(Topic).filter(Topic.org_id == org_id).all()
        clients = db.query(Client).filter(Client.org_id == org_id).all()
        anal= list()
        for i in range(1, int(len(topics)/(len(clients)+2)-1),2):
            anal.append(i)
        anal.append(len(topics)/(len(clients)+1))
        return anal