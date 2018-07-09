close all;
data = csvread('data.txt');

time = 1:length(data(:,1));
time = time / 7200 + 17;

figure(1)
plot(data)
grid on