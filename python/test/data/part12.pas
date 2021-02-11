PROGRAM Part12;
VAR
   a : INTEGER;

PROCEDURE P1;
VAR
   a : REAL;
   k : INTEGER;

   PROCEDURE P2;
   VAR
      a, z : INTEGER;
   BEGIN {P2}
      z := 777;
   END;  {P2}

BEGIN {P1}
END;  {P1}


PROCEDURE P3;
VAR
   a : REAL;
BEGIN {P3}
END; {P3}


BEGIN {Part12}
   a := 10;
END.  {Part12}
