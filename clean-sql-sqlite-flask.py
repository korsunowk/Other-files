def get_db():
    """
    Helper function for create connection with database
    and return database connection object for use one
    :return: database connection object
    """
    db = getattr(g, '_database', None)
    if not db:
        db = g._database = sqlite3.connect(settings.DATABASE)
    return db


@app.teardown_appcontext
def close_connection(exception):
    """
    Helper function for close connection with database
    :param exception: exception which send flask app
    """
    db = getattr(g, '_database', None)
    if db:
        db.close()


def write_purchase_hash_to_db(purchase, hash_code):
    """
    Function for write new purchase hash code to database
    """
    cursor = get_db().cursor()
    sql = "UPDATE purchases SET purchase_hash='{0}' WHERE ID={1}"\
          .format(hash_code, purchase)
    cursor.execute(sql)
    get_db().commit()


def write_purchase_to_db(data):
    """
    Function for write new purchase information to database
    :param data: all information about purchase
    """
    payment = data.get('payment')
    cursor = get_db().cursor()
    sql = "INSERT INTO purchases (operation, email, name, " \
          "country, document, zipcode, address, street_number, " \
          "city, state, phone_number, birth_date, " \
          "currency_code, amount_total, payment_type_code)" \
          " VALUES ('{0}', '{1}', '{2}', '{3}'," \
          "'{4}', '{5}', '{6}', '{7}'," \
          "'{8}', '{9}', '{10}', '{11}'," \
          "'{12}', '{13}', '{14}')"\
        .format(
            data.get('operation'), payment.get('email'), payment.get('name'),
            payment.get('country'), payment.get('document'),
            payment.get('zipcode'), payment.get('address'),
            payment.get('street_number'), payment.get('city'),
            payment.get('state'), payment.get('phone_number'),
            payment.get('birth_date'), payment.get('currency_code'),
            payment.get('amount_total'), payment.get('payment_type_code')
        )
    cursor.execute(sql)

    return cursor.lastrowid


@app.teardown_appcontext
def create_database_table(exception):
    """
    Create initial database table for save info about purchases
    """
    sql = """
        CREATE TABLE IF NOT EXISTS purchases (
             ID INTEGER PRIMARY KEY autoincrement,
             purchase_hash string,
             card_token string,
             operation string,
             email string,
             name string,
             country string,
             document string,
             zipcode string,
             address string,
             street_number string,
             city string,
             state string,
             phone_number string,
             birth_date string,
             currency_code string,
             amount_total string,
             payment_type_code string
            );
    """

    get_db().execute(sql)
    get_db().commit()


def write_card_token_to_db(purchase_id, token):
    """
    Function for write new token of card to database
    """
    sql = "UPDATE purchases SET card_token='%s' WHERE ID=%d" \
          % (token, purchase_id)
    get_db().execute(sql)
    get_db().commit()


def get_purchase_data_from_db(purchase_id):
    """
    Get all information about purchase from database
    :param purchase_id: INT id of purchase
    :return: all information from database about that purchase
    """
    cursor = get_db().cursor()
    cursor.execute(
        "SELECT * FROM purchases WHERE ID=%s" % purchase_id)
    return cursor.fetchone()



def get_purchase_hash_from_db(purchase_id):
    """
    Helper function for get purchase object from database

    :param purchase_id: INT id of purchase object
    :return: database row with purchase object
    """
    cursor = get_db().cursor()
    sql = "SELECT purchase_hash FROM purchases WHERE ID=%s" % purchase_id
    cursor.execute(sql)
    return cursor.fetchone()[0]


def get_purchase_amount_from_db(purchase_id):
    """
    Helper function for get purchase amount from database
    :param purchase_id: INT id of purchase object
    :return: purchase.amount from database row
    """
    cursor = get_db().cursor()
    sql = "SELECT amount_total FROM purchases WHERE ID=%s" % purchase_id
    cursor.execute(sql)
    return cursor.fetchone()[0]
