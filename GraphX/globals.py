_engine = None

def get_engine():
    global _engine
    return _engine

def set_engine(engine):
    global _engine
    _engine = engine