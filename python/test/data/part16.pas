
program Part16;

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

begin { Main }

  Alpha(3 + 5, 7);  { procedure call }
  Beta();
end.  { Main }
