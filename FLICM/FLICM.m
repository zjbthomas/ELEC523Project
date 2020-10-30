function clusters = FLICM(img, cNum)
    % parameters
    m = 2; 
    winSize = 3; % size of windows
    maxIter = 200; % number of iterations
    thrE = 0.0000001; % threshold
    
    % run FLICM
    [clusters, iter] = FLICMClustering(img, cNum, m, winSize, maxIter, thrE);
    
    fprintf('Number of iteration: %d\n',iter);
end

