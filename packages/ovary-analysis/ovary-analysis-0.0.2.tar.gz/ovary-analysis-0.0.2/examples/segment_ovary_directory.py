from ovary_analysis.post_process.ovary import segment_ovary_dir

BASE_DIR = "/cluster/work/cobi/kevin/ivf/full_data_20220301/ovary_segmentation"
RAW_IM_DIR = "/cluster/work/cobi/kevin/ivf/full_data_20220301/raw_data/denoised"
PROBABILITY_THRESHOLD = 0.5
APPLY_SIGMOID = False
APPLY_SOFTMAX = True
DILATION_SIZE = None
MASK_PADDING = False


segment_ovary_dir(
    dir_path=BASE_DIR,
    raw_im_dir=RAW_IM_DIR,
    predictions_subdir='predictions',
    output_dir_name='segmentations',
    threshold=PROBABILITY_THRESHOLD,
    apply_sigmoid=APPLY_SIGMOID,
    apply_softmax=APPLY_SOFTMAX,
    prediction_index=1,
    dilation_size=DILATION_SIZE,
    mask_padding=MASK_PADDING,
    raw_im_key='raw_rescaled',
    follicle_labels_key=None,
    ovary_labels_key=None,
    prediction_key='predictions',
)
