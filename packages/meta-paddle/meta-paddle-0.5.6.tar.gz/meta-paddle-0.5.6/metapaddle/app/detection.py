import os
import cv2
import yaml
from ..model_zoo import Detector, DetectorSOLOv2, DetectorPicoDet


class Detection:
    def __init__(self, model_dir, output_dir='outputs', device='cpu', run_mode='paddle'):
        deploy_file = os.path.join(model_dir, 'infer_cfg.yml')
        with open(deploy_file) as f:
            yml_conf = yaml.safe_load(f)
        arch = yml_conf['arch']
        detector_func = 'Detector'
        if arch == 'SOLOv2':
            detector_func = 'DetectorSOLOv2'
        elif arch == 'PicoDet':
            detector_func = 'DetectorPicoDet'

        self.detector = eval(detector_func)(
            model_dir=model_dir,
            device=device,
            run_mode=run_mode,
            batch_size=1,
            trt_min_shape=1,
            trt_max_shape=1280,
            trt_opt_shape=640,
            trt_calib_mode=False,
            cpu_threads=1,
            enable_mkldnn=False,
            enable_mkldnn_bfloat16=False,
            threshold=0.5,
            output_dir=output_dir)

    def predict(self, image, threshold=0.5):
        results = self.detector.predict_image([image], repeats=100)
        results = self.detector.filter_box(results, threshold=threshold)
        self.detector.det_times.info(average=True)
        return results

    def show(self, img, results):
        for r in results['boxes']:
            cls, bbox, score = int(r[0]), r[2:], r[1]
            text = self.detector.pred_config.labels[cls] + '-' + str(round(score, 2))
            cv2.putText(img, text,
                        (int(bbox[0]), int(bbox[1])),
                        cv2.FONT_HERSHEY_COMPLEX, 1.0, (0, 255, 0), 1)
            cv2.rectangle(img, (int(bbox[0]), int(bbox[1])), (int(bbox[2]), int(bbox[3])), (255, 0, 255), 2)
        return img
