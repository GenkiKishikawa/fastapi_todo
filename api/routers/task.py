from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

import api.schemas.task as task_schema
import api.cruds.task as task_crud
from api.core.db import get_async_db
from api.exceptions.core import APIException
from api.exceptions.error_messages import ErrorMessage


router = APIRouter()


@router.get("/tasks", response_model=list[task_schema.Task])
async def list_tasks(db: AsyncSession = Depends(get_async_db)):
	return await task_crud.get_tasks_with_done(db)


@router.post("/tasks", response_model=task_schema.TaskCreateResponse)
async def create_task(task_body: task_schema.TaskCreate, db: AsyncSession = Depends(get_async_db)):
	return await task_crud.create_task(db, task_body)


@router.put("/tasks/{task_id}", response_model=task_schema.TaskCreateResponse)
async def update_task(task_id: int, task_body: task_schema.TaskCreate, db: AsyncSession = Depends(get_async_db)):
	task = await task_crud.get_task(db, task_id)
	if task is None:
		raise APIException(ErrorMessage.ID_NOT_FOUND)
	
	return await task_crud.update_task(db, task_body, original=task)


@router.delete("/tasks/{task_id}", response_model=None)
async def delete_task(task_id: int, db: AsyncSession = Depends(get_async_db)):
	task = await task_crud.get_task(db, task_id=task_id)
	if task is None:
		raise APIException(ErrorMessage.ID_NOT_FOUND)
	
	return await task_crud.delete_task(db, original=task)