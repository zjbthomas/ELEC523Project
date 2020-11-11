function mainCore(dataset, method, oriImg, procImg, oriMask, ss, outputDir)
    clc;
    
    %% pre-processing
    % TODO: enhancement

    %% segmentation
    tic
    
    switch method
        case 'otsu'
            mask = Otsu(oriImg);
        case 'flicm'
            mask = FLICM(dataset, oriImg, outputDir);
        otherwise
            error('Incorrect method!');
    end
    
    fprintf('Time: %.4f\n',toc);

    switch dataset
        case 'cjdata'
            subplot(2, 3, 4), imshow(mask); title('Proc. Mask');
        case 'brats'
            subplot(1, 3, 3), imshow(mask); title('Proc. Mask');
    end


    % also output results after skull stripping for cjdata
    if strcmp(dataset, 'cjdata')
        % do skull stripping on input image
        tic
        
        switch method
            case 'otsu'
                procMask = Otsu(procImg);
            case 'flicm'
                procMask = FLICM(dataset, procImg, outputDir);
            otherwise
                error('Incorrect method!');
        end
        
        fprintf('Time (skull stripped): %.4f\n',toc);

        % do skull stripping on mask
        procOnMask = mask;
        procOnMask(~ss) = 0;
        
        % show images
        subplot(2, 3, 5), imshow(procMask); title('Proc. Mask Skull Stipped');
        subplot(2, 3, 6), imshow(procOnMask); title('Mask After Skull Stipped');
    end

    %% evaluation
    % use matlab function to calculate Dice and Jaccard
    dResult = dice(mask > 0, oriMask  > 0);    
    jResult = jaccard(mask > 0, oriMask > 0);
    
    fprintf('Dice: %.4f\n',dResult);
    fprintf('Jaccard: %.4f\n',jResult);
    
    if strcmp(dataset, 'cjdata')
        dProcResult = dice(procMask > 0, oriMask > 0);
        jProcResult = jaccard(procMask > 0, oriMask > 0);

        fprintf('Dice (skull stripped): %.4f\n', dProcResult);
        fprintf('Jaccard (skull stripped): %.4f\n', jProcResult);
        
        dOnMaskResult = dice(procOnMask > 0, oriMask > 0);
        jOnMaskResult = jaccard(procOnMask > 0, oriMask > 0);
        
        fprintf('Dice (skull stripped on mask): %.4f\n', dOnMaskResult);
        fprintf('Jaccard (skull stripped on mask): %.4f\n', jOnMaskResult);
    end
    
    % manually calculate Dice and Jaccard (also for checking number of TPs,
    % FPs, TNs, FNs)
    TP_mask = 0; TN_mask = 0; FP_mask = 0; FN_mask = 0;
    
    if strcmp(dataset, 'cjdata')
        TP_procMask = 0; TN_procMask = 0;
        FP_procMask = 0; FN_procMask = 0;
        
        TP_procOnMask = 0; TN_procOnMask = 0;
        FP_procOnMask = 0; FN_procOnMask = 0;
    end
    
    for r = 1:size(oriMask, 1)
        for c = 1:size(oriMask, 2)
            % for mask
            if (oriMask(r, c) > 0 && mask (r, c) > 0)
                TP_mask = TP_mask + 1;
            elseif (oriMask(r, c) == 0 && mask(r, c) == 0)
                TN_mask = TN_mask + 1;
            elseif (oriMask(r, c) == 0 && mask(r, c) > 0)
                FP_mask = FP_mask + 1;
            elseif (oriMask(r, c) > 0 && mask(r, c) == 0)
                FN_mask = FN_mask + 1;
            end
            
            if strcmp(dataset, 'cjdata')
                % for procMask
                if (oriMask(r, c) > 0 && procMask (r, c) > 0)
                    TP_procMask = TP_procMask + 1;
                elseif (oriMask(r, c) == 0 && procMask(r, c) == 0)
                    TN_procMask = TN_procMask + 1;
                elseif (oriMask(r, c) == 0 && procMask(r, c) > 0)
                    FP_procMask = FP_procMask + 1;
                elseif (oriMask(r, c) > 0 && procMask(r, c) == 0)
                    FN_procMask = FN_procMask + 1;
                end
                % for procOnMask
                if (oriMask(r, c) > 0 && procOnMask (r, c) > 0)
                    TP_procOnMask = TP_procOnMask + 1;
                elseif (oriMask(r, c) == 0 && procOnMask(r, c) == 0)
                    TN_procOnMask = TN_procOnMask + 1;
                elseif (oriMask(r, c) == 0 && procOnMask(r, c) > 0)
                    FP_procOnMask = FP_procOnMask + 1;
                elseif (oriMask(r, c) > 0 && procOnMask(r, c) == 0)
                    FN_procOnMask = FN_procOnMask + 1;
                end
            end
        end
    end
    
    fprintf('Statistics: TP = %d, TN = %d, FP = %d, FN = %d\n', ...
        TP_mask, TN_mask, FP_mask, FN_mask);
    fprintf('Dice (manual): %.4f\n', ...
        2 * TP_mask / (2 * TP_mask + FP_mask + FN_mask));
    fprintf('Jaccard (manual): %.4f\n', ...
        TP_mask / (TP_mask + FP_mask + FN_mask));
    
    if strcmp(dataset, 'cjdata')
        fprintf('Statistics (skull stripped): TP = %d, TN = %d, FP = %d, FN = %d\n', ...
            TP_procMask, TN_procMask, FP_procMask, FN_procMask);
        fprintf('Dice (manual, skull stripped): %.4f\n', ...
        2 * TP_procMask / (2 * TP_procMask + FP_procMask + FN_procMask));
        fprintf('Jaccard (manual, skull stripped): %.4f\n', ...
            TP_procMask / (TP_procMask + FP_procMask + FN_procMask));
        
        fprintf('Statistics (skull stripped on mask): TP = %d, TN = %d, FP = %d, FN = %d\n', ...
            TP_procOnMask, TN_procOnMask, FP_procOnMask, FN_procOnMask);
        fprintf('Dice (manual, skull stripped on mask): %.4f\n', ...
        2 * TP_procOnMask / (2 * TP_procOnMask + FP_procOnMask + FN_procOnMask));
        fprintf('Jaccard (manual, skull stripped on mask): %.4f\n', ...
            TP_procOnMask / (TP_procOnMask + FP_procOnMask + FN_procOnMask));
    end

    %% save results
    % figure
    saveas(gcf, char(strcat(outputDir, '.jpg')));
    % log
    diary(char(strcat(outputDir, '.txt')));
end

