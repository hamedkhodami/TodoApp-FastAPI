from fastapi import APIRouter, HTTPException, Path, Depends, Query
from sqlalchemy.orm import Session
from typing import List

from core.database import get_db
from tasks.schemas import TaskCreateSchema, TaskUpdateSchema, TaskResponseSchema
from tasks.models import TaskModel

router = APIRouter(tags=["tasks"], prefix="/todo")

@router.get("/tasks", response_model=List[TaskResponseSchema])
async def retrieve_tasks_list(
        completed: bool = Query(None, description="Whether or not the task has been completed"),
        limit: int = Query(10, gt=0, le=50, description="The maximum number of tasks to return"),
        offset: int = Query(0, gt=0, description="The offset of the first task to return"),
        db: Session = Depends(get_db)):
    query = db.query(TaskModel)
    if completed is not None:
        query = query.filter_by(is_completed=completed)
    return query.limit(limit).offset(offset).all()

@router.get("/tasks/{task_id}", response_model=TaskResponseSchema)
async def retrieve_tasks_detail(task_id: int = Path(..., gt=0), db: Session = Depends(get_db)):
    task_object = db.query(TaskModel).filter_by(id = task_id).first()
    if not task_object:
        raise HTTPException(status_code=404, detail="Task not found")
    return task_object

@router.post("/tasks")#, response_model=TaskCreateSchema
async def create_task(request: TaskCreateSchema, db: Session = Depends(get_db)):
    task_object = TaskModel(**request.model_dump())
    db.add(task_object)
    db.commit()
    db.refresh(task_object)
    return task_object

@router.put("/tasks/{task_id}", response_model=TaskResponseSchema)
async def update_task(request: TaskUpdateSchema,task_id: int = Path(..., gt=0), db: Session = Depends(get_db)):
    task_object = db.query(TaskModel).filter_by(id = task_id).first()
    if not task_object:
        raise HTTPException(status_code=404, detail="Task not found")
    for field, value in request.model_dump(exclude_unset=True).items():
        setattr(task_object, field, value)
    db.commit()
    db.refresh(task_object)
    return task_object


@router.delete("/tasks/{task_id}", status_code=204)
async def delete_task(task_id: int = Path(..., gt=0), db: Session = Depends(get_db)):
    task_object = db.query(TaskModel).filter_by(id = task_id).first()
    if not task_object:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task_object)
    db.commit()
