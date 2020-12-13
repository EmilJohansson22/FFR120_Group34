%% Plot the results from CSV in Python
clear all
clc
load('tVec.csv')
load('overlapVec.csv')
load('covVec.csv')
load('maxPossible.csv')

%% Plot Coverage Vector
endIter = 50;
maxTmp = maxPossible(1:endIter,:);
xTmp = tVec(1:endIter,:);
yTmp = covVec(1:endIter,:);
plot(xTmp,yTmp)
hold on
plot(xTmp,maxTmp)

%% Plot overlap Vector
endIter = 50;
xTmp = tVec(1:endIter,:);
yTmp = overlapVec(1:endIter,:);
plot(xTmp,yTmp)
