function main()
    %% clear
    clear;
    
    %% constants
    dataset = 'cjdata'; % cjdata; brats;
    method = 'otsu'; % otsu; fcm; flicm;
    
    types = {'flair', 't1', 't2', 't1ce'}; % type for brats
    
    %% generate paths
    [imgDirs, outputDirs] = generatePaths(dataset, method);
    
    %% run main core
    for i = 1:length(imgDirs)
        switch dataset
            case 'cjdata'
                mainInit(dataset, method);
                
                [oriImg, procImg, oriMask, ss] = readCjdata(imgDirs{i}, method);
                
                mainCore(dataset, method, oriImg, procImg, oriMask, ss, outputDirs{i});
            case 'brats'
                for t = types
                    mainInit(dataset, method);
                    
                    [oriImg, oriMask] = readNII(char(strcat(imgDirs{i}, '_', t, '.nii.gz')), ...
                        char(strcat(imgDirs{i}, '_seg.nii.gz')), ...
                        method);
                    
                    mainCore(dataset, method, oriImg, NaN, oriMask, NaN, regexprep(outputDirs{i}, '@@@', t));
                end
            otherwise
                error('Incorrect dataset!');
        end
    end
end