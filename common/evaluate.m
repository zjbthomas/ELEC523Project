function [d, j, TP, TN, FP, FN, dM, jM] = evaluate(proc, ori)
    % use matlab function to calculate Dice and Jaccard    
    d = dice(proc, ori);    
    j = jaccard(proc, ori);
    
    % checking number of TPs, FPs, TNs, FNs
    TP = 0; TN = 0; FP = 0; FN = 0;
    
    for r = 1:size(ori, 1)
        for c = 1:size(ori, 2)
            if (ori(r, c) > 0 && proc(r, c) > 0)
                TP = TP + 1;
            elseif (ori(r, c) == 0 && proc(r, c) == 0)
                TN = TN + 1;
            elseif (ori(r, c) == 0 && proc(r, c) > 0)
                FP = FP + 1;
            elseif (ori(r, c) > 0 && proc(r, c) == 0)
                FN = FN + 1;
            end
        end
    end
    
    % manually calculate Dice and Jaccard
    dM = 2 * TP / (2 * TP + FP + FN);
    jM = TP / (TP + FP + FN);
end

