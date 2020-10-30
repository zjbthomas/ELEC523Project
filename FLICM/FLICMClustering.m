function [clusters, iter] = FLICMClustering(imgIn, cNum, m, winSize, maxIter, thrE)    
    % initialize the fuzzy partition matrix
    U = zeros([size(imgIn), cNum]);
    
    Upos = zeros(size(imgIn));
    
    for r = 1:size(imgIn, 1)
        for c = 1:size(imgIn, 2)
            for k = 1:cNum
                U(r, c, k) = rand;
                Upos(r, c) = Upos(r,c) + U(r, c, k);
            end
            % normalize each position in U to sum up at 1
            for k = 1:cNum
                U(r, c, k) = U(r, c, k) / Upos(r, c);
            end
        end
    end
    
    % run core function of FLICM
    [U, iter] = FLICMCore(imgIn, U, m, cNum, winSize, maxIter, thrE);
    
    % clustering based on U
    clusters = zeros(size(imgIn));
    
    for r = 1:size(imgIn, 1)
        for c = 1:size(imgIn, 2)
            [uMax, class] = max(U(r, c, :)); 
            
            clusters(r, c) = class;
        end
    end
end