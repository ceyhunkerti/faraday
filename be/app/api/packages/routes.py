# from fastapi import APIRouter

# router = APIRouter(prefix="/packages")


# @app.get("/users/{user_id}")
# async def read_user(user_id: int, session: AsyncSession = Depends(get_async_session)):
#     """Get a user by ID."""
#     query = session.query(User).options(selectinload(User.posts)).filter(User.id == user_id)
#     user = await query.first()
#     return user
