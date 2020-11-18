clear;

%% parameters
datasets = {'brats'}; % cjdata; brats;
methods = {'fcm', 'flicm'}; % otsu; fcm; flicm;

%% constants
types = {'t1', 't2', 't1ce'}; % type for brats
cNums = {4, 5}; % number of clusters for FCM-based

%% main
for d = 1:length(datasets)
    for m = 1: length(methods)
        for c = 1: length(cNums)
            % generate paths
            [imgDirs, outputDirs] = generatePaths(datasets{d}, methods{m}, cNums{c});

            %% run main core
            for i = 1:length(imgDirs)
                switch datasets{d}
                    case 'cjdata'
                        mainInit(datasets{d}, methods{m});

                        [oriImg, procImg, oriMask, ss] = readCjdata(imgDirs{i}, methods{m});

                        mainCore(datasets{d}, methods{m}, NaN, cNums{c}, oriImg, procImg, oriMask, ss, outputDirs{i});
                    case 'brats'
                        for t = types
                            mainInit(datasets{d}, methods{m});

                            [oriImg, oriMask, pos] = readNII(char(strcat(imgDirs{i}, '_', t, '.nii.gz')), ...
                                char(strcat(imgDirs{i}, '_seg.nii.gz')), ...
                                methods{m});

                            mainCore(datasets{d}, methods{m}, char(t), cNums{c}, oriImg, NaN, oriMask, NaN, regexprep(outputDirs{i}, '@@@', t));
                        end
                    otherwise
                        error('Incorrect dataset!');
                end
            end
        end
    end
end
