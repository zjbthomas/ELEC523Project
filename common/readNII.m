function [img, mask, pos] = readNII(imgPath, segPath, method, maxMask)
    imgs = niftiread(imgPath);
    masks = niftiread(segPath);
    
    if (~maxMask)
        pos = ceil(size(imgs, 3) / 2); % assuming the best slice is at the center
    else
        % find the maximum tumor slice
        pos = 1;
        areaMax = 0;
        for p = 1:size(imgs, 3)
            area = sum(sum(masks(:, :, p) > 0));
            if (area > areaMax)
                areaMax = area;
                pos = p;
            end
        end
    end

    switch method
        case 'otsu'
            img = imgs(:, :, pos);
        case 'otsun'
            img = imgs(:, :, pos);
        case 'fcm'
            img = minMaxNormalize(imgs(:, :, pos));
        case 'flicm'
            img = minMaxNormalize(imgs(:, :, pos));
        otherwise
            error('Incorrect method!');
    end
    
    mask = double(masks(:, :, pos)) / 4.0;
    
    % show images
    subplot(2, 3, 1), imshow(minMaxNormalize(imgs(:, :, pos))); title('Ori. Image');
    subplot(2, 3, 2), imshow(mask); title('Ori. Mask');
end