function masks = SortMasks(dataset, ss, cNum, img, clusters, outputDir)
    % use maximum average to find cluster for tumor
    sum = zeros(cNum, 1);
    count = zeros(cNum, 1);
    for r = 1:size(clusters, 1)
        for c = 1:size(clusters, 2)
            sum(clusters(r, c)) = sum(clusters(r, c)) + img(r, c);
            count(clusters(r, c)) = count(clusters(r, c)) + 1;
        end
    end
    
    avgs = zeros(cNum, 1);
    for k = 1:cNum
        avgs(k) = double(sum(k)) / double(count(k));
    end
    
    [sortAvgs, sortI] = sort(avgs, 'descend');
    
    masks = zeros([size(clusters) cNum]);
    for k = 1:cNum
        masks(:, :, k) = clusters == sortI(k);
    end
    
    % save matrices
    if (strcmp(dataset, 'cjdata') && ss)
        filename = char(strcat(outputDir, '_SS_C'));
    else
        filename = char(strcat(outputDir, '_C'));
    end
    
    for k = 1:cNum
        out = masks(:, :, k);
        save(strcat(filename, num2str(k), '.mat'),  'out');
    end
end

