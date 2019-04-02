% Archivo: palindromo.pl
% Fecha de creación: 2019-04-01
% Modificación: 2019-04-01
% Versión: 1
% Autor: David Jiménez

% Un palindromo es una palabra que


invertir([],X,X).
invertir([X|Y],Z,W) :- invertir(Y,[X|Z],W).
invertir(A,B) :- invertir(A,[],B).

palindroma(X) :- invertir(X,I), X = I.

prefijo([],_).
prefijo([A|L],[A|P]) :- prefijo(L,P).

sufijo(A,B) :- invertir(A,C),invertir(B,D),prefijo(C,D).

afijo(A,B) :- sufijo(A,B).
afijo(A,B) :- prefijo(A,B).
