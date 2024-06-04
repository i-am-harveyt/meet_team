"""This is the route for message"""

import os
from typing import Annotated 

import jwt
from fastapi import APIRouter, Header, status
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse


from ...models.models_message import MessageCreateRequest
from ..handlers import handler_message

message_router = APIRouter() # 建FastAPI router

@message_router.post("/") # 設POST router,當訪問此router時會調用create()
async def create(

    
      req: MessageCreateRequest, authorization: Annotated[str | None, Header()]= None
):
    try: # 創建新的message
        new_message_id = await handler_message.create( # 調用 message.create
            req.task_id, req.creator_id, req.description,
        )
        return {"message": "Message created successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e),
        ) from e
    