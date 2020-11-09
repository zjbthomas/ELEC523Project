function mainCore(dataset, method, oriImg, procImg, oriMask, outputDir)
    clc;
    %% pre-processing
    % TODO: enhancement

    %% segmentation
    tic
    
    switch method
        case 'otsu'
            mask = Otsu(oriImg);
        case 'flicm'
            mask = FLICM(oriImg);
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
        
        tic
        
        switch method
            case 'otsu'
                procMask = Otsu(procImg);
            case 'flicm'
                procMask = FLICM(procImg);
            otherwise
                error('Incorrect method!');
        end
        
        fprintf('Time (skull stripped): %.4f\n',toc);

        subplot(2, 3, 5), imshow(procMask); title('Proc. Mask Skull Stipped');
    end

    %% evaluation
    dResult = dice(mask > 0, oriMask  > 0);    
    jResult = jaccard(mask > 0, oriMask > 0);
    
    fprintf('Dice: %.4f\n',dResult);
    fprintf('Jaccard: %.4f\n',jResult);
    
    if strcmp(dataset, 'cjdata')
        dProcResult = dice(mask > 0, procMask > 0);
        jProcResult = jaccard(mask > 0, procMask > 0);

        fprintf('Dice (skull stripped): %.4f\n',dProcResult);
        fprintf('Jaccard (skull stripped): %.4f\n',jProcResult);
    end
    
    %% save results    
    saveas(gcf, char(strcat(outputDir, '.jpg')));
    
    diary(char(strcat(outputDir, '.txt')));
end

