function [masks, iter, diff] = FLICM(dataset, ss, cNum, img, outputDir)
    %% parameters
    m = 2; 
    winSize = 3; % size of windows
    maxIter = 1000; % number of iterations
    thrE = 0.0000001; % threshold
    
    %% run FLICM
    [clusters, iter, diff] = FLICMClustering(img, cNum, m, winSize, maxIter, thrE);
    %% post-processing
    masks = FCMFind(dataset, ss, cNum, img, clusters, outputDir);
end

