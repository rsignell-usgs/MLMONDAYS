
## IMPORTS
###############################################################

from imports import *

###############################################

imdir = '/media/marda/TWOTB/USGS/DATA/tamucc_coastal_imagery/subset'
recoded_dir = '/media/marda/TWOTB/USGS/DATA/tamucc_coastal_imagery/subset_recoded_12class'
tfrecord_dir = '/media/marda/TWOTB/USGS/SOFTWARE/DL-CDI2020/4_UnsupImageRecog/data/tamucc/subset_12class/'+str(TARGET_SIZE)

csvfile = '/media/marda/TWOTB/USGS/DATA/tamucc_coastal_imagery/tamucc_subset.csv'



dat = pd.read_csv(csvfile)

orig_classes = np.unique(dat['class'].values).tolist()

files = []
classes = []
for f,c in zip(dat.file.values, dat['class'].values):
    files.append(f)
    class_idx = [i for i,k in enumerate(orig_classes) if k==c][0]
    classes.append(class_idx)


cnts = np.bincount(classes, minlength=len(orig_classes))

CLASSES = [k for i,k in enumerate(orig_classes) if cnts[i]>64]

print(CLASSES)

# ['exposed_riprap_structures', 'exposed_tidal_flats', 'exposed_walls_other_structures',
# 'finegrained_sand_beaches', 'gravel_shell_beaches', 'mixed_sand_gravel_shell_beaches',
# 'salt_brackish_water_marshes', 'scarps_steep_slopes_clay', 'scarps_steep_slopes_sand',
# 'sheltered_scarps', 'sheltered_solid_manmade', 'sheltered_tidal_flats']


files = []
classes = []
for f,c in zip(dat.file.values, dat['class'].values):
   if c in CLASSES: #only take certain files
       files.append(f)
       classes.append(c)

print(len(files))

# for f,c in zip(files, classes):
#    shutil.copy(imdir+os.sep+f, recoded_dir+os.sep+c+'_'+f)
#


im, lab = read_image_and_label(recoded_dir+os.sep+'sheltered_solid_manmade_IMG_7729_SecQN_Sum12_Pt3.jpg')
print(lab.numpy())
class_num = np.argmax(np.array(CLASSES)==lab)
print(class_num)

im, lab = read_image_and_label(recoded_dir+os.sep+'finegrained_sand_beaches_IMG_0763_SecBC_Spr12.jpg')
print(lab.numpy())
class_num = np.argmax(np.array(CLASSES)==lab)
print(class_num)

im, lab = read_image_and_label(recoded_dir+os.sep+'salt_brackish_water_marshes_IMG_2138_SecDE_Spr12.jpg')
print(lab.numpy())
class_num = np.argmax(np.array(CLASSES)==lab)
print(class_num)

im, lab = read_image_and_label(recoded_dir+os.sep+'gravel_shell_beaches_IMG_5574_SecOPQ_Sum12_Pt3.jpg')
print(lab.numpy())
class_num = np.argmax(np.array(CLASSES)==lab)
print(class_num)


CLASSES = [c.encode() for c in CLASSES]

nb_images=len(tf.io.gfile.glob(recoded_dir+os.sep+'*.jpg'))

SHARDS = int(nb_images / ims_per_shard) + (1 if nb_images % ims_per_shard != 0 else 0)
print(SHARDS)

shared_size = int(np.ceil(1.0 * nb_images / SHARDS))
print(shared_size)


tamucc_dataset = get_dataset_for_tfrecords(recoded_dir, shared_size)

write_records(tamucc_dataset, tfrecord_dir, CLASSES)