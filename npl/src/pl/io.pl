
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%
%%%%%  Program         :  io.pl
%%%%%  Author          :  Juri Mengon
%%%%%  Creation date   :  20/07/2001
%%%%%  Last update     :  20/07/2001
%%%%%
%%%%%  Function        :  - input / output operations
%%%%%
%%%%%  Main predicates :
%%%%%
%%%%%

:- module( io, [ io__skip_lf/0,
                 io__read_line/1,
                 io__read_buffer/2,
                 io__read_buffer_dl/2,
                 io__read_buffer/4,
                 io__read_tokenized_list/1,
                 io__read_tokenized_file/2,
                 io__write_term_indented/1,
                 io__write_term_indented/2,
                 io__write_term_as_tree/1,
                 io__write_term_as_csv/1,
                 io__write_pred_as_csv/1,
                 io__write_file_as_csv/2,
                 io__var_letters/2,
                 io__display_ascii_table/0 ]).

:- use_module(library(lists)).
:- use_module(library(readln)).
:- use_module(library(backcomp)).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%io__write_term_indented

io__skip_lf :-
    peek_byte( 10),
    get0( 10),
    !,
    io__skip_lf.
io__skip_lf.


io__read_line( Line) :-
    io_read_buffer_dl( Line-[], 0-_Len).


io__read_buffer( L, Len) :-
    io_read_buffer_dl( L-[], 0-Len).


io__read_buffer_dl( D-L, Len) :-
    io_read_buffer_dl( D-L, 0-Len).

    io_read_buffer_dl( D0-L, C0-Cn) :-
        get0( Char),
        (  Char = 10          -> D0 = L, Cn = C0
         ; Char = end_of_file -> D0 = L, Cn = C0
         ; C1 is C0 + 1,
           D0 = [Char|D1],
           !,
           io_read_buffer_dl( D1-L, C1-Cn)
         ).


io__read_buffer(Stream, D, BuffLen, Eof) :-
    io_read_buffer(Stream, 0'., 0' , D, Eof, BuffLen, 0-_Len).

    io_read_buffer(Stream, Ch, Next, D0, Eof, BuffLen, C0-Cn) :-
        get0(Stream, Char),
        (  Char = -1
            -> D0  = [],
               Cn  = C0,
               Eof = Char
        ;
           C0 >= BuffLen,
           Char = Ch,
           peek_byte(Stream, Next)
            -> D0 = [Char],
               Cn is C0 + 1,
               Eof = Char
        ;
           C1 is C0 + 1,
           D0 = [Char|D1],
           !,
           io_read_buffer(Stream, Ch, Next, D1, Eof, BuffLen, C1-Cn)
        ).


io__read_tokenized_file( File, Tokens) :-
    seeing( OldFile),
    see( File),
    readln( Tokens, -1),
    seen,
    see( OldFile).

io__read_tokenized_list( L) :-
    readln( L).

io__write_pred_as_csv( Func/Arity) :-
    functor( Term, Func, Arity),
    (  call( Term),
       io__write_term_as_csv( Term),
       fail
     ;
       !, true
     ).


io__write_term_as_csv( Term) :-
    functor( Term, _, Arity),
    (  between( 1, Arity, N),
       arg( N, Term, Arg),
       write( Arg),
       (  N < Arity -> write( ';') ; nl  ),
       fail
     ;
       !, true
     ).


io__write_file_as_csv( InFile, OutFile) :-
    open( InFile, read, InStream),
    tell( OutFile),
    repeat,
    read( InStream, Clause),
    (  Clause \= end_of_file
        ->  io__write_term_as_csv( Clause),
            fail
        ;
            !,
            close( InStream),
            told
     ).


%%% io__var_letters( +TermIn, -TermOut)
%%%   binds unbound variables to uppercase letters
%
io__var_letters( TermIn, TermOut) :-
     copy_term( TermIn, TermOut),
     free_variables( TermOut, FreeVars),
     variable_letters( Letters),
     unify_variables( FreeVars, Letters).

     variable_letters( [ 'X', 'Y', 'Z', 'U', 'V', 'W',
                         'A', 'B', 'C', 'D', 'E', 'F',
                         'G', 'H', 'I', 'J', 'K', 'L' ,
                         'M', 'N', 'O', 'P', 'Q', 'R',
                         'S', 'T']).

     unify_variables( [Var|Vars], [Var|Letters]) :-
          !,
          unify_variables( Vars, Letters).
     unify_variables( [_Var|Vars], Letters) :-
          !,
          unify_variables( Vars, Letters).
     unify_variables( _Vars, _Letters).  % exhausted variables or letters




