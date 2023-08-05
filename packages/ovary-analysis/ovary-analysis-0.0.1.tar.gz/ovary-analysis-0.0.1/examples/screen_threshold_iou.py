"""
This example creates a dataframe for screening
effect of probability threshold on IOU
"""
from ovary_analysis.post_process.segmentation_metrics import measure_iou_from_crossval


thresholds = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0,9]
crossval_dir = '/cluster/work/cobi/kevin/ivf/cross_validation_20220126/ovary_cross_validation'
measurement_table = measure_iou_from_crossval(
    crossval_dir=crossval_dir,
    fold_dir_pattern='fold_*',
    ref_dir='test',
    prediction_dir='predictions',
    thresholds=thresholds,
    label_key='ovary_labels_rescaled',
    prediction_key='predictions'
)

measurement_table.to_csv('ovary_ious.csv')
