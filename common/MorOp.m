function mask = MorOp(mask)
    %% parameters
    openSize = 2;
    dilateSize = 1;

    se = strel('disk', openSize);
    mask = imopen(mask, se);
    
    se = strel('disk', dilateSize);
    mask = imdilate(mask, se); 
end

