% adapted from https://www.mathworks.com/matlabcentral/answers/172701-how-to-perform-skull-stripping-using-matlab
function [imgOut] = skullStrip(grayImage)
    % threshold to create a binary image (default: 20/255)
    binaryImage = grayImage > 0.08; 

    % get rid of small specks of noise
    binaryImage = bwareaopen(binaryImage, 10);

    % fill the image
    binaryImage = imfill(binaryImage, 'holes');

    % erode away pixels (default: 15)
    se = strel('disk', 20, 0);
    binaryImage = imerode(binaryImage, se);

    % mask the gray image
    imgOut = grayImage;
    imgOut(~binaryImage) = 0;
end