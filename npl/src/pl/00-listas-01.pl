% Archivo: 00-listas.pl
% Fecha: 19 de marzo de 2015.
% Modificación: 2015-04-13.
% Versión: 3.
% Autor: Jorge Antonio Leoni de León
% Fuente: https://www.cpp.edu/~jrfisher/www/prolog_tutorial/2_7.html

% ¿ Es X miembro de la lista L ?

miembro(X , [X|_]).
miembro(X, [_|COLA]) :- miembro(X,COLA).

% Concatenar una lista
%
% 1) Una lista A concatenada con una lista vacía es igual a A.
%
% 2) El primer elmento de la lista X siempre será el primer elemento 
% de la tercera lista
%
% 3) La cola de la primera lista (Y) siempre tendrá al segundo 
% argumento (Z) concatenado para formar la cola (W) del tercer 
% argumento
%
% 4) Esta acción continúa recursivamente hasta tener una lista 
% vacía como primer argumento.
%

concatenar([],X,X).
concatenar([X|Y],Z,[X|W]) :- concatenar(Y,Z,W).

% Invertir una lista

invertir([],X,X).
invertir([X|Y],Z,W) :- invertir(Y,[X|Z],W).
invertir(A,B) :- invertir(A,[],B).

% ¿Es la secuencia X un palíndromo?
%
% aboba		aérea	alela	ananá	aviva	ososo	radar
% rajar		rapar	rasar	sacas	salas	sanas	sayas
% seres		solos	somos	sosos	sugus	narran	rallar
% selles	abanaba	anilina	arenera	recocer			acurruca
% reconocer			sometemos		girafarig		reconocer
% Adán no cala con nada
% allí ves sevilla
% arde ya la yedra

palindroma(X) :- invertir(X,I), X = I.

% Prefijo

prefijo([],_).
prefijo([A|P],[A|L]) :- prefijo(P,L).

% Sufijo

sufijo(A,B) :- invertir(A,C), invertir(B,D), prefijo(C,D).

% Afijacion

afijo(A,B) :- prefijo(A,B).
afijo(A,B) :- sufijo(A,B).

% O también con el operador ';' (or): 
%	afijo(A,B) :- prefijo(A,B); sufijo(A,B).


% Aplanar una lista
% Fuente: http://www.cs.uni-potsdam.de/wv/lehre/Material/Prolog/Eclipse-Doc/bips/lib/lists/flatten-2.html
% Aquí pasamos de aplanar/3 a aplanar/2
%
% Regla 1 aplanar()
%

aplanar(LISTA, APLANADO) :-
        aplanar(LISTA, APLANADO, []),
        sleep(0.5),
        write('(1) Regla 1 '), nl,
        write(' Esta regla solo invoca aplanar/3 '), nl,
        tab(5), write('(1) [LISTA] (INPUT) '), write(LISTA), nl,
        tab(10), write('(1) [APLANADO] (OUTPUT) '), write(APLANADO), nl.

%
% Dadas dos listas, siendo la primera vacía, la lista resultante
% es igual a la segunda lista
%
% Regla 2 aplanar()
%
aplanar([], Res, Res) :- !, 
		sleep(0.5),
		write('(2) Regla 2 '), nl,
		tab(5), write('(2) [Res] '), write(Res), nl.

%
% Dadas tres listas (1), (2) y (3), (1) consiste en una cabeza y 
% una cola, (2) es el resultado y (3) es la continuación de la 
% lista
%
% Regla 3 aplanar()
%

aplanar([Head|Tail], Res, Cont) :-
        !,
        aplanar(Head, Res, Cont1), % Separación de la cabeza y la cola 
        write('(3) Regla 3 '),  nl,
        tab(5), write('(3.a) [Head] '), write(Head), nl, 
        tab(5), write('(3.a) [Res] '), write(Res), nl, 
        tab(5), write('(3.a) [Cont1] '), write(Cont1), nl, 
        aplanar(Tail, Cont1, Cont),
        sleep(0.5),
        tab(10), write('(3.b) [Tail] '), write(Tail), nl,
        tab(10), write('(3.b) [Cont1] '), write(Cont1), nl, 
        tab(10), write('(3.b) [Cont] '), write(Cont), nl.

% 'Hecho' invocado por la regla anterior, una lista cuyo primer elemento
% es igual al primer argumento del predicado, produce una lista Cont
% igual a la cola de la lista. Luego, el input de la estructura de la regla 1
% consistente en una lista de entrada y una lista vacía para llenar con el
% resultado es modificada, quedando unificado el tercer argumento (vacío)
% con una lista que contiene los elementos de la cola. El proceso sigue, 
% unificando con otras reglas.
%
% Regla 4 (Hecho 1) aplanar()
%

aplanar(Term, [Term|Cont], Cont) :- write('(4) Regla 4 (Hecho 1) '), nl,
		tab(5), write('(4.a) [Term] '), write(Term), nl,
		tab(10), write('(4.b) [Cont] '), write(Cont), nl.

% Success:
%    [eclipse]: flatten([[1,2,[3,4],5],6,[7]], L).
%    L = [1, 2, 3, 4, 5, 6, 7]
%    yes.
%
% Fail:
%    [eclipse]: flatten([1,[3],2], [1,2,3]).
%    no.


