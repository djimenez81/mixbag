function [Plot, SubC, Indices ] = findMaxCommonSubcloud( C1, C2, pivote1, pivote2, angulo, tolerancia )
%PRINTMAXSUBCLOUD Extrae la subnube maximal en común entre C1 y C2
% Esta función requiere especificar la tolerancia en el workspace primero.

  R = [cos(angulo), -sin(angulo); sin(angulo), cos(angulo)];

  n=size(C1,1);

  C1nueva = C1 - C1(pivote1,:);
  C2nueva = (C2 - C2(pivote2,:))*R';

  %Creamos matrices vacías para guardar los elementos de la subnube con sus
  %índices respectivos
  SubC = zeros(0,2);
  Indices = zeros(0,2);

  for i=1:n

    j=n+1-i; %Vamos de atrás hacia adelante para evitar problemas al eliminar filas.

    X = C2nueva-C1nueva(j,:);
    VectDistAC2 = diag(X*X');
    [distMin,indiceMin]=min(VectDistAC2);

    if(distMin<=tolerancia)
      SubC = [SubC; C1nueva(j,:)];
      Indices = [Indices; [j indiceMin]];

      %Eliminamos los puntos emparejados. PROFE, ¿ESTO FUNCIONA?
      %Hice pruebas y parece que sí.
      C1nueva(j,:) = [];
      C2nueva(indiceMin,:)=[];

    end

  end

  Plot = scatter(SubC(:,1), SubC(:,2), 20, 'rs', 'LineWidth', 2)

end
