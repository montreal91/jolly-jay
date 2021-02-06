
program0 = """BEGIN END."""

program1 = """\
BEGIN

    BEGIN
        number := 2;
        a := number;
        b := 10 * a + 10 * number / 4;
        c := a - - b
    END;

    x := 11;
END.
"""

program1_case_insensitive = """\
Begin

    begin
        Number := 2;
        a := NUMBER;
        b := 10 * a + 10 * number / 4;
        c := A - - B
    end;

    x := 11;
END.
"""
