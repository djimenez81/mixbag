% Archivo: dos.pl
% Fecha de creación: 2019-03-25
% Modificación: 2019-03-25
% Versión: 1
% Autor: David Jiménez


letras([filosofia,lenguas,filologia,literatura]).
ciencias([mate,fisica,quimica,biolo,geologia]).
salud([enfermeria,medicina,nutricion,publica,odonto,micro]).
ingenieria([civil,electrica,quimica,industrial,mecanica,compu,arquitectura]).
economicas([negocios,publica,economia,estadistica]).



% OTRAS REGLAS

miembro(X,[X|_]).
miembro(X,[_|COLA]) :- miembro(X,COLA).

concatenar([],X,X).
concatenar([X|Y],Z,[X|W]) :- concatenar(Y,Z,W).

concatenar2(X,X,[]).
concatenar2([X|Y],Z,[X|W]) :- concatenar2(Y,Z,W).

invertir([],X,X).
invertir([X|Y],Z,W) :- invertir(Y,[X|Z],W).
invertir(A,B) :- invertir(A,[],B).
