function [masks, iter, diff] = FCM(dataset, ss, cNum, img, outputDir)
    %% parameters
    m = 2; 
    winSize = 3; % size of windows
    maxIter = 1000; % number of iterations
    thrE = 0.0000001; % threshold
    
    % for morphological operations
    openSize = 0;
    closeSize = 0;
    
    %% run FCM
    [clusters, iter, diff] = FCMClustering(img, cNum, m, winSize, maxIter, thrE);
    %% post-processing
    masks = FCMFind(dataset, ss, cNum, img, clusters, outputDir);
    
    % morphological operation
    %se = strel('disk', openSize);
    %mask = imopen(mask, se);
    
    %se = strel('disk', closeSize);
    %mask = imclose(mask, se);
end

