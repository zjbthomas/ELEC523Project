clear;

%% parameters
datasets = {'brats', 'cjdata'}; % cjdata; brats;
methods = {'otsun'}; % otsu; otsun; fcm; flicm;
maxMask = false;
resetDirs = true;
useCache = false;

%% constants
types = {'flair', 't1', 't2', 't1ce'}; % type for brats
cNums = {5}; % number of clusters

%% main
for d = 1:length(datasets)
    for m = 1: length(methods)
        for c = 1: length(cNums)
            % generate paths
            [imgDirs, outputDirs] = generatePaths(datasets{d}, methods{m}, cNums{c}, resetDirs && ~useCache);

            %% run main core
            for i = 1:length(imgDirs)
                switch datasets{d}
                    case 'cjdata'
                        mainInit(datasets{d}, methods{m});

                        [oriImg, procImg, oriMask, ss] = readCjdata(imgDirs{i}, methods{m});

                        mainCore(datasets{d}, methods{m}, NaN, cNums{c}, oriImg, procImg, oriMask, ss, useCache, outputDirs{i});
                    case 'brats'
                        for t = types
                            mainInit(datasets{d}, methods{m});

                            [oriImg, oriMask, pos] = readNII(char(strcat(imgDirs{i}, '_', t, '.nii.gz')), ...
                                char(strcat(imgDirs{i}, '_seg.nii.gz')), ...
                                methods{m}, maxMask);

                            mainCore(datasets{d}, methods{m}, char(t), cNums{c}, oriImg, NaN, oriMask, NaN, useCache, regexprep(outputDirs{i}, '@@@', t));
                        end
                    otherwise
                        error('Incorrect dataset!');
                end
            end
        end
    end
end
