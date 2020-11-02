function [normImg, mask] = readCjdata(imgPath)
    load(imgPath);
    normImg = minMaxNormalize(cjdata.image);
    mask = cjdata.tumorMask;
end