% Archivo: 09-chart_parser.pl
% Fecha: [2019-06-18]
% Modificación: [2019-06-18]
% Versión: 002
% Autor: Jorge Antonio Leoni de León
% Descripción: Chart parser según Nugues (2014:376-386)
/*
Observaciones:

1. ?- predictor(2,[arc(np, [np, '.', pp], 0, 2)],Chart).
   Chart = [arc(pp, ['.', prep, np], 2, 2), arc(np, [np, '.', pp], 0, 2)].
2. La idea es automáticamente representar las reglas como sigue:
   np --> np . 􏰏pp [0, 2]
   regla(np, [np, pp]).
   arc(np, [np, '.', pp], 0, 2).

Ejecución:

1. a. ?- parse([el,mesero,llevo,el,plato,de,el,dia],s,Chart).
Chart = [arc(start, [s, '.'], 0, 8), arc(s, [np, vp, '.'], 0, 8), arc(vp, [v, np, '.'], 2, 8), arc(np, [np, '.', pp], 3, 8), arc(np, [np, pp, '.'], 3, 8), arc(pp, [prep, np|...], 5, 8), arc(np, [np|...], 6, 8), arc(np, [...|...], 6, 8), arc(..., ..., ..., ...)|...]
*/
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Reglas
%
regla(s, [np, vp]).
regla(np, [d, n]).
regla(np, [d, a, n]).
regla(np, [np, pp]).
regla(pp, [prep, np]).
regla(vp, [v]).
regla(vp, [v, np]).
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Léxico
%
entrada_lexica(d, [el]).
entrada_lexica(n, [mesero]).
entrada_lexica(n, [plato]).
entrada_lexica(n, [dia]).
entrada_lexica(prep, [de]).
entrada_lexica(v, [llevo]).
entrada_lexica(v, [durmio]).
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Expand chart
%
expand_chart([], Chart, Chart).

expand_chart([Entry | Entries], Chart, NewChart) :-
  \+ member(Entry, Chart),
  !,
  expand_chart(Entries, [Entry | Chart], NewChart).

expand_chart([_ | Entries], Chart, NewChart) :-
  expand_chart(Entries, Chart, NewChart).

earley_parser([], FinalPos, FinalPos, Chart, Chart):-
  !.

earley_parser(EntradasLexicas, CurPos, FinalPos, Chart, FinalChart) :-
  predictor(CurPos, Chart, PredChart),
  NextPos is CurPos + 1,
  scanner(EntradasLexicas, RestEntradasLexicas, CurPos, NextPos, PredChart, ScanChart),
  completer(NextPos, ScanChart, NewChart),
  !,
  earley_parser(RestEntradasLexicas, NextPos, FinalPos, NewChart, FinalChart).

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
scanner([EntradaLexica | Rest], Rest, CurPos, NextPos, Chart,
        NewChart) :-
    findall(
      arc(CAT, [EntradaLexica, '.'], CurPos, NextPos),
      (
        entrada_lexica(CAT, [EntradaLexica]),
        once((
          member(arc(LHS, ACTIVE_RHS, InitPos, CurPos),
            Chart),
          append(B, ['.', CAT | E], ACTIVE_RHS)))
      ),
      NewChartEntries),
    NewChartEntries \== [],
    expand_chart(NewChartEntries, Chart, NewChart).
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
