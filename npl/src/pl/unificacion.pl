% Archivo: 07-unification_sp.pl
% Fecha: [2015-03-09]
% Modificación: [2019-04-09]
% Versión: 001
% Autor: Jorge Antonio Leoni de León
%
% Nugues (2006:256).
%
% Para generar:
%
% 1.	sn(_,_,_,_,ORACION,[]).
%
% 2.	?- sn(L1,L2,L3,L4,L,[]).
%		L1 = gen:masc,
%		L2 = num:sg,
%		L3 = cas:nom,
%		L4 = pers:3,
%		L = [el, piloto, bueno]
%
% 3.  between(1,8,N), length(S,N), phrase(sn(L1,L2,L3,L4),S),writeln(S),sleep(0.2),false.
%

:- op(600, xfy, ':').

sn(gen:GEN, num:NUM, cas:CAS, pers:PER) --> det(gen:GEN, num:NUM, cas:CAS, pers:PER), n(gen:GEN, num:NUM, cas:CAS, pers:PER), adj(gen:GEN, num:NUM, cas:CAS, pers:PER).

% sn(gen:GEN, num:NUM, cas:CAS, pers:PER) --> det(gen:GEN, num:NUM, cas:CAS, pers:PER), pro_n(gen:GEN, num:NUM, cas:CAS, pers:PER), adj(gen:GEN, num:NUM, cas:CAS, pers:PER).

sn(gen:GEN, num:NUM, cas:CAS, pers:PER) --> pro_n(gen:GEN, num:NUM, cas:CAS, pers:PER).

% pro_n(gen:GEN, num:NUM, cas:nom, pers:PERS) --> [].

det(gen:masc, num:sg, cas:nom, pers:3) --> ['el'].
det(gen:fem, num:sg, cas:nom, pers:3) --> ['la'].
det(gen:masc, num:pl, cas:nom, pers:3) --> ['los'].
det(gen:fem, num:pl, cas:nom, pers:3) --> ['las'].
det(gen:masc, num:sg, cas:nom, pers:3) --> ['un'].
det(gen:masc, num:pl, cas:nom, pers:3) --> ['unos'].
det(gen:fem, num:pl, cas:nom, pers:3) --> ['unas'].

adj(gen:masc, num:sg, cas:nom, pers:3) --> ['bueno'].
adj(gen:fem, num:sg, cas:nom, pers:3) --> ['buena'].
adj(gen:masc, num:pl, cas:nom, pers:3) --> ['curiosos'].
adj(gen:fem, num:pl, cas:nom, pers:3) --> ['blancas'].
adj(gen:masc, num:sg, cas:nom, pers:3) --> ['negro'].
adj(gen:masc, num:pl, cas:nom, pers:3) --> ['resguardados'].
adj(gen:fem, num:pl, cas:nom, pers:3) --> ['improvisadas'].
adj(gen:_, num:sg, cas:nom, pers:3) --> ['verde'].

n(gen:masc, num:sg, cas:nom, pers:3) --> ['piloto'].
n(gen:fem, num:sg, cas:nom, pers:3) --> ['paloma'].
n(gen:masc, num:pl, cas:nom, pers:3) --> ['toreros'].
n(gen:fem, num:pl, cas:nom, pers:3) --> ['alumnas'].
n(gen:masc, num:sg, cas:nom, pers:3) --> ['marinero'].
n(gen:masc, num:pl, cas:nom, pers:3) --> ['policias'].
n(gen:fem, num:pl, cas:nom, pers:3) --> ['personas'].
n(gen:_, num:pl, cas:nom, pers:3) --> ['estudiantes'].

n(gen:fem, num:_, cas:nom, pers:3) --> ['tesis'].
