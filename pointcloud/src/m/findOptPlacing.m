function [ potMin, pivote1, pivote2, angulo ] = findOptPlacing( X, Y, delta )
%La función obtiene la ubicación óptima de traslape para 2 nubes de puntos
%dadas, usando un loop parfor

%Es posible calcular explícitamente la región dónde las escalones unitario son 1.
%Con base en esto, iremos siguiendo las particiones de [0,2pi] pertinentes.

%   ENTRADA:
%    * cloud1 y cloud2 son las nubes de puntos (matrices nx2)
%    * N es el número de ángulos con el que se trabajarán las rotaciones
%   SALIDA:
%    * potmin es el potencial mínimo correspondiente a la ubicación óptima
%    * pivote1 y pivote2 son las posiciones de los puntos en C1 y C2
%    respectivamente que deben hacerse coincidir para obtener la ubicación
%    óptima
%    * angulo es el ángulo de rotación que se usó para dicha ubicación

    M = size(X,1);
    N = size(Y,1);
    % Para hacer que las iteraciones del código sean independientes entre sí,
    % trabajaremos con un vector de potenciales mínimos, con tantas entradas
    % como el tamaño de cloud1. Inicializamos con un vector de entradas infinitas.
    % CONCEPTO IMPORTANTE: Sliced variables

    VectorPotMins = Inf(M,1);
    VectorPivotes2 = zeros(M,1);
    VectorAngulos = zeros(M,1);

    tic %EMPIEZA A MEDIR TIEMPO

    for p = 1:M

        Xp = X - X(p,:);
        XpNormsSq = diag(Xp*Xp');
        XpNormsSqMatrix = repmat(XpNormsSq, 1, N); %Clona horizontalmente
        XpAnglesMatrix = repmat(atan2(Xp(:,1), Xp(:,2)), 1, N);

        for q = 1:N

            %Montar las matrices apropiadas:
            Yq = Y - Y(q,:);
            YqNormsSq = diag(Yq*Yq')'; %Ojo: diag retorna columnas
            YqNormsSqMatrix = repmat(YqNormsSq, M,1); %Clona verticalmente
            YqAnglesMatrix = repmat(atan2(Yq(:,1), Yq(:,2))', M, 1);

            % Calcule la semiapertura de cada cono para cada ijpq. Se toma
            % la parte real para descartar valores imaginarios: el resultado
            % será cero.

            SemiApertureMatrix = real(acos((XpNormsSqMatrix + YqNormsSqMatrix - delta^2)./(2*sqrt(XpNormsSqMatrix.*YqNormsSqMatrix))));
            SemiApertures = SemiApertureMatrix(:);
            NonZeroPositions = find(SemiApertures); %¿ESTÁ SIRVIENDO?
            SemiApertures = SemiApertures(NonZeroPositions);

            XpAngles = XpAnglesMatrix(:);
            XpAngles = XpAngles(NonZeroPositions);

            YqAngles = YqAnglesMatrix(:);
            YqAngles = YqAngles(NonZeroPositions);

            SecondAngles = mod(XpAngles-YqAngles + SemiApertures, 2*pi);
            FirstAngles = mod(XpAngles-YqAngles - SemiApertures, 2*pi);

            %Calculemos la condición inicial para el problema de los
            %intervalos: ¿cuántos intervalos rodean 0? Todos aquellos para
            %los que SecondAngles<FirstAngles

            v=SecondAngles-FirstAngles;
            i=sum(v<0); %¿Por qué es que esto sirve?

            %Ahora vamos a ordenar los intervalos:

            EntryAngles = [FirstAngles ones(size(SecondAngles))];
            ExitAngles = [SecondAngles -ones(size(SecondAngles))];

            TaggedAngles = sortrows([ExitAngles; EntryAngles], 1);

            TaggedAngles(:,2) = cumsum(TaggedAngles(:,2));

            [Matches, place] = max(TaggedAngles(:,2));
            Matches = Matches + i;
            pot = M*N - Matches;

            if(pot<VectorPotMins(p))
                    VectorPotMins(p) = pot;
                    VectorPivotes2(p) = q;
                    VectorAngulos(p) = TaggedAngles(place,1);
            end

        end

        aviso = ['Barrido punto ',num2str(p), ' de ' num2str(M), ' en la nube 1.'];
        disp(aviso)

         %A VER CUÁNTO DURÓ

    end

    [potMin,pivote1]=min(VectorPotMins);
    pivote2=VectorPivotes2(pivote1);
    angulo=2*pi-VectorAngulos(pivote1); %¿POR QUE EL SUPLEMENTARIO?

    toc

end
