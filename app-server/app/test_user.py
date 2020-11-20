import requests
from rich.console import Console


BASE_URL = 'http://localhost:5000'
VALID_USER = {'name': 'Steve-77', 'age': 66}
NOT_VALID_USER = {'names': 'not_Steve-999', 'age': 999}
UPDATED_USER = {'name': 'Jobs-UPDATED', 'age': 7}

console = Console()


# 1
def test_user_create_base():
    # user = {'name': 'Steve-0', 'age': 3}
    # REQUESTs will change dict {'user': user} to JSON
    response = requests.post(f'{BASE_URL}/user', json={'user': VALID_USER})

    assert response.status_code == 201


# 2
def test_user_create_not_json():
    # user = {'name': 'Steve-1', 'age': 13}
    response = requests.post(f'{BASE_URL}/user', data={'user': VALID_USER})     # HERE: 'data={...}' - means 'table data', NOT json

    assert response.status_code == 422


##############################################################################

# THE FOLLOWING TEST CHECKS IS UUID OF THE USER MATCHES 'UUID PATTERN/RULES'
# BUT WE CEASE TO USE UUID AFTER WE SWITCH TO DATABASES/TABLES
# NOW WE USE JUST SEQUESCE OF INTEGER AS USER IDENTIFIER

# 3
# def test_user_create_check_uuid():
#     response = requests.post(f'{BASE_URL}/user', json={'user': VALID_USER})

#     user_id = response.json()['user_id']

#     assert type(UUID(user_id)) is UUID

#######################################################################################################################

# QUESTION: Is it better to just pass 'user_id' from prev func?? And HOW??
# ANSWER: Better to create user again (because we do 'pytest')...
# ...If it was a regular code then it would better  to create a class
# ALSO See: https://stackoverflow.com/questions/49238725/chaining-tests-and-passing-an-object-from-one-test-to-another

#######################################################################################################################


# 3
def test_user_read_correct_name_age():
    response = requests.post(f'{BASE_URL}/user', json={'user': VALID_USER})
    user_id = response.json()['user_id']

    console.log(f'user_id = {user_id}', log_locals=True)

    response = requests.get(f'{BASE_URL}/user/{user_id}')

    # console.log(f'URL = {response.url}', log_locals=True)

    console.log(f'response = {response.json()}', log_locals=True)
    # console.log(f"response['user'] = {response['user']}", log_locals=True)

    # assert response.status_code == 200
    assert response.json()['user']['name'] == VALID_USER['name']
    assert response.json()['user']['age'] == VALID_USER['age']
    # assert response['user']['name'] == VALID_USER['name']
    # assert response['user']['age'] == VALID_USER['age']


# 4
def test_user_update_is_not_json():
    response = requests.post(f'{BASE_URL}/user', json={'user': VALID_USER})

    # console.log(f'URL = {response.url}', log_locals=True)

    user_id = response.json()['user_id']

    # console.log(f'user_id = {user_id}', log_locals=True)

    response = requests.patch(f'{BASE_URL}/user/{user_id}', data={'user': UPDATED_USER})

    assert response.status_code == 422


# 5
def test_user_update_user_is_not_valid():

    response = requests.post(f'{BASE_URL}/user', json={'user': VALID_USER})

    # console.log(f'URL = {response.url}', log_locals=True)

    user_id = response.json()['user_id']

    # console.log(f'user_id = {user_id}', log_locals=True)

    response = requests.patch(f'{BASE_URL}/user/{user_id}', json={'users': VALID_USER})

    assert response.status_code == 422


# 6
def test_user_update_user_name_or_age_is_not_valid():

    response = requests.post(f'{BASE_URL}/user', json={'user': VALID_USER})
    user_id = response.json()['user_id']

    response = requests.patch(f'{BASE_URL}/user/{user_id}', json={'user': NOT_VALID_USER})

    assert response.status_code == 422


# 7
def test_user_update_user_not_found():

    response = requests.post(f'{BASE_URL}/user', json={'user': VALID_USER})
    user_id = response.json()['user_id']

    response = requests.patch(f'{BASE_URL}/user/{user_id + 1}', json={'user': VALID_USER})

    assert response.status_code == 404


# 8
# TEMP TEST FOR USER # 2
def test_user_update_correct_update():

    response = requests.post(f'{BASE_URL}/user', json={'user': VALID_USER})
    user_id = response.json()['user_id']

    response = requests.patch(f'{BASE_URL}/user/{user_id}', json={'user': UPDATED_USER})

    assert response.status_code == 200


# 9
def test_user_delete_no_user_found():
    response = requests.post(f'{BASE_URL}/user', json={'user': VALID_USER})
    user_id = response.json()['user_id']

    user_id += 789
    response = requests.delete(f'{BASE_URL}/user/{user_id}')

    console.log(f'URL = {response.url}', log_locals=True)
    console.log(f'user_id = {user_id}', log_locals=True)

    assert response.status_code == 404


# 10
# TEMP TEST FOR USER # 2
def test_user_delete_user_deleted():
    response = requests.post(f'{BASE_URL}/user', json={'user': VALID_USER})
    user_id = response.json()['user_id']

    response = requests.delete(f'{BASE_URL}/user/{user_id}')

    assert response.status_code == 200


# 11
def test_user_authenticate_success():
    response = requests.post(f'{BASE_URL}/user_authenticate', json={'login': 'abc', 'password': '123'})

    console.log('dsfwrgewrgewt', log_locals=True)

    assert response.status_code == 200


#################################

# TODO: FIMISH @ TESTS

#################################


# 12
def test_create_user_success():
    # response = requests.post(f'{BASE_URL}/user', json={'IP': '170.6.12.88'})
    pass


# 13
def test_create_user_fail():
    pass
