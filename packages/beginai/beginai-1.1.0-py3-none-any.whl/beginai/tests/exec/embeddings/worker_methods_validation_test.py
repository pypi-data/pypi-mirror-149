from .mock_service import BeginWorkerMock

APP_ID = 1
LICENSE_KEY = 10

def test_register_user_that_doesnt_exist_yet():
    user_id = 1231212
    bw = BeginWorkerMock(APP_ID, LICENSE_KEY)
    bw.register_user(user_id)
    assert bw.get_data().get("user") == { user_id: {}}

def test_register_user_when_user_already_exists_do_nothing():
    user_id = 1231212
    bw = BeginWorkerMock(APP_ID, LICENSE_KEY)

    bw.register_user(user_id)
    bw.register_user(user_id)
    assert bw.get_data().get("user") == { user_id: {}}


def test_register_user_more_than_one_user():
    user_id_1 = 1231212
    user_id_2 = 8888888
    bw = BeginWorkerMock(APP_ID, LICENSE_KEY)

    bw.register_user(user_id_1)
    bw.register_user(user_id_2)
    assert bw.get_data().get("user") == { user_id_1: {}, user_id_2: {}}

def test_update_user_text_field():
    user_id = 12312125
    value = 'Hello'
    bw = BeginWorkerMock(APP_ID, LICENSE_KEY)
    bw.register_user(user_id)
    bw.update_user_text_field(user_id, "text", value)

    expected = { user_id: { "text": value } }

    assert bw.get_data().get("user") == expected

def test_update_user_text_field_returns_error_when_value_provided_is_not_string():
    user_id = 12312125
    value = 123
    bw = BeginWorkerMock(APP_ID, LICENSE_KEY)
    bw.register_user(user_id)

    try:
        bw.update_user_text_field(user_id, "text", value)
    except ValueError:
        assert True

def test_update_user_text_field_returns_error_when_fields_are_not_provided():
    user_id = 12312125
    value = 'Hello'
    bw = BeginWorkerMock(APP_ID, LICENSE_KEY)
    bw.register_user(user_id)
    try:
        bw.update_user_text_field(None, "text", value)
    except ValueError:
        assert True

    try:
        bw.update_user_text_field(user_id, None, value)
    except ValueError:
        assert True

    try:
        bw.update_user_text_field(user_id, "text", None)
    except ValueError:
        assert True

def test_update_user_numerical_field():
    user_id = 12312125
    value = 10.0
    bw = BeginWorkerMock(APP_ID, LICENSE_KEY)
    bw.register_user(user_id)
    bw.update_user_numerical_field(user_id, "number", value)

    expected = { user_id: { "number": value } }

    assert bw.get_data().get("user") == expected

def test_update_user_numerical_field_when_fields_are_not_provided():
    user_id = 12312125
    value = 10
    bw = BeginWorkerMock(APP_ID, LICENSE_KEY)
    bw.register_user(user_id)
    try:
        bw.update_user_numerical_field(None, "number", value)
    except ValueError:
        assert True

    try:
        bw.update_user_numerical_field(user_id, None, value)
    except ValueError:
        assert True

    try:
        bw.update_user_numerical_field(user_id, "number", None)
    except ValueError:
        assert True

def test_update_user_numerical_field_returns_error_when_value_provided_is_not_number():
    user_id = 12312125
    value = "a"
    bw = BeginWorkerMock(APP_ID, LICENSE_KEY)
    bw.register_user(user_id)

    try:
        bw.update_user_numerical_field(user_id, "number", value)
    except ValueError:
        assert True

def test_update_user_date_field():
    user_id = 12312125
    date = '16-05-1991'
    bw = BeginWorkerMock(APP_ID, LICENSE_KEY)
    bw.register_user(user_id)
    bw.update_user_date_field(user_id, "userBirthDate", date)

    expected = { user_id: { "userbirthdate": date } }

    assert bw.get_data().get("user") == expected

def test_update_user_date_field_fails_when_the_user_is_not_registered():
    user_id = 12312125
    date = '16-05-1991'
    bw = BeginWorkerMock(APP_ID, LICENSE_KEY)

    try:
        bw.update_user_date_field(user_id, "userBirthDate", date)
    except ValueError:
        assert True

def test_update_user_date_field_fails_when_the_field_is_not_provided():
    user_id = 12312125
    date = '16-05-1991'
    bw = BeginWorkerMock(APP_ID, LICENSE_KEY)
    bw.register_user(user_id)

    try:
        bw.update_user_date_field(user_id, '', date)
    except ValueError:
        assert True

def test_update_user_date_field_fails_when_the_date_is_not_provided():
    user_id = 12312125
    bw = BeginWorkerMock(APP_ID, LICENSE_KEY)
    bw.register_user(user_id)

    try:
        bw.update_user_date_field(user_id, 'userBirthDate', None)
    except ValueError:
        assert True

