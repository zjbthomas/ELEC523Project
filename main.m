function main()
    %% clear
    clear;
    
    %% constants
    dataset = 'brats'; % cjdata; brats;
    method = 'otsu'; % otsu; flicm;
    
    types = {'flair', 't1', 't2'}; % type for brats
    
    %% generate paths
    [imgDirs, outputDirs] = generatePaths(dataset, method);
    
    %% run main core
    for i = 1:length(imgDirs)
        switch dataset
            case 'cjdata'
                mainInit(dataset, method);
                
                [oriImg, procImg, oriMask] = readCjdata(imgDirs{i}, method);
                
                mainCore(dataset, method, oriImg, procImg, oriMask, outputDirs{i});
            case 'brats'
                for t = types
                    mainInit(dataset, method);
                    
                    [oriImg, oriMask] = readNII(char(strcat(imgDirs{i}, '_', t, '.nii.gz')), ...
                        char(strcat(imgDirs{i}, '_seg.nii.gz')), ...
                        method);

                    procImg = oriImg; % just a place-holder
                    
                    mainCore(dataset, method, oriImg, procImg, oriMask, regexprep(outputDirs{i}, '@@@', t));
                end
            otherwise
                error('Incorrect dataset!');
        end
    end
end