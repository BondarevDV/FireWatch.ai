
def get_db_session():
    """Фейковый генератор сессии БД"""
    print("--> Yielding fake DB session")
    yield "fake_db_session_object"
    print("<-- Closing fake DB session")