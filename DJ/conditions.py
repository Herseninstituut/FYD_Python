import datajoint as dj
schema = dj.schema('socialbrainlab')

@schema
class Conditions(dj.Manual):
    definition = '''
    conditionid : varchar(30)   # unique name
    ---
    idx : int(3) auto_increment
    shortdescr : varchar(250)
    longdescr : varchar(3000)
    '''