def test_update_user_location_field():
    user_id = 1231212
    bw = BeginWorkerMock(APP_ID, LICENSE_KEY)
    bw.register_user(user_id)
    latitude = 36.8507689
    longitude =  -76.2858726

    bw.update_user_location_field(user_id, "userLocation", latitude, longitude)

    expected = { user_id: { "userlocation": { "latitude": latitude, "longitude": longitude} } }

    assert bw.get_data().get("user") == expected

def test_update_user_location_field_fails_when_user_id_not_registered():
    user_id = 1231212
    bw = BeginWorkerMock(APP_ID, LICENSE_KEY)
    latitude = 36.8507689
    longitude =  -76.2858726

    try:
        bw.update_user_location_field(user_id, "userLocation", latitude, longitude)
    except ValueError:
        assert True

def test_update_user_location_field_fails_when_field_name_not_provided():
    user_id = 1231212
    bw = BeginWorkerMock(APP_ID, LICENSE_KEY)
    latitude = 36.8507689
    longitude =  -76.2858726
    bw.register_user(user_id)

    try:
        bw.update_user_location_field(user_id, '', latitude, longitude)
    except ValueError:
        assert True

def test_update_user_location_field_fails_when_lat_long_not_provided():
    user_id = 1231212
    bw = BeginWorkerMock(APP_ID, LICENSE_KEY)
    latitude = 36.8507689
    longitude =  -76.2858726
    bw.register_user(user_id)

    try:
        bw.update_user_location_field(user_id, 'location', None, longitude)
    except ValueError:
        assert True

    try:
        bw.update_user_location_field(user_id, 'location', latitude, None)
    except ValueError:
        assert True


def test_register_object_without_object_name():
    bw = BeginWorkerMock(APP_ID, LICENSE_KEY)
    try:
        bw.register_object(object_name='', object_id=12)
    except ValueError:
        assert True

def test_register_object_without_object_id():
    bw = BeginWorkerMock(APP_ID, LICENSE_KEY)
    try:
        bw.register_object(object_name='name', object_id=None)
    except ValueError:
        assert True

def test_register_object():
    bw = BeginWorkerMock(APP_ID, LICENSE_KEY)
    object_name = 'Product'
    object_id = 10
    bw.register_object(object_name, object_id)

    expected = {
        object_name.lower() : { object_id: { }},
        "user": {},
        "interactions": {}
    }

    assert bw.get_data() == expected

def test_register_object_more_than_one():
    bw = BeginWorkerMock(APP_ID, LICENSE_KEY)
    object_name = 'Product'
    object_id_1 = 10
    object_id_2 = 20
    bw.register_object(object_name, object_id_1)
    bw.register_object(object_name, object_id_2 )

    expected = {
        object_name.lower() : { object_id_1: { }, object_id_2: { } },
        "user": {},
        "interactions": {}
    }

    assert bw.get_data() == expected

def test_update_object_text_field_when_object_not_registered():
    bw = BeginWorkerMock(APP_ID, LICENSE_KEY)
    object_name = 'Product'
    object_id = 10
    field = "bio"
    value = "test test"

    try:
        bw.update_object_text_field(object_name, object_id, field, value)
    except ValueError:
        assert True

def test_update_object_text_field_when_value_is_not_string():
    bw = BeginWorkerMock(APP_ID, LICENSE_KEY)
    object_name = 'Product'
    object_id = 10
    field = "bio"
    value = 10
    bw.register_object(object_name, object_id)

    try:
        bw.update_object_text_field(object_name, object_id, field, value)
    except ValueError:
        assert True

def test_update_object_text_field_when_object_parameters_not_provided():
    bw = BeginWorkerMock(APP_ID, LICENSE_KEY)
    object_name = 'Product'
    object_id = 10
    field = "bio"
    value = "test test"

    try:
        bw.update_object_text_field('', object_id, field, value)
    except ValueError:
        assert True

    bw.register_object(object_name, object_id)
    
    try:
        bw.update_object_text_field(object_name, None, field, value)
    except ValueError:
        assert True

    try:
        bw.update_object_text_field(object_name, object_id, None, value)
    except ValueError:
        assert True

    try:
        bw.update_object_text_field(object_name, object_id, field, None)
    except ValueError:
        assert True

def test_update_object_text_field_when_object_id_not_registered():
    bw = BeginWorkerMock(APP_ID, LICENSE_KEY)
    object_name = 'Product'
    object_id_exists = 10
    object_id_doesnt_exist = 20
    field = "bio"
    value = "test test"

    bw.register_object(object_name, object_id_exists)

    try:
        bw.update_object_text_field(object_name, object_id_doesnt_exist, field, value)
    except ValueError:
        assert True

def test_update_object_numerical():
    bw = BeginWorkerMock(APP_ID, LICENSE_KEY)
    object_name = 'Product'
    object_id = 10
    field = "bio"
    value = 10
    bw.register_object(object_name, object_id)

    bw.update_object_numerical_field(object_name, object_id, field, value)
    assert bw.get_data().get(object_name.lower()).get(object_id) == { field: value}

