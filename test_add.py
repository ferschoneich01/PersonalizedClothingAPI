import requests

url = "http://localhost:8080/api/users/add"
data = {
    "username": "testuser99",
    "password": "testpass",
    "email": "test99@test.com",
    "cedula": "123-123-123",
    "name": "Test",
    "lastname": "User",
    "birthday": "1990-01-01",
    "phone": "12345678",
    "city": "Managua",
    "sex": "M"
}

response = requests.post(url, json=data)
print(response.status_code)
print(response.text)
