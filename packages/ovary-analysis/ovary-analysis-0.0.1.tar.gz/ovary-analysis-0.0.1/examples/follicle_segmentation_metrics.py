import os

from ovary_analysis.post_process.segmentation_metrics import quantify_performance_from_crossval


CROSSVAL_DIR = '/cluster/work/cobi/kevin/ivf/cross_validation_20220126/follicle_crossval_no_mask'
FOLD_DIR_PATTERN = 'fold_*'
PROB_THRESHOLDS = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
IOU_THRESH = 0.5
VOLUME_THRESHOLD = 30
VOXEL_SIZE_MM3 = 0.157288 * 0.157288 * 0.157288
PREDICTIONS_DIR_NAME = 'predictions'
PREDICTIONS_INDEX = 1
REF_DIR_NAME = 'test'
REF_FILE_PATTERN = '*.h5'
OUTPUT_NAME_BASE = 'follicle_crossval_no_mask'

performance_metrics, tp_table, seg_metrics = quantify_performance_from_crossval(
        crossval_dir=CROSSVAL_DIR,
        fold_dir_pattern=FOLD_DIR_PATTERN,
        prob_thresholds=PROB_THRESHOLDS,
        iou_thresh=IOU_THRESH,
        volume_threshold=VOLUME_THRESHOLD,
        voxel_size_mm3=VOXEL_SIZE_MM3,
        predictions_dir_name=PREDICTIONS_DIR_NAME,
        prediction_index=PREDICTIONS_INDEX,
        ref_dir_name=REF_DIR_NAME,
        ref_file_pattern = REF_FILE_PATTERN,
)

output_name_performance_metrics = OUTPUT_NAME_BASE + '_performance_metrics.csv'
output_path_performance_metrics = os.path.join(CROSSVAL_DIR, output_name_performance_metrics)
performance_metrics.to_csv(output_path_performance_metrics)

output_name_tp_table = OUTPUT_NAME_BASE + '_tp_table.csv'
output_path_tp_table = os.path.join(CROSSVAL_DIR, output_name_tp_table)
tp_table.to_csv(output_path_tp_table)

output_name_seg_metrics = OUTPUT_NAME_BASE + '_seg_metrics.csv'
output_path_seg_metrics = os.path.join(CROSSVAL_DIR, output_name_seg_metrics)
seg_metrics.to_csv(output_path_seg_metrics)