def test_update_object_numerical_field_when_value_is_not_valid():
    bw = BeginWorkerMock(APP_ID, LICENSE_KEY)
    object_name = 'Product'
    object_id = 10
    field = "bio"
    value = "10"
    bw.register_object(object_name, object_id)

    try:
        bw.update_object_numerical_field(object_name, object_id, field, value)
    except ValueError:
        assert True

def test_update_object_text_field():
    bw = BeginWorkerMock(APP_ID, LICENSE_KEY)
    object_name = 'Product'
    object_id = 10
    field = "bio"
    value = "test test"

    bw.register_object(object_name, object_id)

    bw.update_object_text_field(object_name, object_id, field, value)

    assert bw.get_data().get(object_name.lower()).get(object_id) == { field: value}

def test_update_object_date_field():
    bw = BeginWorkerMock(APP_ID, LICENSE_KEY)
    object_name = 'Product'
    object_id = 10
    field = "date"
    value = "10-10-1991"

    bw.register_object(object_name, object_id)

    bw.update_object_date_field(object_name, object_id, field, value)

    assert bw.get_data().get(object_name.lower()).get(object_id) == { field: value}


def test_register_interaction_without_user_id():
    bw = BeginWorkerMock(APP_ID, LICENSE_KEY)
    try:
        bw.register_interaction(user_id = '', object_name='', object_id=1, action='like')
    except ValueError:
        assert True

def test_register_interaction_without_object_name():
    bw = BeginWorkerMock(APP_ID, LICENSE_KEY)
    try:
        bw.register_interaction(user_id = 1, object_name='', object_id=1, action='like')
    except ValueError:
        assert True

def test_register_interaction_without_object_id():
    bw = BeginWorkerMock(APP_ID, LICENSE_KEY)
    try:
        bw.register_interaction(user_id = 1, object_name='product', object_id=None, action='like')
    except ValueError:
        assert True

def test_register_interaction_without_action_id():
    bw = BeginWorkerMock(APP_ID, LICENSE_KEY)
    try:
        bw.register_interaction(user_id = 1, object_name='product', object_id=1, action='')
    except ValueError:
        assert True

def test_register_interaction_with_the_same_product_id():
    bw = BeginWorkerMock(APP_ID, LICENSE_KEY)
    object_name = "product"
    object_id = 10
    user_id = 1

    bw.register_interaction(user_id, object_name, 'like', object_id)
    bw.register_interaction(user_id, object_name, 'dislike', object_id)

    results = bw.get_data().get('interactions').get(user_id).get(object_name)

    assert results == { object_id: [ 'like', 'dislike' ]}

def test_register_interaction_with_different_product_id():
    bw = BeginWorkerMock(APP_ID, LICENSE_KEY)
    object_name = "product"
    object_id_one = 10
    object_id_two = 20
    user_id = 1

    bw.register_interaction(user_id, object_name, 'LIKE', object_id_one)
    bw.register_interaction(user_id, object_name, 'DISLIKE', object_id_two)

    results = bw.get_data().get('interactions').get(user_id).get(object_name)
    assert results == { object_id_one: [ 'like' ], object_id_two: ['dislike']}

def test_add_label_for_user():
    bw = BeginWorkerMock(APP_ID, LICENSE_KEY)
    object_name = "user"
    object_id = 10
    label = 'test'

    bw.register_user(object_id)
    bw.add_label(object_name, object_id, label)

    results = bw.get_data().get('user')
    assert results == { 
        object_id: {
            "labels": [label]
        }
    }

def test_add_more_than_one_label_for_user():
    bw = BeginWorkerMock(APP_ID, LICENSE_KEY)
    object_name = "user"
    object_id = 10
    label = 'test'
    label_2 = 'test_2'

    bw.register_user(object_id)
    bw.add_label(object_name, object_id, label)
    bw.add_label(object_name, object_id, label_2)

    results = bw.get_data().get('user')
    assert results == { 
        object_id: {
            "labels": [label, label_2]
        }
    }


def test_add_more_than_one_label_for_different_object():
    bw = BeginWorkerMock(APP_ID, LICENSE_KEY)
    object_name = "book"
    object_id = 20
    label = 'test'
    label_2 = 'test_2'

    bw.register_user(10)
    bw.add_label("user", 10, label)
    bw.add_label("user", 10, label_2)

    bw.register_object(object_name, object_id)
    bw.add_label(object_name, object_id, 'object_label')

    results = bw.get_data()
    assert results == {'user': {10: {'labels': ['test', 'test_2']}}, 'interactions': {}, 'book': {20: {'labels': ['object_label']}}}

def test_add_label_validation_when_object_not_registered():
    bw = BeginWorkerMock(APP_ID, LICENSE_KEY)
    try:
        bw.add_label(object_id=1, object_name='user', label='test')
    except ValueError:
        assert True

def test_add_label_validation_when_label_not_provided():
    bw = BeginWorkerMock(APP_ID, LICENSE_KEY)
    bw.register_user(1)
    try:
        bw.add_label(object_id=1, object_name='user', label='')
    except ValueError:
        assert True
