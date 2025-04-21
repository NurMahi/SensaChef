from fastapi import APIRouter, Depends
from app.database import supabase
from app.database import admin_supabase
from pydantic import BaseModel
from datetime import datetime, timezone
from fastapi import HTTPException
from app.auth.auth_handler import JWTBearer

router = APIRouter()
class userModel(BaseModel):
    firstName: str
    lastName: str
    username: str
    email: str
    password: str
    confirmPassword: str
    userType: str
    
class SignInModel(BaseModel):
    username: str
    password: str

# Get all Users
@router.get("/users", tags=["users"])
async def read_all_users():
    response = supabase.table("users").select("*").execute()
    return response.data

# Create A User
@router.post("/create_user", tags=["users"])
async def create_user(user: userModel):

    if user.password != user.confirmPassword:
        raise HTTPException(status_code=400, detail="Passwords do not match")

    full_name = user.firstName + " " + user.lastName

    response = supabase.auth.sign_up(
    {
        "email": user.email,
        "password": user.password,
        "options": {"data": {"full_name": full_name, "username": user.username, "userType": user.userType}},
    }
)
    return response
# Sign in Route
@router.post("/sign_in", tags=["users"])
async def sign_in(user: SignInModel):
    result = supabase.table("users").select("email").eq("username", user.username).execute()
    email = result.data[0]["email"]
    response = supabase.auth.sign_in_with_password(
    {
        "email": email, 
        "password": user.password,
    }
)
    return response
# Sign Out Route
@router.get("/sign_out", tags=["users"])
async def sign_out():
    response = supabase.auth.sign_out()
    return response

# Get User's Recipes
@router.post("/users/recipes", tags=["users"])
async def user_recipes(user_id: str):
    response = supabase.table("recipes").select("*, steps(*)").eq("user_id", user_id).execute()
    return response.data

# Update Users
@router.put("/users/{user_id}", tags=["users"])
async def update_user(user_id: str, user: userModel):
    response = supabase.table("users").update({
        "name": user.name,
        "email": user.email
    }).eq("user_id", user_id).execute()
    return response.data

# Delete User
@router.delete("/users/{user_id}", dependencies=[Depends(JWTBearer())], tags=["users"])
async def delete_user(user_id: str):
    response = supabase.table("users").delete().eq("user_id", user_id).execute()
    admin_supabase.auth.admin.delete_user(user_id)
    return response.data

@router.get("/protected")
async def get_user_info(payload: dict = Depends(JWTBearer())):
    user_id = payload.get("sub")
    return {"message": f"Welcome, user {user_id}!", "payload": payload}
