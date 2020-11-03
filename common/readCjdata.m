function [normImg, procImg, mask] = readCjdata(imgPath)
    load(imgPath);
    normImg = minMaxNormalize(cjdata.image);
    mask = cjdata.tumorMask;
    
    subplot(2, 3, 1), imshow(normImg); title('Ori. Image');
    subplot(2, 3, 2), imshow(mask); title('Ori. Mask');
    
    % skull stripping
    procImg = skullStrip(normImg);
    
    subplot(2, 3, 3), imshow(procImg); title('Skull Stripped');
end