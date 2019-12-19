from bson.objectid import ObjectId


def str_to_objectid(str_id):
    try:
        object_id = ObjectId(str_id)
    except:
        raise ValueError('{} is not a valid ObjectId'.format(str_id))
    else:
        return object_id


def is_valid_object_id(str_id):
    try:
        ObjectId(str_id)
    except:
        raise ValueError('{} is not a valid ObjectId'.format(str_id))
    else:
        return str_id


def greater_than_zero(num):
    try:
        num = int(num)
    except:
        raise ValueError(f'{num} cannot convert to int')
    else:
        if num <= 0:
            raise ValueError(f'{num} must be greater than 0')
        return num


def greater_equal_zero(num):
    try:
        num = int(num)
    except:
        raise ValueError(f'{num} cannot convert to int')
    else:
        if num < 0:
            raise ValueError(f'{num} cannot less than 0')
        return num

