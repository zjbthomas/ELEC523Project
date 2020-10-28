function [U, iter] = FLICMCore(img, U, m, cNum, winSize, maxIter, thrE)
    % constants
    sStep = (winSize - 1) / 2;
    
    dMax = 10.0;
    iter = 0;
    while (dMax >= thrE && iter < maxIter) % Step 6
        % backup the last U for calculating dMax
        UOld = U;
        
        % Step 4
        centers = calcCenters(img, UOld, cNum, m);
        
        % Step 5
        for r = 1:size(img, 1)
            for c = 1:size(img, 2)   
                Gji = zeros(cNum, 1);
                sqrd = zeros(cNum, 1);
                
                % preparation for Equ (19)
                for k = 1:cNum
                    Gji(k) = 0;
                    % calculate around the window
                    for ii = -sStep:sStep
                        for jj = -sStep:sStep
                            % dij
                            dist = sqrt(ii ^ 2 + jj ^ 2);
                            %xj -vk
                            rr = r + ii;
                            cc = c + jj;
                            if (rr > 0 && rr <= size(img, 1) && ...
                                cc > 0 && cc <= size(img, 2) && ... % within image
                                (ii ~= 0 || jj ~= 0) ) % not the same point
                                Gji(k) = Gji(k) + 1.0 / (dist + 1.0) * ...
                                    (1 - UOld(rr, cc, k)) ^ m * ...
                                    abs(img(rr, cc) - centers(k)) ^ 2; % Equ (17)
                            end
                        end
                    end
                    
                    sqrd(k) = (abs(img(r, c) - centers(k))) ^ 2;
                end
                
                % calcualte uki
                for k = 1:cNum
                    den = 0;
                    for j = 1:cNum
                        % calculate denominator and make sure it is not 0
                        denj = sqrd(j) + Gji(j);
                        if (denj == 0)
                            denj = eps;
                        end
                        den = den + ((sqrd(k) + Gji(k)) / denj) ^ (1 / (m - 1));
                    end
                    U(r, c, k) = 1 / den;
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