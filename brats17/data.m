close all;
clear;
clc;

%% parameters
maxMask = false;

%% constants
bratsBase = 'E:\eDocs\PhD\Y1S1\ELEC523\Project\MICCAI_BraTS_2019_Data_Training\MICCAI_BraTS_2019_Data_Training\HGG\';
resultBase = 'E:\eDocs\PhD\Y1S1\ELEC523\Project\brats17\result19\HGG\';

bratsList = { ...
    'BraTS19_CBICA_ATD_1', ...
    'BraTS19_CBICA_ATF_1', ...
    'BraTS19_CBICA_ATN_1', ...
    'BraTS19_CBICA_AAB_1', ...
    'BraTS19_CBICA_AAG_1', ...
    'BraTS19_CBICA_AAL_1', ...
    'BraTS19_CBICA_AAP_1', ...
    'BraTS19_CBICA_ABB_1', ...
    'BraTS19_CBICA_ABE_1', ...
    'BraTS19_CBICA_ABM_1', ...
    'BraTS19_CBICA_ABN_1', ...
    'BraTS19_CBICA_ABO_1', ...
    'BraTS19_CBICA_ABY_1', ...
    'BraTS19_CBICA_ALN_1', ...
    'BraTS19_CBICA_ALU_1', ...
    'BraTS19_CBICA_ALX_1', ...
    'BraTS19_CBICA_AME_1', ...
    'BraTS19_CBICA_AMH_1', ...
    'BraTS19_CBICA_ANG_1', ...
    'BraTS19_CBICA_ANI_1', ...
    'BraTS19_CBICA_ANP_1', ...
    'BraTS19_CBICA_ANV_1', ...
    'BraTS19_CBICA_ANZ_1', ...
    'BraTS19_CBICA_AOC_1', ...
    'BraTS19_CBICA_AOD_1', ...
    'BraTS19_CBICA_AOH_1', ...
    'BraTS19_CBICA_AOO_1', ...
    'BraTS19_CBICA_AOP_1', ...
    'BraTS19_CBICA_AOS_1', ...
    'BraTS19_CBICA_AOZ_1', ...
    'BraTS19_CBICA_APK_1', ...
    'BraTS19_CBICA_APR_1', ...
    'BraTS19_CBICA_APY_1', ...
    'BraTS19_CBICA_APZ_1', ...
    'BraTS19_CBICA_AQA_1', ...
    'BraTS19_CBICA_AQD_1', ...
    'BraTS19_CBICA_AQG_1', ...
    'BraTS19_CBICA_AQJ_1', ...
    'BraTS19_CBICA_AQN_1', ...
    'BraTS19_CBICA_AQO_1', ...
    'BraTS19_CBICA_AQP_1', ...
    'BraTS19_CBICA_AQQ_1', ...
    'BraTS19_CBICA_AQR_1', ...
    'BraTS19_CBICA_AQT_1', ...
    'BraTS19_CBICA_AQU_1', ...
    'BraTS19_CBICA_AQV_1', ...
    'BraTS19_CBICA_AQY_1', ...
    'BraTS19_CBICA_AQZ_1', ...
    'BraTS19_CBICA_ARF_1', ...
    'BraTS19_CBICA_ARW_1'
};

for p = bratsList
    % open log
    clc;
    fid = fopen(char(strcat(resultBase, '\', p, '.txt')), 'w');
    
    % read original data
    imgDir = char(strcat(bratsBase, '\', p, '\', p));
    [oriImg, oriMask, pos] = readNII(char(strcat(imgDir, '_flair.nii.gz')), ... % type not important, use FLAIR as it is clear
                        char(strcat(imgDir, '_seg.nii.gz')), ...
                        'flicm', maxMask); % method not important, use FLICM with normalization
    
    % read result
    resultNII = char(strcat(resultBase, '\', p, '.nii.gz'));
    masks = niftiread(resultNII);
    
    mask = minMaxNormalize(masks(:, :, pos));
    subplot(1, 3, 3), imshow(mask); title('Proc. Mask');
    
    % evaluation: use matlab function to calculate Dice and Jaccard
    dResult = dice(mask > 0, oriMask  > 0);    
    jResult = jaccard(mask > 0, oriMask > 0);
    
    fprintf(fid, 'Dice: %.4f\n',dResult);
    fprintf(fid, 'Jaccard: %.4f\n',jResult);
    
    % save figure
    saveas(gcf, char(strcat(resultBase, '\', p, '.jpg')));
    
    % close log
    fclose(fid);
end