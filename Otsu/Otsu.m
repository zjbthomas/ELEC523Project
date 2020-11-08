function mask = Otsu(img)
    %% parameters
    openSize = 0;
    closeSize = 0;

    %% constants
    % int16 (0-32767)
    bits = 32768;
    
    % threashold for background removal: remove those smaller then 200
    thres_bg = 200;
    
	%% set the imaging editing area
    % the huge black background outside the head needs to be removed 

    procImg = zeros(size(img));
    
    for r = 1:size(img, 1)
        for c = 1:size(img, 2)
            if (img(r, c) <= thres_bg) 
                procImg(r, c) = NaN;
            else
                procImg(r, c) = img(r, c);
            end
        end
    end

    %% obtain the histogram
    histogram = zeros([bits 1]);

    for r = 1:size(img, 1)
        for c = 1:size(img, 2)
            if isnan(procImg(r, c)) == 0
                val = procImg(r, c) + 1;
                histogram(val) = histogram(val) + 1;
            end
        end
    end

    %% run Otsu
    total = sum(histogram);  % total number of pixels (except NaN)

    sumB = 0;
    wB = 0;
    maximum = 0.0;
    sum1 = dot(0:bits-1, histogram);
    for ii = 1:bits
        wF = total - wB;
        if wB > 0 && wF > 0
            mF = (sum1 - sumB) / wF;
            val = wB * wF * ((sumB / wB) - mF) * ((sumB / wB) - mF);
            if ( val >= maximum )
                level = ii; % the threshold
                maximum = val;
            end
        end
        wB = wB + histogram(ii);
        sumB = sumB + (ii-1) * histogram(ii);
    end

    %% generate mask
    mask = zeros(size(img));  % binary image editing area

    for r = 1:size(img, 1)
        for c = 1:size(img, 2)
            if img(r, c) >= level
                mask(r, c) = 1;
            end
        end
    end
    
    % morphological operation
    se = strel('disk', openSize);
    mask = imopen(mask, se);
    
    se = strel('disk', closeSize);
    mask = imclose(mask, se);
end
