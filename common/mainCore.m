function mainCore(dataset, method, type, cNum, oriImg, procImg, oriMask, ss, useCache, outputDir)
    clc;
    % open log
    fid = fopen(char(strcat(outputDir, '.txt')), 'w');

    %% pre-processing
    % TODO: enhancement

    %% segmentation
    % original images
    if (~useCache)
        tic

        switch method
            case 'otsu'
                masks = Otsu(oriImg);
            case 'fcm'
                [masks, iter, diff] = FCM(dataset, false, cNum, oriImg, outputDir);
                fprintf(fid, 'Number of iteration: %d (diff: %.7f)\n', iter, diff);
            case 'flicm'
                [masks, iter, diff] = FLICM(dataset, false, cNum, oriImg, outputDir);
                fprintf(fid, 'Number of iteration: %d (diff: %.7f)\n', iter, diff);
            otherwise
                error('Incorrect method!');
        end
        
        fprintf(fid, 'Time: %.4f\n',toc);
    else
        % no cache for Otsu
        if (strcmp(method, 'otsu'))
            masks = Otsu(oriImg);
        else
            masks = zeros([size(oriImg) cNum]);
            for k = 1:cNum
                load(strcat(outputDir, '_C', num2str(k), '.mat'));
                masks(:, :, k) = out;
            end
        end
    end

    % skull stripping for cjdata
    if strcmp(dataset, 'cjdata')
        if (~useCache)
            % do skull stripping on input image
            tic

            switch method
                case 'otsu'
                    procMasks = Otsu(procImg);
                case 'fcm'
                    [procMasks, iter, diff] = FCM(dataset, true, cNum, procImg, outputDir);
                    fprintf(fid, 'Number of iteration (skull stripped): %d (diff: %.7f)\n', iter, diff);
                case 'flicm'
                    [procMasks, iter, diff] = FLICM(dataset, true, cNum, procImg, outputDir);
                    fprintf(fid, 'Number of iteration (skull stripped): %d (diff: %.7f)\n', iter, diff);
                otherwise
                    error('Incorrect method!');
            end

            fprintf(fid, 'Time (skull stripped): %.4f\n',toc);
        else
            % no cache for Otsu
            if (strcmp(method, 'otsu'))
                procMasks = Otsu(procImg);
            else
                procMasks = zeros([size(procImg) cNum]);
                for k = 1:cNum
                    load(strcat(outputDir, '_SS_C', num2str(k), '.mat'));
                    procMasks(:, :, k) = out;
                end
            end
        end
    end

    %% selection and evaluation
    if (strcmp(method, 'otsu'))
        select = 2;
    else
        select = cNum;
    end
    
    sMax = 1;
    dMax = 0.0;
    tMax = 'un';
    
    for s = 1:select
        fprintf(fid, '\nSelect mask %d\n', s);
        
        % select mask
        mask = masks(:, :, s);
        switch dataset
            case 'cjdata'
                subplot(3, 3, 4), imshow(mask); title('Proc. Mask');
            case 'brats'
                subplot(2, 3, 3), imshow(mask); title('Proc. Mask');
        end

        maskMO = MorOp(mask);
        switch dataset
        case 'cjdata'
            subplot(3, 3, 7), imshow(maskMO); title('Mask MO');
        case 'brats'
            subplot(2, 3, 4), imshow(maskMO); title('Mask MO');
        end

        
        % select skull stripped masks for cjdata
        if strcmp(dataset, 'cjdata')
            procMask = procMasks(:, :, s);
            
            % do skull stripping on mask
            procOnMask = mask;
            procOnMask(~ss) = 0;

            % show images
            subplot(3, 3, 5), imshow(procMask); title('Image Skull Stipped');
            subplot(3, 3, 6), imshow(procOnMask); title('Mask Skull Stipped');

            % MO
            procMaskMO = MorOp(procMask);
            procOnMaskMO = MorOp(procOnMask);

            subplot(3, 3, 8), imshow(procMaskMO); title('ImageSS MO');
            subplot(3, 3, 9), imshow(procOnMaskMO); title('MaskSS MO');
        end
        


        % original image
        [d, j, TP, TN, FP, FN, dM, jM] = evaluate(mask > 0, oriMask > 0);
        fprintf(fid, 'Dice: %.4f\n', d);
        fprintf(fid, 'Jaccard: %.4f\n', j);
        fprintf(fid, 'Statistics: TP = %d, TN = %d, FP = %d, FN = %d\n', TP, TN, FP, FN);
        fprintf(fid, 'Dice (manual): %.4f\n', dM);
        fprintf(fid, 'Jaccard (manual): %.4f\n', jM);

        if (d > dMax)
            sMax = s;
            dMax = d;
            tMax = 'ori';
        end

        [d, j, TP, TN, FP, FN, dM, jM] = evaluate(maskMO > 0, oriMask > 0);
        fprintf(fid, 'Dice (MO): %.4f\n', d);
        fprintf(fid, 'Jaccard (MO): %.4f\n', j);
        fprintf(fid, 'Statistics (MO): TP = %d, TN = %d, FP = %d, FN = %d\n', TP, TN, FP, FN);
        fprintf(fid, 'Dice (manual, MO): %.4f\n', dM);
        fprintf(fid, 'Jaccard (manual, MO): %.4f\n', jM);
        
        if (d > dMax)
            sMax = s;
            dMax = d;
            tMax = 'orimo';
        end
        
        switch dataset
            case 'cjdata'
                % SS on image
                [d, j, TP, TN, FP, FN, dM, jM] = evaluate(procMask > 0, oriMask > 0);
                fprintf(fid, 'Dice (skull stripped): %.4f\n', d);
                fprintf(fid, 'Jaccard (skull stripped): %.4f\n', j);
                fprintf(fid, 'Statistics (skull stripped): TP = %d, TN = %d, FP = %d, FN = %d\n', TP, TN, FP, FN);
                fprintf(fid, 'Dice (manual, skull stripped): %.4f\n', dM);
                fprintf(fid, 'Jaccard (manual, skull stripped): %.4f\n', jM);

                if (d > dMax)
                    sMax = s;
                    dMax = d;
                    tMax = 'ssimg';
                end

                [d, j, TP, TN, FP, FN, dM, jM] = evaluate(procMaskMO > 0, oriMask > 0);
                fprintf(fid, 'Dice (skull stripped, MO): %.4f\n', d);
                fprintf(fid, 'Jaccard (skull stripped, MO): %.4f\n', j);
                fprintf(fid, 'Statistics (skull stripped, MO): TP = %d, TN = %d, FP = %d, FN = %d\n', TP, TN, FP, FN);
                fprintf(fid, 'Dice (manual, skull stripped, MO): %.4f\n', dM);
                fprintf(fid, 'Jaccard (manual, skull stripped, MO): %.4f\n', jM);

                if (d > dMax)
                    sMax = s;
                    dMax = d;
                    tMax = 'ssimgmo';
                end
                
                %% SS on mask
                [d, j, TP, TN, FP, FN, dM, jM] = evaluate(procOnMask > 0, oriMask > 0);
                fprintf(fid, 'Dice (skull stripped on mask): %.4f\n', d);
                fprintf(fid, 'Jaccard (skull stripped on mask): %.4f\n', j);
                fprintf(fid, 'Statistics (skull stripped on mask): TP = %d, TN = %d, FP = %d, FN = %d\n', TP, TN, FP, FN);
                fprintf(fid, 'Dice (manual, skull stripped on mask): %.4f\n', dM);
                fprintf(fid, 'Jaccard (manual, skull stripped on mask): %.4f\n', jM);
                
                if (d > dMax)
                    sMax = s;
                    dMax = d;
                    tMax = 'ssmask';
                end

                [d, j, TP, TN, FP, FN, dM, jM] = evaluate(procOnMaskMO > 0, oriMask > 0);
                fprintf(fid, 'Dice (skull stripped on mask, MO): %.4f\n', d);
                fprintf(fid, 'Jaccard (skull stripped on mask, MO): %.4f\n', j);
                fprintf(fid, 'Statistics (skull stripped on mask, MO): TP = %d, TN = %d, FP = %d, FN = %d\n', TP, TN, FP, FN);
                fprintf(fid, 'Dice (manual, skull stripped on mask, MO): %.4f\n', dM);
                fprintf(fid, 'Jaccard (manual, skull stripped on mask, MO): %.4f\n', jM);
                
                if (d > dMax)
                    sMax = s;
                    dMax = d;
                    tMax = 'ssmaskmo';
                end
                
            case 'brats'
                if (strcmp(type, 't1') || strcmp(type, 't1ce'))
                    % for t1 and t1ce, test enhancing core
                    [d, j, TP, TN, FP, FN, dM, jM] = evaluate(mask > 0, oriMask == 1.0);
                elseif (strcmp(type, 't2'))
                    % for t2, test tumor core
                    [d, j, TP, TN, FP, FN, dM, jM] = evaluate(mask > 0, (oriMask == 0.25) | (oriMask == 1.00));
                end
                fprintf(fid, 'Dice (%s): %.4f\n', type, d);
                fprintf(fid, 'Jaccard (%s): %.4f\n', type, j);
                fprintf(fid, 'Statistics (%s): TP = %d, TN = %d, FP = %d, FN = %d\n', type, TP, TN, FP, FN);
                fprintf(fid, 'Dice (manual, %s): %.4f\n', type, dM);
                fprintf(fid, 'Jaccard (manual, %s): %.4f\n', type, jM);
                
                if (d > dMax)
                    sMax = s;
                    dMax = d;
                    tMax = 'target';
                end
                
                % MO
                if (strcmp(type, 't1') || strcmp(type, 't1ce'))
                    % for t1 and t1ce, test enhancing core
                    [d, j, TP, TN, FP, FN, dM, jM] = evaluate(maskMO > 0, oriMask == 1.0);
                elseif (strcmp(type, 't2'))
                    % for t2, test tumor core
                    [d, j, TP, TN, FP, FN, dM, jM] = evaluate(maskMO > 0, (oriMask == 0.25) | (oriMask == 1.00));
                end
                fprintf(fid, 'Dice (%s, MO): %.4f\n', type, d);
                fprintf(fid, 'Jaccard (%s, MO): %.4f\n', type, j);
                fprintf(fid, 'Statistics (%s, MO): TP = %d, TN = %d, FP = %d, FN = %d\n', type, TP, TN, FP, FN);
                fprintf(fid, 'Dice (manual, %s, MO): %.4f\n', type, dM);
                fprintf(fid, 'Jaccard (manual, %s, MO): %.4f\n', type, jM);
                
                if (d > dMax)
                    sMax = s;
                    dMax = d;
                    tMax = 'targetmo';
                end
        end

        % save figure
        saveas(gcf, char(strcat(outputDir, '_', num2str(s), '.png')));
    end
    
    % write maximum Dice
    fprintf(fid, '\nMaximum Dice %.4f at mask %d for %s\n', dMax, sMax, tMax);
    
    % close log
    fclose(fid);
end

