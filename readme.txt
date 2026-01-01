0) white clock, 3 hands need a bit dark background such that it can be seen on white windows wallpaper.
1) great "liquid glass" looking, clock need 12 hour 刻度.
2) small (widget size: 200x200) but clear transparent (white) circular clock on 4K monitor, default on the top-right when start, it can drag by user anywhere on 4K screen, it need remember its previous position on screen and display on the same position in next startup.
3) three white hands(hour, minute, second) can be seen which shows realtime system time (in AM/PM).  And it have a rectangle box to show date YYYY/MM/DD, weekdays(Sun to Sat), correct Chinese lunar day(from XX月初一 to XX月卅).  [CHINESE_MONTHS replace "冬月" with "十一月", replace "腊月" with "十二月"]
4) have grey background, white "_" minimize button, once click, minimize to taskbar "clock" icon, and can restore its position from taskbar when click, on left top on rectangle.
5) have grey background, white "X" button to complete kill its running, on right top on rectangle.
6) whole configuration (X,Y position, draggable, active, color etc.) in a .ini file (with realtime information, in plain text contents) - pls refer to application "Rainmeter" setting, can be amend by user, once application starts, refer this .ini file (such that it can remember its previous position as stated in 1).
e.g.
Active=1
WindowX=(#SCREENAREAWIDTH#-200)
WindowY=150
ClickThrough=0
Draggable=1
SnapEdges=1
KeepOnScreen=1
AlwaysOnTop=0
7) final version to be built in a .exe (no need install) file for win11.


