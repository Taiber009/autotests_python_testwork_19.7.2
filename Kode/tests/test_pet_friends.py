from api import PetFriends
from settings import valid_email, valid_password
import os

pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """Проверяем что запрос api ключа возвращает статус 200 и в тезультате содержится слово key"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 200
    assert "key" in result


def test_get_all_pets_with_valid_key(filter=""):
    """Проверяем что запрос всех питомцев возвращает не пустой список.
    Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя этого ключ
    запрашиваем список всех питомцев и проверяем что список не пустой.
    Доступное значение параметра filter - 'my_pets' либо ''"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result["pets"]) > 0


def test_add_new_pet_with_valid_data(
    name="Барбоскин", animal_type="двортерьер", age="4", pet_photo="images\\1234.png"
):
    """Проверяем что можно добавить питомца с корректными данными"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result["name"] == name


def test_successful_update_self_pet_info(name="Мурзик", animal_type="Котэ", age=5):
    # sourcery skip: raise-specific-error
    """Проверяем возможность обновления информации о питомце"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Еслди список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets["pets"]) > 0:
        status, result = pf.update_pet_info(
            auth_key, my_pets["pets"][0]["id"], name, animal_type, age
        )

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result["name"] == name
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")


def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets["pets"]) == 0:
        pf.add_new_pet(auth_key, "Суперкот", "кот", "3", "images\\1234.png")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets["pets"][0]["id"]
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()


# ------------------------------------------------------------------
# --------------------------МОИ ТЕСТЫ-------------------------------
# ------------------------------------------------------------------
def test_add_new_pet_simple_with_valid_data(
    name="Барбоскин", animal_type="двортерьер", age="4"
):
    """Проверяем что можно добавить питомца с корректными данными без фото"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_simple(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result["name"] == name


def test_add_photo_with_valid_data(pet_photo="images\\1234.png"):
    """Проверяем что можно добавить фото питомца с корректными данными"""
    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets["pets"]) == 0:
        pf.add_new_pet(auth_key, "Суперкот", "кот", "3", "images\\1234.png")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и обновляем его фото
    pet_id = my_pets["pets"][0]["id"]
    status, result = pf.set_photo(auth_key, pet_id, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 500
    # Сергей Рудик
    # 13:39
    # Ольга Карпова
    # @rudik, Сергей, добрый день! Такой вопрос: если при реализации метода добавления фото поставить некорректный id, то я ожидаю увидеть ошибку 400, но выдает ошибку 500. Почему так? Могу я сделать тест на ошибку 500? (в этом случае проходит)
    # Делайте валидацию на 500, если так реагирует сервис сейчас


def test_add_new_pet_with_1px_photo(
    name="Барбоскин", animal_type="двортерьер", age="4", pet_photo="images\\1236.png"
):
    """Проверяем что можно добавить питомца с фото из 1 пикселя"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result["name"] == name


def test_add_new_pet_with_4к_photo(
    name="Барбоскин", animal_type="двортерьер", age="4", pet_photo="images\\1235.png"
):
    """Проверяем что можно добавить питомца с 4k фото""" #8k не влез в github

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result["name"] == name


def test_add_new_pet_simple_with_empty_data(name="", animal_type="", age=""):
    """Проверяем что можно добавить питомца с пустыми данными без фото"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_simple(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result["name"] == name


def test_add_new_pet_simple_with_50_symbol(
    name="QrcOdГцTPRggSW5lИЛШcPyoK0ERCVB5ZT8DzHYжfUPGKA7Jya7",
    animal_type="QrcOdГцTPRggSW5lИЛШcPyoK0ERCVB5ZT8DzHYжfUPGKA7Jya7",
    age="",
):
    """Проверяем что можно добавить питомца с именем из 50 разных символов"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_simple(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result["name"] == name


def test_add_new_pet_simple_with_255_symbol(
    name="ЗLСOFjpYШоWЭrмAЯKВmWBцMJцzGтшPqшnDЙDзФГгиМCeпСghGёcTЕЪYHяёдУжЩЙжМdиЛGbГQfшIUГjWлMnЯCЗлЫЬcuюSЯкrхJЖSfsjХЦXЛКIТЗъGLЯУdFХрОЖШоИVвТvBtШvУАKЫюЛWOeЖzЮГзRnyТВжcЫзеQiEpoтwUVхвГaиABдиCУULйrюЖoгСзЫZlgтVёIrHлкIITctHzШЖоМqмЫCЧяGтбсхBБЭёwkфVoKЙkщЮsУdЁэvмеHЖЬTTXбJvЭCLD",
    animal_type="ЗLСOFjpYШоWЭrмAЯKВmWBцMJцzGтшPqшnDЙDзФГгиМCeпСghGёcTЕЪYHяёдУжЩЙжМdиЛGbГQfшIUГjWлMnЯCЗлЫЬcuюSЯкrхJЖSfsjХЦXЛКIТЗъGLЯУdFХрОЖШоИVвТvBtШvУАKЫюЛWOeЖzЮГзRnyТВжcЫзеQiEpoтwUVхвГaиABдиCУULйrюЖoгСзЫZlgтVёIrHлкIITctHzШЖоМqмЫCЧяGтбсхBБЭёwkфVoKЙkщЮsУdЁэvмеHЖЬTTXбJvЭCLD",
    age="",
):
    """Проверяем что можно добавить питомца с именем из 255 разных символов"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_simple(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result["name"] == name

def test_add_new_pet_simple_with_chinese(
    name="龍門大酒家",
    animal_type="龍門大酒家",
    age="",
):
    """Проверяем что можно добавить питомца с именем из китайских символов"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_simple(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result["name"] == name

def test_add_new_pet_simple_with_arab(
    name="صسغذئآ",
    animal_type="صسغذئآ",
    age="",
):
    """Проверяем что можно добавить питомца с именем из арабских символов"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_simple(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result["name"] == name

def test_add_new_pet_simple_with_string_age(
    name="",
    animal_type="",
    age="ОДМЕН Я ВЗЛАМАЛ ТВОЙ СИРВАК АХАХАХАХАХАХАХАХ",
):
    """Проверяем что можно добавить питомца со буквенным возрастом"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_simple(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200 #тут должна быть ошибка?
    assert result["name"] == name

def test_add_new_pet_simple_with_injection(
    name="; drop table users; \"; drop table users;\"\"; drop table users;\");drop table users;",
    animal_type="; drop table pets;\"; drop table pets;\"'; DROP TABLE pets; -- ",
    age="; DROP TABLE users; -- ",
):
    """Проверяем что можно добавить питомца с SQL-инъекцией и ничего не упадет"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_simple(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result["name"] == name