from fastapi import FastAPI, HTTPException, Depends
from fastapi_pagination import Page, add_pagination, paginate, Params
from database import database as connection, User
from schemas import UserRequestModel, UserResponseModel, OkResponseModel

app = FastAPI(title='POC FastAPI',
              description='POC Python with FastAPI',
              version='0.0.1')


@app.on_event('startup')
def startup():
    if connection.is_closed():
        connection.connect()

    connection.create_tables([User])


@app.on_event('shutdown')
def shutdown():
    if not connection.is_closed():
        connection.close()


@app.post('/users', response_model=UserResponseModel)
async def create_user(user_request: UserRequestModel):
    try:
        user = User.create(
            username=user_request.username,
            email=user_request.email
        )

        return user
    except Exception as err:
        raise HTTPException(400, err.__cause__)


@app.get('/users', response_model=Page[UserResponseModel])
async def get_all_user(params: Params = Depends()):

    users = User.select().paginate(params.page, params.size)

    print(users)
    if users:
        # return paginate(UserListResponseModel.parse_obj(users))
        return paginate(users, params)
    else:
        raise HTTPException(404, 'There are not users')


@app.get('/users/{user_id}', response_model=UserResponseModel)
async def get_user(user_id):

    user = User.select().where(User.id == user_id).first()

    if user:
        return user
    else:
        raise HTTPException(404, 'User not found')


@app.put('/users/{user_id}', response_model=UserResponseModel)
async def update_user(user_request: UserRequestModel, user_id):

    user = User.select().where(User.id == user_id).first()

    if user:
        user.username = user_request.username
        user.email = user_request.email
        user.save()
        return user
    else:
        raise HTTPException(404, 'User not found')


@app.delete('/users/{user_id}', response_model=OkResponseModel)
async def delete_user(user_id):

    user = User.select().where(User.id == user_id).first()

    if user:
        user.delete_instance()
        return {"message": "User deleted"}
    else:
        raise HTTPException(404, 'User not found')


add_pagination(app)
