function mask = FCMFind(dataset, method, ss, type, cNum, img, clusters, outputDir)
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
    
    % select a proper layer (the layer is chosen by experiments)
    if strcmp(dataset, 'brats')
        switch type
            case 'flair'
                kSel = sortI(1);
            case 't1'
                kSel = sortI(3);
            case 't1ce'
                if (strcmp(method, 'fcm') && cNum == 5)
                    kSel = sortI(4);
                else
                    kSel = sortI(1);
                end
            case 't2'
                if (strcmp(method, 'fcm') && cNum == 4)
                    kSel = sortI(1);
                else
                    kSel = sortI(2);
                end
            otherwise
                error('Incorrect type!');
        end
    else
        kSel = sortI(1);
    end

    classes = zeros([size(clusters) cNum]);
    mask = zeros(size(clusters));
    for r = 1:size(clusters, 1)
        for c = 1:size(clusters, 2)
            classes(r, c, clusters(r, c)) = 1.0;
            
            if (clusters(r,c) == kSel)
                mask(r, c) = 1.0;
            end
        end
    end
    
    % save matrices
    if (strcmp(dataset, 'cjdata') && ss)
        filename = char(strcat(outputDir, '_SS_C'));
    else
        filename = char(strcat(outputDir, '_C'));
    end
    
    for k = 1:cNum
        out = classes(:, :, k);
        if (k == kSel)
            save(strcat(filename, num2str(k), '_SEL.mat'), 'out');
        else
            save(strcat(filename, num2str(k), '.mat'),  'out');
        end
    end
end

