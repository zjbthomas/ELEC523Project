function [mask, iter, diff] = FLICM(dataset, ss, type, cNum, img, outputDir)
    %% parameters
    m = 2; 
    winSize = 3; % size of windows
    maxIter = 1000; % number of iterations
    thrE = 0.0000001; % threshold
    
    % for morphological operations
    openSize = 0;
    closeSize = 0;
    
    %% run FLICM
    [clusters, iter, diff] = FLICMClustering(img, cNum, m, winSize, maxIter, thrE);
    %% post-processing
    mask = FCMFind(dataset, 'flicm', ss, type, cNum, img, clusters, outputDir);
    
    % morphological operation
    se = strel('disk', openSize);
    mask = imopen(mask, se);
    
    se = strel('disk', closeSize);
    mask = imclose(mask, se);
end

