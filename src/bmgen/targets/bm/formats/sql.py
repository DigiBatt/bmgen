from bmgen.targets.bm.helper.sql import string_to_sql, int_to_sql
from dataclasses import dataclass
import typing


@dataclass
class Row:
    iStepNo: int
    iNumeration: int
    csLabel: str | None
    csOperator: str | None
    csSetPoint: str | None
    csCircuitValue: str | None
    csBreakOff: str | None
    csRegistration: str | None
    csComment: str | None
    iGoto: int | None

    def toSql(self, programId: int | str):
        return f"({programId}, {self.iStepNo}, {self.iNumeration}, {string_to_sql(self.csLabel)}, {string_to_sql(self.csOperator)}, {string_to_sql(self.csSetPoint)}, {string_to_sql(self.csCircuitValue)}, {string_to_sql(self.csBreakOff)}, {string_to_sql(self.csRegistration)}, {string_to_sql(self.csComment)}, {int_to_sql(self.iGoto)})"

    @staticmethod
    def fromSql(values) -> "Row":
        return Row(*values[2:])


@dataclass
class StepRows:
    rows: typing.List[Row]

    def toSql(self, programId: int | str):
        return ",\n".join([r.toSql(programId) for r in self.rows])


@dataclass
class Program:
    rows: typing.List[StepRows]

    def toSql(self, programName: str):
        sql = f"""DECLARE @ProgramID int;
DECLARE @ProgramNumber int;
DECLARE @Version int;
SELECT TOP 1 @Version = iVersion + 1, @ProgramNumber = iProgramNo FROM tblProgramReferences WHERE csProgramName = '{programName}' ORDER BY iVersion DESC;
IF @ProgramNumber IS NULL
BEGIN
	SET @Version = 1;
	SELECT @ProgramNumber = MAX(iProgramNo) + 1 FROM tblProgramReferences;
	IF @ProgramNumber IS NULL
	BEGIN
		SET @ProgramNumber = 1;
	END
END
INSERT INTO tblProgramReferences (System, iProgramNo, iProgramType, dCapacity, dDuration, csProgramName, csComment, csCommentFile, tCreationTime, tModificationTime, iVersion, iDelete, iCertificated, tChangeCertificatedDate, bChecked) VALUES(8, @ProgramNumber, 0, 0, 0, '{programName}', null, null, GETDATE(), GETDATE(), @Version, 0, 0, GETDATE(), 1);
SET @ProgramID = @@IDENTITY;
INSERT INTO tblProgramDetail (iProgramID, iStepNo, iNumeration, csLabel, csOperator, csSetPoint, csCircuitValue, csBreakOff, csRegistration, csComment, iGoto) VALUES
"""
        for i in range(len(self.rows)):
            if i > 0:
                sql += ","
            sql += "\n" + self.rows[i].toSql("@ProgramID")

        sql += ";"
        return sql

    @staticmethod
    def fromSql(values):
        steprows = []
        rows = []
        for v in values:
            r = Row.fromSql(v)
            if r.iNumeration == 0 and len(rows) > 0:
                steprows.append(StepRows(rows))
                rows = []
            rows.append(r)
        if len(rows) > 0:
            steprows.append(StepRows(rows))
        return Program(steprows)
