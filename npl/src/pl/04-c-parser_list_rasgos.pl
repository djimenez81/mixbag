% Archivo: 04-c-parser_list_rasgos.pl
% Fecha: [2015-04-13]
% Modifcicación: [2019-04-09]
% Versión: 001
% Autor: Jorge Antonio Leoni de León
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Para poner en funcionamiento la gramática están las siguientes opciones:
%
% (1)	a. phrase(oracion,[el,artista,toma,el,vino]).
%		b. oracion([el,artista,esculpe,el,arbol],[]).
%
% (2) oracion(X,L).
%
% (3) oracion(X,[]).
%
% (4) phrase(oracion,L).
%
% (5) between(1,8,N), length(S,N), phrase(oracion,S), writeln(S), sleep(0.2),false.
%
% (6) tokenize_line(X), oracion(X,[]).
%
% Observaciones:
%
% (a) La opción (5) despliega todas las opciones que contengan de uno a ocho elementos
% terminales. Es posible adaptarlo para todas las otras posibilidad de funcionamiento.
%
% (b) En (6) es necesario invocar '00-tokenizer-nugues.pl'.
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%

oracion(F0,F) :-
	sintagma_nominal(NUM,F0,F1),
	sintagma_verbal(NUM,F1,F).

sintagma_nominal(NUM,F0,F) :-
	determinante(NUM,F0,F1),
	nombre(NUM,F1,F).

sintagma_nominal(NUM,F0,F) :-
	nombre_p(NUM,F0,F).

sintagma_verbal(NUM,F0,F) :-
	verbo(NUM,F0,F).

sintagma_verbal(NUM,F0,F) :-
	verbo(NUM,F0,F1),
	sintagma_nominal(_,F1,F).	% Ej: sintagma_nominal(NUM,F1,F).

determinante(sing,[el|F],F).
determinante(sing,[un|F],F).

determinante(plur,[los|F],F).
determinante(plur,[unos|F],F).

nombre(sing,[arbol|F],F).
nombre(sing,[artista|F],F).
nombre(sing,[vino|F],F).

nombre(plur,[artistas|F],F).
nombre(plur,[rostros|F],F).
nombre(plur,[vinos|F],F).

nombre_p(sing,[tyrion|F],F).

verbo(sing,[esculpe|F],F).
verbo(sing,[reflexiona|F],F).
verbo(sing,[toma|F],F).

verbo(plur,[esculpen|F],F).
verbo(plur,[miran|F],F).
verbo(plur,[toman|F],F).
verbo(plur,[reflexionan|F],F).
