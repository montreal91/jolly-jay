
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

program1_integer_div = """\
Begin

    begin
        Number := 2;
        a := NUMBER;
        b := 10 * a + 10 * number div 4;
        c := A - - B
    end;

    x := 11;
END.
"""

program_with_underscore_id = """
BEGIN
    _x_ := 42
END.
"""
