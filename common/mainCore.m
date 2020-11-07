function mainCore(dataset, method, oriImg, procImg, oriMask, outputDir)
    %% pre-processing
    % TODO: enhancement

    %% segmentation
    switch method
        case 'otsu'
            mask = Otsu(oriImg);
        case 'flicm'
            mask = FLICM(oriImg);
        otherwise
            error('Incorrect method!');
    end

    switch dataset
        case 'cjdata'
            subplot(2, 3, 4), imshow(mask); title('Proc. Mask');
        case 'brats'
            subplot(1, 3, 3), imshow(mask); title('Proc. Mask');
    end


    % also output results after skull stripping for cjdata
    if strcmp(dataset, 'cjdata')
        switch method
            case 'otsu'
                procMask = Otsu(procImg);
            case 'flicm'
                procMask = FLICM(procImg);
            otherwise
                error('Incorrect method!');
        end

        subplot(2, 3, 5), imshow(procMask); title('Proc. Mask Skull Stipped');
    end

    %% evaluation

    %% save results    
    saveas(gcf, char(strcat(outputDir, '.jpg')));
    
    diary(char(strcat(outputDir, '.txt')));
end

