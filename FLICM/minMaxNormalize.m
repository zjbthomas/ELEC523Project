% adapted from https://github.com/chengjun583/brainTumorRetrieval/blob/9d2949a230e45a25f8be1b6f608cb9bf026c96e6/minMaxNormalize.m
function imNor = minMaxNormalize(im)
    % Normalize im into the range of [0, 1] using min-max normalization

    sz=size(im);
    imc=single(im(:));

    valMin = min(imc);
    valMax = max(imc);
    imcn=(imc-valMin)./(valMax-valMin);

    imNor=reshape(imcn, sz);
end