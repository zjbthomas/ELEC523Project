function mask = Otsu(img)
    %% constants
    % cjdata is int16 (0-32767)
    bits = 32768;
    
    % threashold for background removal: remove those smaller then 200 for
    % cjdata
    thres_bg = 200.0 / 32767.0;
    
	%% set the imaging editing area
    % For the threshold method to work, the huge black background outside
    % the head needs to be removed. 
    % The black area can impede the threshold finding algorithm from working
    % properly.
    for r = 1:size(img, 1)
        for c = 1:size(img, 2)
            if (img(r, c) <= thres_bg) 
                img(r, c) = NaN;
            end
        end
    end

    %% obtain the histogram
    histogram = zeros([bits 1]);

    for r = 1:size(img, 1)
        for c = 1:size(img, 2)
            if isnan(img(r, c)) == 0
                val = floor(img(r, c) * (bits - 1)) + 1;
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
            if img(r, c) >= double(level) / double((bits - 1))
                mask(r, c) = 1;
            end
        end
    end
end
