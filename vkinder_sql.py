import psycopg2 as pg

def partner_raw_weight_database():
    with pg.connect(database = 'vkinder', user = 'vinder', password = 'vinder', host = 'localhost', port = 5432) as conn:
        pass

def partner_current_weight():
    pass

def best_partner():
    pass

def previous_search():
    pass

