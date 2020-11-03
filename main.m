function main()
    %% clean
    close all;
    clear;
    clc;

    %% constants
    dataset = 'brats'; % cjdata; brats;
    method = 'otsu'; % otsu; flicm;
    
    %% figure handle
    figure;
    suptitle([method ' on ' dataset]);
    
    %% load images
    switch dataset
        case 'cjdata'
            %imgPath = 'E:\eDocs\PhD\Y1S1\ELEC523\Project\1512427\brainTumorDataPublic_1-766\1.mat';
            imgPath = 'E:\Users\Dexaint\Downloads\1766-153.mat';
            [oriImg, procImg, oriMask] = readCjdata(imgPath, method);
        case 'brats'
            [oriImg, oriMask] = readNII('E:\eDocs\PhD\Y1S1\ELEC523\Project\MICCAI_BraTS_2019_Data_Training\MICCAI_BraTS_2019_Data_Training\HGG\BraTS19_CBICA_AAB_1\BraTS19_CBICA_AAB_1_flair.nii', ...
                'E:\eDocs\PhD\Y1S1\ELEC523\Project\MICCAI_BraTS_2019_Data_Training\MICCAI_BraTS_2019_Data_Training\HGG\BraTS19_CBICA_AAB_1\BraTS19_CBICA_AAB_1_seg.nii', ...
                method);
        otherwise
            error('Incorrect dataset!');
    end
    
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
end