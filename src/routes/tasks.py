from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from mongoengine import Document, StringField, ListField,BooleanField
from typing import List

router = APIRouter()
class TaskInput(BaseModel):
    task: str
    description: str 
class TaskOutput(BaseModel):
    id:str
    title: str
    description: str
    completed: bool
class Task(Document):
    title = StringField(required=True)
    description = StringField(required=True)
    completed=BooleanField(required=True)

tasks_db = []

@router.get("/get_tasks", summary="Get all tasks", response_model=List[TaskOutput])
async def get_tasks():
    tasks_to_return = Task.objects()

    return [{'id': str(task.id), 'title': task.title, 'description': task.description, 'completed': task.completed} for task in tasks_to_return]

@router.post("/create_tasks", summary="Create a new task", response_model=TaskOutput)
async def create_task(task_input: TaskInput):
    existing_task = Task.objects(title=task_input.task).first()
    if existing_task:
        raise HTTPException(status_code=400, detail="Task already exists")

    try:
        new_task = Task(
            title=task_input.task,
            description=task_input.description,
            completed=False
        )
        new_task.save()

        return TaskOutput(
            id=str(new_task.id),
            title=new_task.title,
            description=new_task.description,
            completed=new_task.completed
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create task: {str(e)}")


@router.put("/{task_id}", summary="Update a task")
async def update_task(task_id: str, task_input: TaskInput):
    try:
        task_to_update=Task.objects(id=str(task_id)).first()
        task_to_update.update(title=task_input.task,description=task_input.description)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update a tasks: {str(e)}")

    
    return {'message': f'Task with ID {task_to_update.id} sucesfully updated'}



@router.delete("/{task_id}", summary="Delete a task")
async def delete_task(task_id: str):
    try:

        task_to_delete=Task.objects(id=task_id).first()
        if task_to_delete:
            task_to_delete.delete()
        else:
            return  HTTPException(status_code=500, detail=f"the task doesn't exists")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete  a task: {str(e)}")
    return {'message': f'Task with ID {task_to_delete.id} sucesfully deleted'}




@router.patch("/{task_id}", summary="Partial update of a task")
async def partial_update_task(task_id: str,status:bool):
    tast_patch= Task.objects(id=task_id).first()
    if tast_patch:
        tast_patch.update(completed=status)
    else:
          raise HTTPException(status_code=404, detail=f"the task with  ID {task_id} doesn't exists")
    return {'message': f'Task with ID {tast_patch.id} sucesfully updatedd', 'the current status is': status}
