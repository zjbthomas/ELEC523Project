function mask = FLICM(img, cNum)
    %% parameters
    m = 2; 
    winSize = 3; % size of windows
    maxIter = 200; % number of iterations
    thrE = 0.0000001; % threshold
    
    %% run FLICM
    [clusters, iter] = FLICMClustering(img, cNum, m, winSize, maxIter, thrE);
    
    fprintf('Number of iteration: %d\n',iter);
    
    %% post-processing
    % use maximum average to find cluster for tumor
    sum = zeros(cNum, 1);
    count = zeros(cNum, 1);
    for r = 1:size(clusters, 1)
        for c = 1:size(clusters, 2)
            sum(clusters(r, c)) = sum(clusters(r, c)) + img(r, c);
            count(clusters(r, c)) = count(clusters(r, c)) + 1;
        end
    end
    
    aMax = 0;
    kMax = 1;
    for k = 1:cNum
        if (aMax <= double(sum(k)) / double(count(k)))
            aMax = double(sum(k)) / double(count(k));
            kMax = k;
        end
    end
    
    mask = zeros(size(clusters));
    for r = 1:size(clusters, 1)
        for c = 1:size(clusters, 2)
            if (clusters(r,c) == kMax)
                mask(r, c) = 1.0;
            end
        end
    end
    
    % morphological operation
    se = strel('disk', 10);
    mask = imopen(mask, se);
end

