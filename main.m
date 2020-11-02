function main()
    %% clean
    close all;
    clear;
    clc;

    %% constants
    cNum = 4; % number of clusters
 
    %% load images
    % read brain tumor dataset
    %imgPath = 'E:\eDocs\PhD\Y1S1\ELEC523\Project\1512427\brainTumorDataPublic_1-766\1.mat';
    imgPath = 'E:\Users\Dexaint\Downloads\1766-153.mat';
    [imgIn, oriMask] = readCjdata(imgPath);

    % read BraTS
    %[imgIn, mask] = readNII('E:\eDocs\PhD\Y1S1\ELEC523\Project\MICCAI_BraTS_2019_Data_Training\MICCAI_BraTS_2019_Data_Training\HGG\BraTS19_2013_2_1\BraTS19_2013_2_1_t2.nii' ...
    %, 'E:\eDocs\PhD\Y1S1\ELEC523\Project\MICCAI_BraTS_2019_Data_Training\MICCAI_BraTS_2019_Data_Training\HGG\BraTS19_2013_2_1\BraTS19_2013_2_1_seg.nii');
    
    %% pre-processing
    % convert image to grayscale
    if (size(imgIn, 3) ~= 1)
        imgIn = rgb2gray(imgIn);
    end
    
    figure;
    imshow(imgIn);
    
    figure;
    imshow(imgIn .* double(oriMask));
    
    % TODO: enhancement
    
    % skull stripping
    imgIn = skullStrip(imgIn);
    
    figure;
    imshow(imgIn);
    
    %% segmentation
    % run Otsu
    mask = Otsu(imgIn);
    
    % run FLICM
    % mask = FLICM(imgIn, cNum);
    
    % overlay
    imgOut = imgIn .* mask;
    
    figure;
    imshow(imgOut);
end