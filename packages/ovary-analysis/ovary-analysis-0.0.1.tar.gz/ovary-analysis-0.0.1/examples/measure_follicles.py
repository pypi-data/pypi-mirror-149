from ovary_analysis.measure.vol_measure import measure_dir

if __name__ == "__main__":
    FOLLICLE_SEGMENTATIONS_DIR = "/cluster/work/cobi/kevin/ivf/cross_validation_20220126/follicle_crossval_mask/fold_0/all_segmentations"

    ground_truth_df = measure_dir(
        dir_path=FOLLICLE_SEGMENTATIONS_DIR,
        file_pattern="*.h5",
        follicles_key="follicle_labels_rescaled"
    )
    ground_truth_df.to_csv("fold_0_all_measurements_ground_truth_20220404.csv")

    segmentation_df = measure_dir(
        dir_path=FOLLICLE_SEGMENTATIONS_DIR,
        file_pattern="*.h5",
        follicles_key="follicle_segmentation_rescaled"
    )
    segmentation_df.to_csv("fold_0_all_measurements_segmentation_20220404.csv")


