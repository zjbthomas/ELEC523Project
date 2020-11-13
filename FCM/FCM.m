function mask = FCM(dataset, cNum, img, outputDir, fid)
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
    
    fprintf(fid, 'Number of iteration: %d (diff: %.7f)\n', iter, diff);
    
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
    
    classes = zeros([size(clusters) cNum]);
    mask = zeros(size(clusters));
    for r = 1:size(clusters, 1)
        for c = 1:size(clusters, 2)
            classes(r, c, clusters(r, c)) = 1.0;
            
            if (clusters(r,c) == kMax)
                mask(r, c) = 1.0;
            end
        end
    end
    
    % morphological operation
    se = strel('disk', openSize);
    mask = imopen(mask, se);
    
    se = strel('disk', closeSize);
    mask = imclose(mask, se);
    
    % save matrices
    if strcmp(dataset, 'cjdata')
        filename = char(strcat(outputDir, '_SS_C'));
    else
        filename = char(strcat(outputDir, '_C'));
    end
    
    for k = 1:cNum
        out = classes(:, :, k);
        if (k == kMax)
            save(strcat(filename, num2str(k), '_MAX.mat'), 'out');
        else
            save(strcat(filename, num2str(k), '.mat'),  'out');
        end
    end
end