io__display_ascii_table :-
    format( '~n~tAscii Codes~t~80|~n~n'),
    (  between( 1, 32, Row),
       findall( p( Code, Atom),
                (  between( 0, 7, Column),
                   Code is Row * 8 + Column,
                   between( 32, 255, Code),
                   atom_codes( Atom, [Code])
                 ), AsciiCodes ),
        length( AsciiCodes, Len),
        Len > 0,
        ascii_codes_to_list( AsciiCodes, List),
        format( '  ~d ~`�t ~w~10|   ~d ~`�t ~w~20|   ~d ~`�t ~w~30|   ~d ~`�t ~w~40|   ~d ~`�t ~w~50|   ~d ~`�t ~w~60|   ~d ~`�t ~w~70|   ~d ~`�t ~w~80|~n',
                List),
        fail
      ;
        nl
      ).


    ascii_codes_to_list( [], []).
    ascii_codes_to_list( [p( C, A)|T1], [C, A|T2]) :-
        ascii_codes_to_list( T1, T2).



is_operator( ','  ).
is_operator( not  ).
is_operator( \+   ).
is_operator( =    ).
is_operator( ==   ).
is_operator( \==  ).
is_operator( =:=  ).
is_operator( =\=  ).
is_operator( <    ).
is_operator( >    ).
is_operator( =<   ).
is_operator( >=   ).
is_operator( +    ).
is_operator( -    ).
is_operator( /\   ).
is_operator( \/   ).
is_operator( *    ).
is_operator( /    ).
is_operator( //   ).
is_operator( <<   ).
is_operator( >>   ).
is_operator( ^    ).


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%% io__write_term_indented( +Term)
%%%   output prolog structures
%%%   Actually Hess' ppp/1 (primitive pretty print)
%%%   ex: io__write_term_indented( s( np( det( the), np( dog)), vp( v( sleeps))))
%%%         s(np(det(the)
%%%              n(dog))
%%%           vp(v(sleeps)))
%
io__write_term_indented( Term)   :-
    numbervars( Term, var, 1, _),
    nl,
    write_term_indented( nonlist, Term, 0),
    nl.

    write_term_indented( _, Term, _Pos)  :-
        ( atomic( Term) ; var( Term) ),
        write( Term),
        !.

    write_term_indented( _, Term, _Pos)  :-
        Term =.. [H|_],
        is_operator( H),
        write( Term).

    write_term_indented( nonlist, Term, Pos) :-
        Term =.. ['.'|T],
        write( '['),
        Pos1 is Pos + 1,
        portray_all( list, T, Pos1, ']', -),
        !.

    write_term_indented( list, Term, Pos) :-
        Term =.. ['.'|T],
        Pos1 is Pos + 1,
        write( ','),
        portray_all( list, T, Pos1, ']', -),
        !.

    write_term_indented( _, Term, Pos) :-
        Term =.. [','|_],
        listify( Term, List),
        write( '('),
        Pos1 is Pos + 1,
        portray_all( nonlist, List, Pos1, ')', -),
        !.

    write_term_indented( _, Term, Pos) :-
        Term =.. [H|T],
        write( H),
        write( '('),
        atom_codes( H, List),
        length( List, Len),
        Temp is Pos + Len,
        Pos1 is Temp + 1,
        portray_all( nonlist, T, Pos1, ')', -).

        portray_all( nonlist, [], _Pos, C, _NL) :- write( C), !.
        portray_all( nonlist, [[]|T], Pos, C, NL) :-
            !,
            portray_all( nonlist, T, Pos, C, NL).
        portray_all( nonlist, [H|T], Pos, C, NL) :-
            ( NL = '+'  -> nl, tab( Pos) ;  true ),
            write_term_indented( nonlist, H, Pos),
            !,
            portray_all( nonlist, T, Pos, C, +).

        portray_all( list, [],   _Pos, _C, _NL) :- !.
        portray_all( list, [[]], _Pos, _C, _NL) :- write( ']'), !.
        portray_all( list, [H|T], Pos,  C, _NL) :-
            write_term_indented( list, H, Pos),
            (  member( T, [[[]], []]) -> true ; write( ',') ),
            !,
            portray_all( list, T, Pos, C, +).


%%% listify( +Term, -List)
%%%   converts a Term into a List
%
listify( Term, [H|List]) :-
  Term =.. [',', H, Term1],
  listify( Term1, List).

listify( Atom, [Atom]).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%% io__write_term_indented( +Term, +Tab)
%%%   output Prolog structures
%
io__write_term_indented( Atom, N) :-
  atomic( Atom),
  !,
  do_n_times( N, write( ' ')),
  write( Atom), nl.

io__write_term_indented( Struct, N) :-
  numbervars( Struct, var, 1, _),
  Struct =.. [Func|Args],
  do_n_times( N, write( ' ')),
  atom_length( Func, Len),
  write( Func),
  write( '('), nl,
  M is N + Len + 1,
  pp_arguments( Args, M),
  B is M - 1,
  do_n_times( B, write( ' ')),
  write( ')'), nl.

  pp_arguments( [], _).
  pp_arguments( [H|T], M) :-
    io__write_term_indented( H, M),
    !,
    pp_arguments( T, M).


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


%%% write_tree( +Struct)
%%%   Tree output of prolog term Struct
%
io__write_term_as_tree( Struct) :-
     (  nonvar(Struct)
         -> analyse( Struct, List, 0, _R),
            print_tree( List)
     ;
        true
     ).

     analyse( Atom, [n( Atom, Pos)], L, R) :-
          atomic( Atom),
          !,
          atom_length( Atom, Len),
          R is L + Len + 2,
          Pos is (R + L) // 2 .
     analyse( Tree, [n( Func, Pos), [n( Succ, Pos)]], L, R) :-
          Tree =.. [Func, Succ],
          atomic( Succ),
          !,
          atom_length( Succ, Len1),
          atom_length( Func, Len2),
          max( Len1, Len2, Len),
          R is L + Len + 2,
          Pos is (R + L) // 2.
/*
     analyse( Tree, [n( Func, Pos), List_Succ], L, R) :-
          Tree =.. [Func|Succ],
          member( [], Succ),
          delete( [], Succ, NewSucc),
          !,
          atom_length( Func, Len),
          R_Node is L + Len + 2,
          analyse_successor( NewSucc, L, R_Sub_Tree, List_Succ),
          calculate_pos( L, Pos, List_Succ, R_Sub_Tree, R_Node, R).
 */
     analyse( Tree, [n( Func, Pos), List_Succ], L, R) :-
          Tree =.. [Func|Succ],
          atom_length( Func, Len),
          R_Node is L + Len + 2,
          analyse_successor( Succ, L, R_Sub_Tree, List_Succ),
          calculate_pos( L, Pos, List_Succ, R_Sub_Tree, R_Node, R).

          analyse_successor( [H|T], L, R, List) :-
               \+ (T = []),
               analyse( H, List1, L, Mid),
               analyse_successor( T, Mid, R, List2),
               append( List1, List2, List).
          analyse_successor( [E], L, R, List) :-
               analyse( E, List, L, R).

          calculate_pos( _L, Pos, List_Succ, R, R_Node, R) :-
               R_Node =< R,
               !,
               first_node( List_Succ, Pos1),
               last_node(  List_Succ, Pos2),
               Pos is (Pos1 + Pos2) // 2.
          calculate_pos( L, Pos, _List_Succ, R_Sub_Tree, R, R) :-
               R > R_Sub_Tree,
               Pos is (R + L) // 2.

     print_tree( List) :-
          List = [_|_],
          write_node( List, 0), nl,
          write_branches( List, 0), nl,
          write_twigs( List, List1, 0), nl,
          print_tree( List1).
     print_tree( []).

          write_node( [H|T], Pos) :-
               print_node( H, Pos, Pos1),
               !,
               write_node( T, Pos1).
          write_node( [_|T], Pos) :-
               !,
               write_node( T, Pos).
          write_node( [], _Pos).

               print_node( n( E, Pos), S1, S2) :-
                    atom_length( E, Len),
                    B is Pos - Len // 2 - S1, do_n_times( B, write( ' ')),
                    S2 is Pos + Len // 2 + Len mod 2,
                    write( E).

            % leaves
          write_branches( [_, H|T], Pos) :-
               \+ (H = [_|_]),
               !,
               write_branches( [H|T], Pos).
          write_branches( [_E], _Pos) :- !.
          write_branches( [n( _E, Pos), H2|T], Pos1) :-
               node_number( H2, 1),
               !,
               B is Pos - Pos1, do_n_times( B, write( ' ')),
               write( '|'),
               Pos2 is Pos + 1,
               write_branches( T, Pos2).
            % normal categories
          write_branches( [_H, H2|T], Pos1) :-
               \+ node_number( H2, 1),
               !,
               print_branches( H2, Pos1, Pos2),
               write_branches( T, Pos2).
          write_branches( [], _).

               print_branches( List, Pos1, Pos2) :-
                    first_node( List, PosFirst),
                    last_node(  List, PosLast),
                    Mid is (PosFirst + PosLast) // 2,
                    B is PosFirst - Pos1 + 1, do_n_times( B, write( ' ')),
                    U is Mid - PosFirst - 1,  do_n_times( U, write( '_')),
                    write( '|'),
                    V is PosLast - Mid - 2,   do_n_times( V, write( '_')),
                    Pos2 is PosLast - 1.

                    first_node( [n( _, Pos)|_], Pos).

                    last_node( [_|T], Pos)        :-  last_node( T, Pos).
                    last_node( [n( _, Pos)], Pos) :-  !.    % 1. case: leaf
                    last_node( [n( _, Pos), [_|_]], Pos).   % 2. case: dominant node

            % leaves
          write_twigs( [_H, H2|T], T1, Pos) :-
               \+ (H2 = [_|_]),
               !,
               write_twigs( [H2|T], T1, Pos).
          write_twigs( [E], [], _Pos) :-
               \+ (E = [_|_]),
               !.
            % non branching, i.e. lexical categories
          write_twigs( [n( _, Pos), H|T], List, Pos1) :-
               node_number( H, 1),
               !,
               B is Pos - Pos1, do_n_times( B, write( ' ')),
               write( '|'),
               Pos2 is Pos + 1,
               write_twigs( T, List1, Pos2),
               append( H, List1, List).

            % normal categories
          write_twigs( [H, [H2|T2]|T], List, Pos1) :-
               !,
               print_twigs( H, [H2|T2], Pos1, Pos2),
               write_twigs( T, List1, Pos2),
               append( [H2|T2], List1, List).
          write_twigs( [], [], _).

               print_twigs( n( _H, _Pos), List, Pos1, Pos4) :-
                    first_node( List, PosFirst),
                    B is PosFirst - Pos1, do_n_times( B, write( ' ')),
                    write( /),
                    Pos2 is PosFirst + 1,
                    intermediate_node( List, Pos2, Pos3),
                    last_node( List, PosLast),
                    B2 is PosLast - Pos3 - 1, do_n_times( B2, write( ' ')),
                    write( \),
                    Pos4 is PosLast.

                    intermediate_node( [n( _, _)|T], Pos1, Pos2) :-
                         print_twigs_for_node( T, Pos1, Pos2).

                         print_twigs_for_node( [n( _, _)], Pos, Pos)                :-  !.
                         print_twigs_for_node( [n( _, _), [_Last|_Succ]], Pos, Pos) :-  !.
                         print_twigs_for_node( [n( _, Pos)|T], Pos1, Pos2) :-
                              !,
                              B is Pos - Pos1, do_n_times( B, write( ' ')),
                              write( '|'),
                              Pos3 is Pos + 1,
                              print_twigs_for_node( T, Pos3, Pos2).
                         print_twigs_for_node( [_|T], Pos1, Pos2) :-
                              print_twigs_for_node( T, Pos1, Pos2).

               node_number( [n( _, _)|T], 1) :-
                    \+ memberchk( n( _, _), T).



do_n_times( N, Goal) :-
    (  between( 1, N, _),
       call( Goal),
       fail
     ;
       true
     ).

%%% max( +X, +Y, -Max)
%%%   gets the max of X and Y
%
max( X, Y, X) :- X >= Y, !.
max( X, Y, Y) :- X <  Y.
