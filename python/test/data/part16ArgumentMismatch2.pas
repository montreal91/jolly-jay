
program Part16ArgumentMismatch2;

procedure Alpha(a : integer; b : integer);
var x : integer;
begin
   x := (a + b ) * 2;
end;

begin { Main }

  Alpha(3);  { procedure call }
end.  { Main }
