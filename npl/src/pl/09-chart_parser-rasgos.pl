% Archivo: 09-chart_parser.pl
% Fecha: [2019-06-18]
% Modificación: [2019-06-18]
% Versión: 002
% Autor: Jorge Antonio Leoni de León
% Descripción: Chart parser según Nugues (2014:376-386)
%
/* Observaciones:

1.  ?- predictor(2,[arc(np, [np, '.', pp], 0, 2)],Chart).
   Chart = [arc(pp, ['.', prep, np], 2, 2), arc(np, [np, '.', pp], 0, 2)].
2. La idea es automáticamente representar las reglas como sigue:
  np --> np . 􏰏pp [0, 2]
  regla(np, [np, pp]).
  arc(np, [np, '.', pp], 0, 2).
3. Con respecto al programa '09-chart_parser.pl' este presenta dos diferencias
importantes. En primer lugar, incorpora rasgos de número y género; en segundo
lugar, el algoritmo de Earley está ampliado, de manera que acepta suejtos
vacíos.

Ejecución:

1. a. ?- parse([el,mesero,llevo,el,plato,de,el,dia],s,Chart).
Chart = [arc(start, [s, '.'], 0, 8), arc(s, [np(num:sg, gen:masc), vp(num:sg, gen:_3682), '.'], 0, 8), arc(vp(num:sg, gen:_3314), [v(num:sg, gen:_3338), np(num:sg, gen:masc), '.'], 2, 8), arc(np(num:sg, gen:masc), [np(num:sg, gen:masc), '.', pp], 3, 8), arc(np(num:sg, gen:masc), [np(num:sg, gen:masc), pp, '.'], 3, 8), arc(pp, [prep, np(..., ...)|...], 5, 8), arc(np(... : ..., ... : ...), [np(..., ...)|...], 6, 8), arc(np(..., ...), [...|...], 6, 8), arc(..., ..., ..., ...)|...]
*/
%
:- op(600, xfy, ':').
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Reglas
%
regla(s, [np(num:NUM,gen:_), vp(num:NUM,gen:_)]).
regla(np(num:NUM,gen:GEN), [d(num:NUM,gen:GEN), n(num:NUM,gen:GEN)]).
regla(np(num:NUM,gen:GEN), [d(num:NUM,gen:GEN), a(num:NUM,gen:GEN), n(num:NUM,gen:GEN)]).
regla(np(num:NUM,gen:GEN), [np(num:NUM,gen:GEN), pp]).
regla(pp, [prep, np(num:_,gen:_)]).
regla(vp(num:NUM,gen:_), [v(num:NUM,gen:_)]).
regla(vp(num:NUM,gen:_), [v(num:NUM,gen:_), np(num:_,gen:_)]).
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Léxico
%
entrada_lexica(d(num:sg,gen:masc), [el]).
entrada_lexica(d(num:sg,gen:fem), [la]).
entrada_lexica(d(num:pl,gen:masc), [los]).
entrada_lexica(d(num:pl,gen:fem), [las]).
entrada_lexica(n(num:sg,gen:masc), [mesero]).
entrada_lexica(n(num:sg,gen:fem), [mesera]).
entrada_lexica(n(num:pl,gen:masc), [meseros]).
entrada_lexica(n(num:pl,gen:fem), [meseras]).
entrada_lexica(n(num:sg,gen:masc), [plato]).
entrada_lexica(n(num:sg,gen:masc), [dia]).
entrada_lexica(n(num:pl,gen:masc), [platos]).
entrada_lexica(n(num:pl,gen:masc), [dias]).
entrada_lexica(prep, [de]).
entrada_lexica(v(num:sg,gen:_), [llevo]).
entrada_lexica(v(num:sg,gen:_), [durmio]).
entrada_lexica(v(num:sg,gen:_), [preparo]).
entrada_lexica(v(num:sg,gen:_), [recomendo]).
entrada_lexica(v(num:pl,gen:_), [llevaron]).
entrada_lexica(v(num:pl,gen:_), [durmieron]).
entrada_lexica(v(num:pl,gen:_), [prepararon]).
entrada_lexica(v(num:pl,gen:_), [recomendaron]).
% Para sujeto tácito...
%entrada_lexica(d(num:_,gen:_), []).
%entrada_lexica(n(num:_,gen:_), []).
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Expand chart
%
expand_chart([], Chart, Chart).

