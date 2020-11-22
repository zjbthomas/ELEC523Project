import os
import re
import shutil

# parameters
RESULT_BASE = 'E:\\eDocs\\PhD\\Y1S1\\ELEC523\\Project\\results\\middle_slice_final\\'
DATASETS = ['brats'] # cjdata; brats;
METHODS = ['otsu', 'fcm', 'flicm'] # otsu; fcm; flicm;
CNUMS = [4, 5]

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
                            if (m is 'fcm' or m is 'flicm'):
                                match = re.search(r'mask ([0-9]+)', lines[5 + 17 * c])
                            else:
                                match = re.search(r'mask ([0-9]+)', lines[37])

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
                                    if (m is 'fcm' or m is 'flicm'):
                                        match = re.search(r'mask ([0-9]+)', lines[3 + 12 * c])
                                    else:
                                        match = re.search(r'mask ([0-9]+)', lines[26])

                                    mask = match.group(1) # no need to convert to int

                                    # copy png
                                    shutil.copyfile(subdir + os.sep + basename + '_' + mask + '.png', output_dir + os.sep + basename + '.png')