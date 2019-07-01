% Archivo: 06-parser_subcat.pl
% Fecha: [2015-03-09]
% Modificación: [2019-04-09]
% Versión: 006
% Autor: Jorge Antonio Leoni de León
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
sv --> v(1).
sv --> v(2), sn.
sv --> v(3), sn, sp.
sv --> v(4), o.

v(1) --> [duerme]; [ladra].
v(2) --> [lee];[toma].
v(3) --> [da].
v(4) --> [dice]; [piensa].
