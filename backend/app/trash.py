import app.schemas as schemas
import app.models as models
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import Depends, HTTPException, status, APIRouter
from app.database import get_db

router = APIRouter()


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=schemas.TrashResponse
)
async def create_trash(payload: schemas.TrashBaseSchema, db: Session = Depends(get_db)):
    try:
        new_trash = models.Trash(**payload.model_dump())
        db.add(new_trash)
        db.commit()
        db.refresh(new_trash)

    except Exception as e:
        print(e)
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while creating the user.",
        ) from e

    trash_schema = schemas.TrashBaseSchema.model_validate(new_trash)
    return schemas.TrashResponse(Status=schemas.Status.Success, Trash=trash_schema)


@router.get(
    "/{trash_id}",
    status_code=status.HTTP_200_OK,
    response_model=schemas.GetTrashResponse,
)
def get_trash(trash_id: str, db: Session = Depends(get_db)):
    trash_query = db.query(models.Trash).filter(models.Trash.id == trash_id)
    db_trash = trash_query.first()

    if not db_trash:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No trash with this id: `{trash_id}` found",
        )

    try:
        return schemas.GetTrashResponse(
            Status=schemas.Status.Success,
            Trash=schemas.TrashBaseSchema.model_validate(db_trash),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while fetching the trash.",
        ) from e


@router.patch(
    "/{trash_id}",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=schemas.TrashResponse,
)
async def update_trash(
    trash_id: str, payload: schemas.TrashBaseSchema, db: Session = Depends(get_db)
):
    trash_query = db.query(models.Trash).filter(models.Trash.id == trash_id)
    db_trash = trash_query.first()

    if not db_trash:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No trash with this id: `{trash_id}` found",
        )

    try:
        update_data = payload.model_dump(exclude_unset=True)
        trash_query.update(update_data, synchronize_session=False)
        db.commit()
        db.refresh(db_trash)
        trash_schema = schemas.TrashBaseSchema.model_validate(db_trash)
        return schemas.TrashResponse(Status=schemas.Status.Success, Trash=trash_schema)
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A trash with the given details already exists.",
        ) from e
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while updating the trash.",
        ) from e


@router.delete(
    "/{trash_id}",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=schemas.DeleteTrashResponse,
)
async def delete_trash(trash_id: str, db: Session = Depends(get_db)):
    try:
        trash_query = db.query(models.Trash).filter(models.Trash.id == trash_id)
        trash = trash_query.first()
        if not trash:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No trash with this id: `{trash_id}` found",
            )
        trash_query.delete(synchronize_session=False)
        db.commit()
        return schemas.DeleteTrashResponse(
            Status=schemas.Status.Success, Message="trash deleted successfully"
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while deleting the trash.",
        ) from e


@router.get(
    "/", status_code=status.HTTP_200_OK, response_model=schemas.ListTrashResponse
)
async def get_trashs(
    db: Session = Depends(get_db), limit: int = 10, page: int = 1, search: str = ""
):
    skip = (page - 1) * limit

    trash = (
        db.query(models.Trash)
        .filter(models.Trash.trashname.contains(search))
        .limit(limit)
        .offset(skip)
        .all()
    )
    trash_schema = [schemas.TrashBaseSchema.model_validate(trash) for trash in trash]
    return schemas.ListTrashResponse(
        status=schemas.Status.Success, results=len(trash), trash=trash_schema
    )
