function [img, mask] = readNII(imgPath, segPath, method)
    imgs = niftiread(imgPath);
    masks = niftiread(segPath);
    
    pos = ceil(size(imgs, 3) / 2); % assuming the best slice is at the center
    
    switch method
        case 'otsu'
            img = imgs(:, :, pos);
        case 'flicm'
            img = minMaxNormalize(imgs(:, :, pos));
        otherwise
            error('Incorrect method!');
    end
    
    mask = minMaxNormalize(masks(:, :, pos));
    
    % show images
    subplot(1, 3, 1), imshow(minMaxNormalize(imgs(:, :, pos))); title('Ori. Image');
    subplot(1, 3, 2), imshow(mask); title('Ori. Mask');
end