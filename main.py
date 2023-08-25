# # This is a sample Python script.
#
# # Press Shift+F10 to execute it or replace it with your code.
# # Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
#
#
# def print_hi(name):
#     # Use a breakpoint in the code line below to debug your script.
#     print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.
#
#
# # Press the green button in the gutter to run the script.
# if __name__ == '__main__':
#     print_hi('PyCharm')
#
# # See PyCharm help at https://www.jetbrains.com/help/pycharm/


from fastapi import FastAPI, Response, Path, Query
from fastapi.responses import PlainTextResponse, HTMLResponse, FileResponse

# Запуск сервера: uvicorn main:app --reload
# http://127.0.0.1:8000
#
# Автоматическая документация API: http://127.0.0.1:8000/docs.
# На этой странице находится интерактивная документация по API
#
# Альтернативная документация API: http://127.0.0.1:8000/redoc
#
# чистая схема OpenAPI: http://127.0.0.1:8000/openapi.json
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Главная страница"}


@app.get("/about")
async def about():
    return {"message": "О сайте"}


@app.get("/response")
async def response():
    data = "Пример простого текста. Класс fastapi.Response."
    return Response(content=data, media_type="text/plain")  # from fastapi import Response


# Примеры отправки ответов серверу

@app.get("/PlainTextResponse")
async def text_simple():
    data = "Пример простого текста. Используем класс-наследник" + \
           " PlainTextResponse для класса fastapi.Response."
    return PlainTextResponse(content=data)  # from fastapi.responses import PlainTextResponse


@app.get("/HTMLResponse")
async def text_html():
    data = "<h2>Пример отправки кода html.</h2> <p>Используем класс-наследник" + \
           " PlainTextResponse для класса fastapi.Response.<p>"
    return HTMLResponse(content=data)  # from fastapi.responses import HTMLResponse


@app.get("/FileResponse")
def send_file():
    return FileResponse("FileResponse.html")  # from fastapi.responses import FileResponse


# альтернативный вариант отправки ответов серверу

@app.get("/PlainTextResponse-default", response_class=PlainTextResponse)
async def text_simple_default():
    data = "Пример простого текста (Установка типа ответа " + \
           "через методы FastAPI).\nИспользуем класс-наследник" + \
           " PlainTextResponse для класса fastapi.Response."
    return data  # from fastapi.responses import PlainTextResponse


@app.get("/HTMLResponse-default", response_class=HTMLResponse)
async def text_html_default():
    data = "<h2>Пример отправки кода html.</h2> <p>Установка типа " + \
           "ответа через методы FastAPI.<br>Используем класс-наследник" + \
           " PlainTextResponse для класса fastapi.Response.<p>"
    return data  # from fastapi.responses import HTMLResponse


@app.get("/FileResponse-default", response_class=FileResponse)
def send_file_default():
    return "FileResponse_default.html"


# Конец альтернативного варианта отправки ответов серверу


# В данном случае функция users обрабатывает запросы, путь
# которых соответствует шаблону "/users/{name}/{age}"
# Tакому шаблону соответствовал бы запрос по
# пути http://127.0.0.1:8000/users/Tom/38
@app.get("/users/{name}/{age}")
def users_slash(name, age):
    return {"user_name": name, "user_age": age}


# В данном случае функция users обрабатывает запросы, путь
# которых соответствует шаблону "/users/{name}-{age}"
# Tакому шаблону соответствовал бы запрос по
# пути http://127.0.0.1:8000/users/Tom-38
@app.get("/users/{name}-{age}")
def users_dash(name, age):
    return {"user_name": name, "user_age": age}


@app.get("/users_id/{user_id}")
def users_id(user_id: int):
    return {"user_id": user_id}


@app.get("/users_name/{user_name}")
def users_name(user_name: str = Path(min_length=3, max_length=20)):  # from fastapi import Path
    return {"name": user_name}


@app.get("/users")
def users(name: str = "Undefined", age=18):
    return {"user_name": name, "user_age": age}


@app.get("/users_query")
def users_query(name: str = Query(default="Undefined",
                                  min_length=3,
                                  max_length=20),
                age: int = 18):  # from fastapi import Query
    return {"name": name, "age": age}


@app.get("/users_none")
def users_none(name: str | None = Query(default=None,
                                        min_length=2),
               age: int | None = Query(default=None)):
    # if name == None:
    # if name is None:
    #     return {"name": "Undefined"}
    # else:
    #     return {"name": name}
    if name is None:
        data = {"name": "Undefined"}
    else:
        data = {"name": name}

    if age is None:
        data["age"] = 0
    else:
        data["age"] = age

    return data


@app.get("/users_list")
def users_list(people: list[str] = Query()):
    return {"people": people}


@app.get("/users_name_query/{name}")
def users_name_query(name: str = Path(min_length=3, max_length=20),
                     age: int = Query(ge=18, lt=111)):
    return {"name": name, "age": age}
