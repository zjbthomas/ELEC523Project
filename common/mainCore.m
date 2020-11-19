function mainCore(dataset, method, type, cNum, oriImg, procImg, oriMask, ss, outputDir)
    clc;
    % open log
    fid = fopen(char(strcat(outputDir, '.txt')), 'w');

    %% pre-processing
    % TODO: enhancement

    %% segmentation
    % original images
    tic

    switch method
        case 'otsu'
            mask = Otsu(oriImg);
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

    % skull stripping for cjdata
    if strcmp(dataset, 'cjdata')
        % do skull stripping on input image
        tic

        switch method
            case 'otsu'
                procMask = Otsu(procImg);
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
    end

    %% selection and evaluation
    if (strcmp(dataset, 'cjdata') || strcmp(method, 'otsu'))
        select = 1;
    else
        select = cNum;
    end
    
    sMax = 1;
    dMax = 0.0;
    
    for s = 1:select
        fprintf(fid, '\nSelect mask %d\n', s);
        
        % select mask
        if (~strcmp(method, 'otsu'))
            mask = masks(:, :, s);
        end
        switch dataset
            case 'cjdata'
                subplot(2, 3, 4), imshow(mask); title('Proc. Mask');
            case 'brats'
                subplot(1, 3, 3), imshow(mask); title('Proc. Mask');
        end
        
        % select skull stripped masks for cjdata
        if strcmp(dataset, 'cjdata')
            if (~strcmp(method, 'otsu'))
                procMask = procMasks(:, :, s);
            end
            
            % do skull stripping on mask
            procOnMask = mask;
            procOnMask(~ss) = 0;

            % show images
            subplot(2, 3, 5), imshow(procMask); title('Image Skull Stipped');
            subplot(2, 3, 6), imshow(procOnMask); title('Mask Skull Stipped');
        end
        
        % original image
        [d, j, TP, TN, FP, FN, dM, jM] = evaluate(mask > 0, oriMask > 0);
        fprintf(fid, 'Dice: %.4f\n', d);
        fprintf(fid, 'Jaccard: %.4f\n', j);
        fprintf(fid, 'Statistics: TP = %d, TN = %d, FP = %d, FN = %d\n', TP, TN, FP, FN);
        fprintf(fid, 'Dice (manual): %.4f\n', dM);
        fprintf(fid, 'Jaccard (manual): %.4f\n', jM);

        % if brats, find maximum Dice here
        if strcmp(dataset, 'brats')
            if (d > dMax)
                sMax = s;
                dMax = d;
            end
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

                % for otsu, find maximum Dice here
                if strcmp(method, 'otsu')
                    if (d > dMax)
                        sMax = s;
                        dMax = d;
                    end
                end
                
                %% SS on mask
                [d, j, TP, TN, FP, FN, dM, jM] = evaluate(procOnMask > 0, oriMask > 0);
                fprintf(fid, 'Dice (skull stripped on mask): %.4f\n', d);
                fprintf(fid, 'Jaccard (skull stripped on mask): %.4f\n', j);
                fprintf(fid, 'Statistics (skull stripped on mask): TP = %d, TN = %d, FP = %d, FN = %d\n', TP, TN, FP, FN);
                fprintf(fid, 'Dice (manual, skull stripped on mask): %.4f\n', dM);
                fprintf(fid, 'Jaccard (manual, skull stripped on mask): %.4f\n', jM);
                
                % for otsu, find maximum Dice here
                if ~strcmp(dataset, 'otsu')
                    if (d > dMax)
                        sMax = s;
                        dMax = d;
                    end
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
        end

        % save figure
        saveas(gcf, char(strcat(outputDir, '_', num2str(s), '.png')));
    end
    
    % write maximum Dice
    fprintf(fid, '\nMaximum Dice %.4f at mask %d\n', dMax, sMax);
    
    % close log
    fclose(fid);
end

