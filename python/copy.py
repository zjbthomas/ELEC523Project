import os
import re
import shutil

# parameters
RESULT_BASE = 'E:\\eDocs\\PhD\\Y1S1\\ELEC523\\Project\\results\\'
DATASETS = ['brats', 'cjdata'] # cjdata; brats;
METHODS = ['otsun'] # otsu; otsun; fcm; flicm;
CNUMS = [5]
USECACHE = False

# constants
TYPES = ['flair', 't1', 't2', 't1ce']

# reset final dir
final_base = RESULT_BASE + '\\final\\'
if (os.path.exists(final_base)):
    shutil.rmtree(final_base)
os.mkdir(final_base)

for d in DATASETS:
    for m in METHODS:
        for c in CNUMS:
            
            if (m is 'otsu'):
                result_dir = RESULT_BASE + '\\' + d + '_' + m + '\\'
                output_dir = final_base + '\\' + d + '_' + m + '\\'
            else:
                result_dir = RESULT_BASE + '\\' + d + '_' + m + '_' + str(c) + '\\'
                output_dir = final_base + '\\' + d + '_' + m + '_' + str(c) + '\\'

            # create output dir
            if (not os.path.exists(output_dir)):
                os.mkdir(output_dir)

            if (d is 'cjdata'):
                # iterate over files
                for subdir, dirs, files in os.walk(result_dir):
                    for filename in files:
                        filepath = subdir + os.sep + filename

                        if filepath.endswith('.txt'):
                            basename = filename.replace('.txt', '')
                            
                            # read lines
                            fin = open(filepath, 'r')
                            lines = fin.readlines()
                            fin.close()
                            
                            # copy txt
                            shutil.copyfile(filepath, output_dir + os.sep + filename)

                            # read selected mask
                            if (not USECACHE):
                                if (m is 'fcm' or m is 'flicm'):
                                    offset = 5
                                else:
                                    offset = 3
                            else:
                                offset = 1

                            # mask offset
                            if (m is 'otsun' or m is 'fcm' or m is 'flicm'):
                                match = re.search(r'mask ([0-9]+)', lines[offset + 32 * c])
                            else:
                                match = re.search(r'mask ([0-9]+)', lines[offset + 64])

                            mask = match.group(1) # no need to convert to int

                            # copy png
                            shutil.copyfile(subdir + os.sep + basename + '_' + mask + '.png', output_dir + os.sep + basename + '.png')


            elif (d is 'brats'):
                # iterate over files
                for subdir, dirs, files in os.walk(result_dir):
                    for filename in files:
                        filepath = subdir + os.sep + filename

                        if filepath.endswith('.txt'):
                            for t_i, t_val in enumerate(TYPES):
                                if (m in filename and t_val in filename):
                                    # a filter to separate t1 and t1ce
                                    if (t_val is 't1' and 't1ce' in filename):
                                        continue

                                    # read lines
                                    fin = open(filepath, 'r')
                                    lines = fin.readlines()
                                    fin.close()

                                    basename = filename.replace('.txt', '')

                                    # copy txt
                                    shutil.copyfile(filepath, output_dir + os.sep + filename)

                                    # read selected mask
                                    if (not USECACHE):
                                        if (m is 'fcm' or m is 'flicm'):
                                            offset = 3
                                        else:
                                            offset = 2
                                    else:
                                        offset = 1

                                    # mask offset
                                    if (m is 'otsun' or m is 'fcm' or m is 'flicm'):
                                        match = re.search(r'mask ([0-9]+)', lines[offset + 22 * c])
                                    else:
                                        match = re.search(r'mask ([0-9]+)', lines[offset + 44])

                                    mask = match.group(1) # no need to convert to int

                                    # copy png
                                    shutil.copyfile(subdir + os.sep + basename + '_' + mask + '.png', output_dir + os.sep + basename + '.png')