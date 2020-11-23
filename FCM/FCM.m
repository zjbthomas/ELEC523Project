function [masks, iter, diff] = FCM(dataset, ss, cNum, img, outputDir)
    %% parameters
    m = 2; 
    winSize = 3; % size of windows
    maxIter = 1000; % number of iterations
    thrE = 0.0000001; % threshold
    
    %% run FCM
    [clusters, iter, diff] = FCMClustering(img, cNum, m, winSize, maxIter, thrE);
    %% post-processing
    masks = SortMasks(dataset, ss, cNum, img, clusters, outputDir);
end

