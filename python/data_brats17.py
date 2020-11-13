import os
import math

# parameters
RESULT_DIR = 'E:\\eDocs\\PhD\\Y1S1\\ELEC523\\Project\\brats17\\result19\\HGG'
OUTPUT_FILE = 'E:\\eDocs\\PhD\\Y1S1\\ELEC523\\Project\\results\\brats17.txt'

# init
results_cnt = 0

dice_sum = 0.0
jaccard_sum = 0.0

nan_cnt = 0
nan_path = []

# iterate over files
for subdir, dirs, files in os.walk(RESULT_DIR):
    for filename in files:
        filepath = subdir + os.sep + filename

        if filepath.endswith('.txt'):
            # read lines
            fin = open(filepath, 'r')
            lines = fin.readlines()
            fin.close()

            # Dice (line 1)
            val = float(lines[0].replace('Dice: ', '').replace('\n', ''))
            if (math.isnan(val)):
                nan_cnt = nan_cnt + 1
                nan_path.append(filename.replace('.txt',''))
            else:
                results_cnt = results_cnt + 1
                dice_sum = dice_sum + val

            # Jaccard (line 2)
            if (not math.isnan(val)):
                jaccard_sum = jaccard_sum + float(lines[1].replace('Jaccard: ', '').replace('\n', ''))
            
        
# output
fout = open(OUTPUT_FILE, 'w')

if (results_cnt != 0):
    fout.write('Number of images with valid results: ' + str(results_cnt) + '\n')
    fout.write('Dice: ' + str(dice_sum / results_cnt) + '\n')
    fout.write('Jaccard: ' + str(jaccard_sum / results_cnt) + '\n')

    fout.write('\n')

    fout.write('Number of images with NaN: ' + str(nan_cnt) + '\n')
    for p in nan_path:
        fout.write(p + '\n')


fout.close()