function [imgOut, iter] = FLICMCluster(imgIn, cNum, m, winSize, maxIter, thrE)
    % convert image to grayscale
    if (size(imgIn, 3) ~= 1)
        gray = rgb2gray(imgIn);
    else
        gray = imgIn;
    end
    
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
    [U, iter] = FLICMCore(gray, U, m, cNum, winSize, maxIter, thrE);
    
    % clustering based on U
    imgOut = zeros(size(imgIn));
    
    for r = 1:size(imgIn, 1)
        for c = 1:size(imgIn, 2)
            [uMax, class] = max(U(r, c, :)); 
            
            imgOut(r, c) = double(class) / double(cNum);
        end
    end
end