expand_chart([Entry|Entries], Chart, NewChart) :-
    \+ member(Entry, Chart),
    !,
    expand_chart(Entries, [Entry | Chart], NewChart).

expand_chart([_|Entries], Chart, NewChart) :-
    expand_chart(Entries, Chart, NewChart).
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Earley parser
%
earley_parser([], FinalPos, FinalPos, Chart, Chart):-
      !.

earley_parser(EntradasLexicas, CurPos, FinalPos, Chart, FinalChart) :-
      predictor(CurPos, Chart, PredChart),
      NextPos is CurPos + 1,
      scanner(EntradasLexicas, RestEntradasLexicas, CurPos, NextPos, PredChart, ScanChart),
      completer(NextPos, ScanChart, NewChart),
      !,
      earley_parser(RestEntradasLexicas, NextPos, FinalPos, NewChart, FinalChart).
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
% Parse
%
parse(EntradasLexicas, Category, FinalChart) :-
  expand_chart([arc(start, ['.', Category], 0, 0)], [], Chart),
  earley_parser(EntradasLexicas, 0, FinalPos, Chart, FinalChart),
  member(arc(start, [Category, '.'], 0, FinalPos), FinalChart).
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Predictor
% The predictor looks for reglas to expand arcs from a current position (CurPos).
%
predictor(CurPos, Chart, PredChart) :-
  findall(
          arc(CAT, ['.' | RHS], CurPos, CurPos),
          (
            member(arc(LHS, ACTIVE_RHS, InitPos, CurPos),
            Chart),
            append(B, ['.', CAT | E], ACTIVE_RHS),
            regla(CAT, RHS),
            \+ member(arc(CAT, ['.' | RHS], CurPos,CurPos), Chart)
          ),
          NewChartEntries),
          NewChartEntries \== [],
          expand_chart(NewChartEntries, Chart, NewChart),
          predictor(CurPos, NewChart, PredChart),
          !.

predictor(_, PredChart, PredChart).
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% The Scanner
% The scanner gets a new word (entrada_lexica) from the input and looks for active arcs that
% match its possible parts of speech to the right of the dot. The scanner stores
% the word (entrada_lexica) with its compatible parts of speech as new chart entries.
%
% The first scanner regla
scanner([EntradaLexica | Rest], Rest, CurPos, NextPos, Chart, NewChart) :-
    findall(
      arc(CAT, [EntradaLexica, '.'], CurPos, NextPos),
      (
        entrada_lexica(CAT, [EntradaLexica]),
        once((
          member(arc(LHS, ACTIVE_RHS, InitPos, CurPos),
            Chart),
          append(B, ['.', CAT | E], ACTIVE_RHS)
          )
        )
      ),
      NewChartEntries),
      NewChartEntries \== [],
      expand_chart(NewChartEntries, Chart, NewChart),
      !.
%
% The second regla to handle empty symbols
%
scanner(EntradasLexicas, EntradasLexicas, CurPos, NextPos, Chart,NewChart) :-
    findall(
      arc(CAT, [[], '.'], CurPos, NextPos),
      (
        entrada_lexica(CAT, []),
        once((
              member(arc(LHS, ACTIVE_RHS, InitPos, CurPos),
              Chart),
              append(B, ['.', CAT | E], ACTIVE_RHS)
              )
        )
      ),
      NewChartEntries),
      NewChartEntries \== [],
      expand_chart(NewChartEntries, Chart, NewChart),
      !.
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% The Completer
% The completer looks for completed constituents, that is, for arcs with a dot
% at the end of the right-hand-side part of the regla.
%
completer(CurPos, Chart, CompChart) :-
    findall(
      arc(LHS2, RHS3, PrevPos, CurPos),
      (
        member(arc(LHS, COMPLETE_RHS, InitPos, CurPos),
          Chart),
        append(_, ['.'], COMPLETE_RHS),
        member(arc(LHS2, RHS2,PrevPos,InitPos), Chart),
        append(B, ['.', LHS | E], RHS2),
        append(B, [LHS, '.' | E], RHS3),
        \+ member(arc(LHS2, RHS3, PrevPos, CurPos),
        Chart)
      ),
      CompletedChartEntries),
      CompletedChartEntries \== [],
      expand_chart(CompletedChartEntries,Chart,NewChart),
      completer(CurPos, NewChart, CompChart),
      !.

completer(_, CompChart, CompChart).
