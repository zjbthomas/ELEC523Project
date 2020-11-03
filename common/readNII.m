function [normImg, mask] = readNII(imgPath, segPath)
    imgs = niftiread(imgPath);
    masks = niftiread(segPath);
    
    pos = ceil(size(imgs, 3) / 2); % assuming the best slice is at the center
    
    normImg = minMaxNormalize(imgs(:, :, pos));
    mask = minMaxNormalize(masks(:, :, pos));
    
    subplot(1, 3, 1), imshow(normImg); title('Ori. Image');
    subplot(1, 3, 2), imshow(mask); title('Ori. Mask');
end