% Archivo: 10-parser_shift_reduce_01.pl
% Fecha: [2015-05-08]
% Modificación: [2015-05-08]
% Versión: 021
% Autor: Jorge Antonio Leoni de León
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Para poner en funcionamiento la gramática están las siguientes opciones:
/*
(1) ?- shift_reduce([el,gato,duerme],[s]).
Shift: [el]
Reduce: [d]
Shift: [d,gato]
Reduce: [d,n]
Reduce: [sn]
Shift: [sn,duerme]
Reduce: [sn,v]
Reduce: [sn,sv]
Reduce: [s]
true

(2) tokenize_line(Input), shift_reduce(Input,[s]).

Observaciones:

(a) Para que (2) funcione, es necesario invocar '00-tokenizer-nugues.pl'.
*/
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Shift reduce
%?- shift_reduce([the, waiter, brought, the, meal], [s]).
% yes
% ?- shift_reduce([the, waiter, brought, the, meal], [sn, sv]).
% yes

% shift_reduce(+Oracion, ?Categoria)

shift_reduce(Oracion, Categoria) :-
	shift_reduce(Oracion, [], Categoria).

% shift_reduce(+Oracion, +Stack, ?Categoria)
shift_reduce([], Categoria, Categoria).
shift_reduce(Oracion, Stack, Categoria) :-
	reduce(Stack, ReducedStack),
	write('Reduce: '), write(ReducedStack), nl,
	shift_reduce(Oracion, ReducedStack, Categoria).
shift_reduce(Oracion, Stack, Categoria) :-
	shift(Oracion, Stack, NuevaOracion, NewStack),
	write('Shift: '), write(NewStack), nl,
	shift_reduce(NuevaOracion, NewStack, Categoria).

% shift(+Oracion, +Stack, -NuevaOracion, -NewStack),
shift([Primero | Resto], Stack, Resto, NewStack) :-
	append(Stack, [Primero], NewStack).

/*
It is possible to implement a reversed stack. See code here
shift([Primero | RestoOracion], Stack, RestoOracion, [Primero | Stack]).
*/

%reduce(+Stack, -NewStack)
reduce(Stack, NewStack) :-
	match_regla(Stack, NewStack),
	write('  Stack:'), write(Stack),nl,
	write('  NewStack:'), write(NewStack),nl.
reduce(Stack, NewStack) :-
	match_entrada_lexica(Stack, NewStack),
	write('  Stack:'), write(Stack),nl,
	write('  NewStack:'), write(NewStack),nl.

match_regla(Stack, ReducedStack) :-
	regla(Head, Expansion),
	append(StackBottom, Expansion, Stack),
	append(StackBottom, [Head], ReducedStack),
	write('    Stack:'), write(Stack),nl,
	write('    ReduceStack:'), write(ReduceStack),nl.

match_entrada_lexica(Stack, NewStack) :-
	append(StackBottom, Word, Stack),
	entrada_lexica(POS, Word),
	append(StackBottom, [POS], NewStack),
	write('    Stack:'), write(Stack),nl,
	write('    NewStack:'), write(NewStack),nl.
/*
It is possible to implement a reversed stack. See code here
match_regla(Stack, [Head | RestoStack]) :-
	regla(Head, Expansion),
	reverse(Expansion, ExpansionRev),
	append(ExpansionRev, RestoStack, Stack).

match_entrada_lexica([Word | Stack], [POS | Stack]) :-
	entrada_lexica(POS, [Word]).
*/

regla(s, [sn, sv]).
regla(sn, [d, n]).
regla(sv, [v]).
regla(sv, [v, sn]).

entrada_lexica(d, [el]).
entrada_lexica(n, [mesero]).
entrada_lexica(n, [plato]).
entrada_lexica(n, [gato]).
entrada_lexica(v, [lleva]).
entrada_lexica(v, [duerme]).
