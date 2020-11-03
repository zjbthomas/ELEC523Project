function main()
    %% clean
    close all;
    clear;
    clc;

    %% constants
    cNum = 4; % number of clusters
    dataset = 'brats'; % cjdata; brats;
    method = 'flicm'; % otsu; flicm;
    
    %% figure handle
    figure;
    suptitle([method ' on ' dataset]);
    
    %% load images
    switch dataset
        case 'cjdata'
            %imgPath = 'E:\eDocs\PhD\Y1S1\ELEC523\Project\1512427\brainTumorDataPublic_1-766\1.mat';
            imgPath = 'E:\Users\Dexaint\Downloads\1766-153.mat';
            [normImg, procImg, oriMask] = readCjdata(imgPath);
        case 'brats'
            [normImg, oriMask] = readNII('E:\eDocs\PhD\Y1S1\ELEC523\Project\MICCAI_BraTS_2019_Data_Training\MICCAI_BraTS_2019_Data_Training\HGG\BraTS19_CBICA_AAB_1\BraTS19_CBICA_AAB_1_t2.nii' ...
            , 'E:\eDocs\PhD\Y1S1\ELEC523\Project\MICCAI_BraTS_2019_Data_Training\MICCAI_BraTS_2019_Data_Training\HGG\BraTS19_CBICA_AAB_1\BraTS19_CBICA_AAB_1_seg.nii');
        otherwise
            error('Incorrect dataset!');
    end
    
    %% pre-processing
    % TODO: enhancement

    %% segmentation
    switch method
        case 'otsu'
            normMask = Otsu(normImg);
        case 'flicm'
            normMask = FLICM(normImg, cNum);
        otherwise
            error('Incorrect method!');
    end
    
    % overlay
    normImgOut = normMask;
    
    switch dataset
        case 'cjdata'
            subplot(2, 3, 4), imshow(normImgOut); title('Proc. Mask');
        case 'brats'
            subplot(1, 3, 3), imshow(normImgOut); title('Proc. Mask');
    end
    
    
    % also output results after skull stripping for cjdata
    if strcmp(dataset, 'cjdata')
        switch method
            case 'otsu'
                procMask = Otsu(procImg);
            case 'flicm'
                procMask = FLICM(procImg, cNum);
            otherwise
                error('Incorrect method!');
        end
        
        % overlay
        procImgOut = procMask;
        subplot(2, 3, 5), imshow(procImgOut); title('Proc. Mask Skull Stipped');
    end
    
    %% evaluation
end