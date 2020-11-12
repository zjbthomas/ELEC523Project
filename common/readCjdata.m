function [img, procImg, mask, ss] = readCjdata(imgPath, method)
    load(imgPath);
    
    switch method
        case 'otsu'
            img = cjdata.image;
        case 'flicm'
            img = minMaxNormalize(cjdata.image);
        otherwise
            error('Incorrect method!');
    end
    
    mask = cjdata.tumorMask;
    
    % skull stripping
    ss = skullStrip(minMaxNormalize(cjdata.image));
    
    % mask the gray image
    procImg = img;
    procImg(~ss) = 0;
    
    % show images
    subplot(2, 3, 1), imshow(minMaxNormalize(cjdata.image)); title('Ori. Image');
    subplot(2, 3, 2), imshow(mask); title('Ori. Mask');
    switch method
        case 'otsu'
            subplot(2, 3, 3), imshow(minMaxNormalize(procImg)); title('Skull Stripped');
        case 'fcm'
            subplot(2, 3, 3), imshow(procImg); title('Skull Stripped');
        case 'flicm'
            subplot(2, 3, 3), imshow(procImg); title('Skull Stripped');
        otherwise
            error('Incorrect method!');
    end
    
end