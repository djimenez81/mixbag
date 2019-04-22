% Archivo: 02-parser_list_append.pl
% Fecha: [2015-04-13]
% Modifcicación: [2015-04-13]
% Versión: 009
% Autor: Jorge Antonio Leoni de León
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Para poner en funcionamiento la gramática están las siguientes opciones:
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
oracion(X) :-
	append(Y,Z,X),
	sintagma_nominal(Y),
	sintagma_verbal(Z).

sintagma_nominal(X) :-
	append(Y,Z,X),
	determinante(Y),
	nombre(Z).

sintagma_verbal(X) :- % Verbo intransitivo
	verbo(X).

sintagma_verbal(X) :-  % Verbo transitivo
	append(Y,Z,X),
	verbo(Y),
	sintagma_nominal(Z).

sintagma_verbal(X) :-
	append(Y,Z,X),
	verbo(Y),
	sintagma_preposicional(Z).

sintagma_verbal(X) :-
	append(T,P,X),
	append(Y,Z,T),
	verbo(Y),
	sintagma_nominal(Z),
	sintagma_preposicional(P).


sintagma_preposicional(X) :-
	append(Y,Z,X),
	preposicion(Y),
	sintagma_nominal(Z).

determinante([el]).
determinante([un]).

nombre([arbol]).
nombre([artista]).
nombre([barco]).
nombre([modelo]).
nombre([tonel]).
nombre([vino]).

verbo([esculpe]).
verbo([hace]).
verbo([reflexiona]).
verbo([toma]).

preposicion([en]).
