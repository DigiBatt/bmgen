#! /usr/bin/env python3

import pandas as pd
from sqlalchemy import create_engine, text
from bmgen.targets.bm.formats.sql import Program
from bmgen.targets.bm.converters.sql2bm import SQL2BM
import sys


# Import a BM program from the databse. If version is None, use the newest one.
def import_bm_sql(url, programName, version=None):
    if version is not None:
        raise NotImplementedError()
    query = text("""select tblProgramDetail.* from tblProgramDetail join
    (select max(ID) as ID, csProgramName from tblProgramReferences group by csProgramName) sq on tblProgramDetail.iProgramID = sq.ID
    where sq.csProgramName = :programName
    order by iStepNo, iNumeration""")

    engine = create_engine(url)
    with engine.connect() as conn:
        result = conn.execute(query, parameters={"programName": programName})
        program = Program.fromSql(result)
    bm = SQL2BM().convert(program)
    print(bm.toText())


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: import_bm_sql.py <database url> <program name>")
        sys.exit(1)

    url = sys.argv[1]
    programName = sys.argv[2]
    import_bm_sql(url, programName)
