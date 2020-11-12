function [U, iter, dMax] = FCMCore(img, U, m, cNum, winSize, maxIter, thrE)
    % constants
    dMax = 10.0;
    iter = 0;
    while (dMax >= thrE && iter < maxIter) % Step 6
        % backup the last U for calculating dMax
        UOld = U;
        
        % Step 4
        centers = calcCenters(img, UOld, cNum, m); % same as FLICM
        
        % Step 5
        for r = 1:size(img, 1)
            for c = 1:size(img, 2)
                
                for j = 1:cNum
                    den = 0.0;
                    
                    dji = (abs(img(r, c) - centers(j))) ^ 2;
                    for k = 1:cNum
                        dki = (abs(img(r, c) - centers(k))) ^ 2;
                        
                        den = den + (dji / dki) ^ (2 / (m - 1));
                    end
                    
                    U(r, c, j) = 1 / den;
                end
                
            end
        end
        
        % Update dMax
        dMax = max(max(max(abs(UOld - U))));

        % Update iter
        iter = iter + 1;
        
        fprintf('Iteration %d, diff %.7f\n',iter, dMax);
    end
end