function main()
    % clean
    close all;
    clear;
    clc;

    % constants
    cNum = 4; % number of clusters
 
    % read brain tumor dataset
    [imgIn, mask] = readCjdata('E:\eDocs\PhD\Y1S1\ELEC523\Project\1512427\brainTumorDataPublic_1-766\1.mat');

    % read BraTS
    %[imgIn, mask] = readNII('E:\eDocs\PhD\Y1S1\ELEC523\Project\MICCAI_BraTS_2019_Data_Training\MICCAI_BraTS_2019_Data_Training\HGG\BraTS19_2013_2_1\BraTS19_2013_2_1_t2.nii' ...
    %, 'E:\eDocs\PhD\Y1S1\ELEC523\Project\MICCAI_BraTS_2019_Data_Training\MICCAI_BraTS_2019_Data_Training\HGG\BraTS19_2013_2_1\BraTS19_2013_2_1_seg.nii');
    
    % convert image to grayscale
    if (size(imgIn, 3) ~= 1)
        imgIn = rgb2gray(imgIn);
    end
    
    figure;
    imshow(imgIn);
    
    figure;
    imshow(imgIn .* double(mask));
    
    % TODO: enhancement
    
    % skull stripping
    imgIn = skullStrip(imgIn);
    
    figure;
    imshow(imgIn);
    
    % run FLICM
    clusters = FLICM(imgIn, cNum);
    
    % use maximum average to find cluster for tumor
    sum = zeros(cNum, 1);
    count = zeros(cNum, 1);
    for r = 1:size(clusters, 1)
        for c = 1:size(clusters, 2)
            sum(clusters(r, c)) = sum(clusters(r, c)) + imgIn(r, c);
            count(clusters(r, c)) = count(clusters(r, c)) + 1;
        end
    end
    
    aMax = 0;
    kMax = 1;
    for k = 1:cNum
        if (aMax <= double(sum(k)) / double(count(k)))
            aMax = double(sum(k)) / double(count(k));
            kMax = k;
        end
    end
    
    mask = zeros(size(clusters));
    for r = 1:size(clusters, 1)
        for c = 1:size(clusters, 2)
            if (clusters(r,c) == kMax)
                mask(r, c) = 1.0;
            end
        end
    end
    
    % morphological operation
    se = strel('disk', 8);
    openMask = imopen(mask, se);
    
    % overlay
    imgOut = imgIn .* openMask;
    
    figure;
    imshow(imgOut);
end