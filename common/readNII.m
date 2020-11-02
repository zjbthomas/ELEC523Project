function [normImg, mask] = readNII(imgPath, segPath)
    imgs = niftiread(imgPath);
    masks = niftiread(segPath);
    
    pos = ceil(size(imgs, 3) / 2); % assuming the best slice is at the center
    
    normImg = minMaxNormalize(imgs(:, :, pos));
    mask = minMaxNormalize(masks(:, :, pos));
end