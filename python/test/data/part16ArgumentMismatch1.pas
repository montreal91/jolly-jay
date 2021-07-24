
program Part16ArgumentMismatch1;

procedure Alpha(a : integer; b : integer);
var x : integer;
begin
   x := (a + b ) * 2;
end;

begin { Main }

  Alpha();  { procedure call }
end.  { Main }
