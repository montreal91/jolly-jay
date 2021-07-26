
program part19a;

procedure Alpha(a : integer; b : integer);
var x : integer;
begin
   x := (a + b ) * 2;
end;

procedure Beta;
var x : Real;
begin
  x := 9.1 + 4.3;
end;

  procedure Gamma(a : Integer; b : integer);
  begin
    Alpha(a + 1, b + 1);
    Beta();
  end;

begin { Main }
  Alpha(3 + 5, 7);  { procedure call }
  Beta();
  Gamma(2 + 2 * 2, (2 + 2) * 2);
end.  { Main }
