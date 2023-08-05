from ovary_analysis.post_process.ovary import post_process_ovary_cross_val

CROSS_VAL_DIR = '/cluster/work/cobi/kevin/ivf/cross_validation_20211031/ovary_crossval'
OVARY_DATASETS_DIR = '/cluster/work/cobi/kevin/ivf/cross_validation_20211031/converted_data/ovary_datasets_20211101'
PROBABILITY_THRESHOLD = 0.8
APPLY_SIGMOID = True
DILATION_SIZE = 5

post_process_ovary_cross_val(
    crossval_dir=CROSS_VAL_DIR,
    ovary_datasets_dir=OVARY_DATASETS_DIR,
    predictions_subdir='predictions',
    output_dir_name='segmentations',
    threshold=PROBABILITY_THRESHOLD,
    apply_sigmoid=APPLY_SIGMOID,
    prediction_index=0,
    dilation_size=DILATION_SIZE,
    raw_im_key='raw_rescaled',
    follicle_labels_key='follicle_labels_rescaled',
    ovary_labels_key='ovary_labels_rescaled',
    prediction_key='predictions',
)
