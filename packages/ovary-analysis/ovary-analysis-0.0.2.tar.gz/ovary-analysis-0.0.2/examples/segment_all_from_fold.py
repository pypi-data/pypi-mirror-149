from ovary_analysis.post_process.follicles import segment_follicles_fold

if __name__ == "__main__":
    FOLD_DIR_PATH = "/cluster/work/cobi/kevin/ivf/cross_validation_20220126/follicle_crossval_mask/fold_0"
    PREDICTIONS_DIR_NAME = "predictions"
    OUTPUT_DIR_NAME = 'all_segmentations'
    PROB_THRESHOLD = 0.5
    VOLUME_THRESHOLD = 30
    PREDICTION_INDEX = 1
    APPLY_SOFTMAX = True
    RAW_IM_KEY = 'raw_rescaled'
    FOLLICLES_LABELS_KEY = 'follicle_labels_rescaled'
    OVARY_SEGMENTATION_KEY = 'ovary_labels_rescaled'
    PREDICTIONS_KEY = 'predictions'

    for folder in ["test", "train", "val"]:
        segment_follicles_fold(
            fold_dir_path=FOLD_DIR_PATH,
            raw_im_dir_name=folder,
            output_dir_name=OUTPUT_DIR_NAME,
            predictions_dir_name=PREDICTIONS_DIR_NAME,
            prob_threshold=PROB_THRESHOLD,
            volume_threshold=VOLUME_THRESHOLD,
            prediction_index=PREDICTION_INDEX,
            apply_softmax=APPLY_SOFTMAX,
            raw_im_key=RAW_IM_KEY,
            follicle_labels_key=FOLLICLES_LABELS_KEY,
            ovary_segmentation_key=OVARY_SEGMENTATION_KEY,
            prediction_key=PREDICTIONS_KEY,
        )
