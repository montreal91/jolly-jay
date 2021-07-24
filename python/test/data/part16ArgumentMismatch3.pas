
program Part16ArgumentMismatch3;

procedure Alpha(a : integer; b : integer);
var x : integer;
begin
   x := (a + b ) * 2;
end;

begin { Main }

  Alpha(3, 4, 3);  { procedure call }
end.  { Main }
