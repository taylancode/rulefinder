from rulefinder.rulefinder import Rulefinder
from rulefinder.sqlmanager import SQL
from rulefinder.constants import FW, PA_KEY, DGROUPS

def update_values(db: None, dgrp: str) -> None:
    '''
    Simple function to update the Database with the rules

    :param db: Database class object
    :param dgrp: String containing device group
    '''
    
    # Calling the update db function that handles the data iteration and SQL table update
    finder = Rulefinder(host=FW, key=PA_KEY, dgrp=dgrp)
    attrs = finder.update_db()

    for attr in attrs:
        print(attr)
        db.excecute_sql(
            "INSERT INTO"
            " securityrules (rule_id, dgrp, rulename, fromzone, tozone, sourceip, sourceusr, "
            "destip, category, application, service, negatesrc, negatedest, action, disabled)"
            " VALUES ("
            f"'{attr['uuid']}',"
            f"'{attr['dgrp']}',"
            f"'{attr['name']}',"
            f"ARRAY{attr['from']},"
            f"ARRAY{attr['to']},"
            f"ARRAY{attr['source']},"
            f"ARRAY{attr['source-user']},"
            f"ARRAY{attr['destination']},"
            f"ARRAY{attr['category']},"
            f"ARRAY{attr['application']},"
            f"ARRAY{attr['service']},"
            f"{attr['negate-source']},"
            f"{attr['negate-destination']},"
            f"'{attr['action']}',"
            f"{attr['disabled']})")

def recreate_table() -> None:
    db_con = SQL()
    # Re-make the table before running the update
    db_con.excecute_sql(sql=
        """DROP TABLE IF EXISTS securityrules;

        CREATE TABLE securityrules (
        rule_id UUID PRIMARY KEY,
        rulename TEXT,
        dgrp TEXT,
        fromzone TEXT[],
        tozone TEXT[],
        sourceip TEXT[],
        sourceusr TEXT[],
        destip TEXT[],
        category TEXT[],
        application TEXT[],
        service TEXT[],
        negatesrc BOOLEAN NOT NULL,
        negatedest BOOLEAN NOT NULL,
        action TEXT NOT NULL,
        disabled BOOLEAN NOT NULL);

        commit""")

    for dgrp in DGROUPS:
        update_values(db=db_con, dgrp=dgrp)

    db_con.close_connect(close_cur=True, close_DB=True, commit=True)

if __name__ == '__main__':
    recreate_table()
