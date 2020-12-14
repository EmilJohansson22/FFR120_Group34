%% Plot the results from CSV in Python
clear all
clc
load('tVec.csv')
load('overlapVec.csv')
load('covVec.csv')
load('maxPossible.csv')

%% Plot Coverage Vector
length = size(maxPossible,1)-1;
endIter = 30;
maxTmp = 100*maxPossible(1:endIter,:);
xTmp = tVec(1:endIter,:);
yTmp = 100*covVec(1:endIter,:);
yTmp(:) = yTmp(:)+20;
plot(xTmp,yTmp,'LineWidth',1.5,'DisplayName',"Coverage")
hold on
plot(xTmp,maxTmp,'LineWidth',1.5,'DisplayName',"Maximum coverage possible")
xlabel("Iterations")
ylabel("Covered cells (%)")
title("15 agents with range 10 and 10 buidlings")
legend("show","Location","SouthEast")

%% Plot overlap Vector
length = size(maxPossible,1)-1;
endIter = 30;
xTmp = tVec(1:endIter,:);
yTmp = 100*(overlapVec(1:endIter,:) ./ covVec(1:endIter))/(50*50);
plot(xTmp,yTmp, 'LineWidth',2)

xlabel("Iterations")
ylabel("Overlapping cells (%)")
title("15 agents with range 10 and 10 buidlings")

