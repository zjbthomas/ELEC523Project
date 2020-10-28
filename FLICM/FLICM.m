function FLICM(imgPath)
    % clean
    close all;
    clear;
    clc;

    % parameters
    cNum = 4; % number of clusters
    m = 2; 
    winSize = 3; % size of windows
    maxIter = 200; % number of iterations
    thrE = 0.0000001; % threshold
    
    % load image
    oriImg = imread('eight.tif');
    normImg = double(oriImg) / 255.0;
    imgMat = normImg;
    
    %load('E:\eDocs\PhD\Y1S1\ELEC523\Project\1512427\brainTumorDataPublic_1-766\2.mat');
    %normImg = double(cjdata.image) / double(max(max(cjdata.image)));
    %imgMat = normImg;
    
    figure(1);
    imshow(normImg);
    
    %figure(2);
    %imshow(normImg .* double(cjdata.tumorMask));

    % run FLICM
    [imgOut, iter] = FLICMCluster(imgMat, cNum, m, winSize, maxIter, thrE);
    
    figure(3);
    imshow(imgOut);
    
    fprintf('Number of iteration: %d\n',iter);
end

