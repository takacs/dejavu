import app.schemas as schemas
import app.models as models
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import Depends, HTTPException, status, APIRouter
from app.database import get_db

router = APIRouter()


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse
)
async def create_user(payload: schemas.UserBaseSchema, db: Session = Depends(get_db)):
    try:
        new_user = models.User(**payload.model_dump())
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A user with the given details already exists.",
        ) from e
    except Exception as e:
        print(e)
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while creating the user.",
        ) from e

    user_schema = schemas.UserBaseSchema.model_validate(new_user)
    return schemas.UserResponse(Status=schemas.Status.Success, User=user_schema)


@router.get(
    "/{user_id}", status_code=status.HTTP_200_OK, response_model=schemas.GetUserResponse
)
def get_user(user_id: str, db: Session = Depends(get_db)):
    user_query = db.query(models.User).filter(models.User.id == user_id)
    db_user = user_query.first()

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No User with this id: `{user_id}` found",
        )

    try:
        return schemas.GetUserResponse(
            Status=schemas.Status.Success,
            User=schemas.UserBaseSchema.model_validate(db_user),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while fetching the user.",
        ) from e


@router.patch(
    "/{user_id}",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=schemas.UserResponse,
)
async def update_user(
    user_id: str, payload: schemas.UserBaseSchema, db: Session = Depends(get_db)
):
    user_query = db.query(models.User).filter(models.User.id == user_id)
    db_user = user_query.first()

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No User with this id: `{user_id}` found",
        )

    try:
        update_data = payload.model_dump(exclude_unset=True)
        print(update_data)
        user_query.update(update_data, synchronize_session=False)
        db.commit()
        db.refresh(db_user)
        user_schema = schemas.UserBaseSchema.model_validate(db_user)
        return schemas.UserResponse(Status=schemas.Status.Success, User=user_schema)
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A user with the given details already exists.",
        ) from e
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while updating the user.",
        ) from e


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=schemas.DeleteUserResponse,
)
async def delete_user(user_id: str, db: Session = Depends(get_db)):
    try:
        user_query = db.query(models.User).filter(models.User.id == user_id)
        user = user_query.first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No User with this id: `{user_id}` found",
            )
        user_query.delete(synchronize_session=False)
        db.commit()
        return schemas.DeleteUserResponse(
            Status=schemas.Status.Success, Message="User deleted successfully"
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while deleting the user.",
        ) from e


@router.get(
    "/", status_code=status.HTTP_200_OK, response_model=schemas.ListUserResponse
)
async def get_users(
    db: Session = Depends(get_db), limit: int = 10, page: int = 1, search: str = ""
):
    skip = (page - 1) * limit

    users = (
        db.query(models.User)
        .filter(models.User.username.contains(search))
        .limit(limit)
        .offset(skip)
        .all()
    )
    print(users)
    users_schema = [schemas.UserBaseSchema.model_validate(user) for user in users]
    return schemas.ListUserResponse(
        status=schemas.Status.Success, results=len(users), users=users_schema
    )
