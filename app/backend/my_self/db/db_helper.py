from bson.objectid import ObjectId

def add_user_helper(user) ->dict:
    return {'UserName':user['name'],"email":user['email'],"password":user['password'],'role': user['role']}
    
def fetch_user_helper(data) -> dict:
    return data

def get_user_helper(data, flag) -> dict:
    if flag == 1:
        return {"email": data['email']}
    else:
        return {"_id": ObjectId(data['userid'])}

def update_user_helper(data):
    return data
