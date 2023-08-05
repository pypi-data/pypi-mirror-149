from ovary_analysis.post_process.follicles import post_process_follicles_cross_val


CROSSVAL_DIR_PATH = '/cluster/work/cobi/kevin/ivf/cross_validation_20220126/follicle_crossval_mask'
FOLD_DIR_PATTERN = 'fold_*'
RAW_IM_DIR_NAME = 'test'
PREDICTIONS_DIR_NAME = 'predictions'
OUTPUT_DIR_NAME = 'segmentations'
PROB_THRESHOLD = 0.5
VOLUME_THRESHOLD = 30
PREDICTION_INDEX = 1
APPLY_SOFTMAX = True
RAW_IM_KEY = 'raw_rescaled'
FOLLICLES_LABELS_KEY = 'follicle_labels_rescaled'
OVARY_SEGMENTATION_KEY = 'ovary_labels_rescaled'
PREDICTIONS_KEY = 'predictions'

post_process_follicles_cross_val(
    crossval_dir_path=CROSSVAL_DIR_PATH,
    fold_dir_pattern=FOLD_DIR_PATTERN,
    raw_im_dir_name=RAW_IM_DIR_NAME,
    predictions_dir_name=PREDICTIONS_DIR_NAME,
    output_dir_name=OUTPUT_DIR_NAME,
    prob_threshold=PROB_THRESHOLD,
    volume_threshold=VOLUME_THRESHOLD,
    prediction_index=PREDICTION_INDEX,
    apply_softmax=APPLY_SOFTMAX,
    raw_im_key=RAW_IM_KEY,
    follicle_labels_key=FOLLICLES_LABELS_KEY,
    ovary_segmentation_key=OVARY_SEGMENTATION_KEY,
    prediction_key=PREDICTIONS_KEY
)
