from __future__ import annotations

import logging
from pathlib import Path

import pandas as pd
from joblib import Parallel, delayed
from radiomics import featureextractor
from tqdm import tqdm

from autorad.config import config
from autorad.config.type_definitions import PathLike
from autorad.data.dataset import ImageDataset
from autorad.utils.utils import time_it

log = logging.getLogger(__name__)


class FeatureExtractor:
    def __init__(
        self,
        dataset: ImageDataset,
        out_path: PathLike,
        feature_set: str = "pyradiomics",
        extraction_params: PathLike = "Baessler_CT.yaml",
        verbose: bool = False,
    ):
        """
        Args:
            dataset: ImageDataset containing image paths, mask paths, and IDs
            out_path: Path to save feature dataframe
            feature_set: library to use features from (for now only pyradiomics)
            extraction_params: path to the JSON file containing the extraction
                parameters, or a string containing the name of the file in the
                default extraction parameter directory
                (autorad.config.pyradiomics_params)
            verbose: logging for pyradiomics
        Returns:
            None
        """
        self.dataset = dataset
        self.out_path = out_path
        self.feature_set = feature_set
        self.extraction_params = self._get_extraction_param_path(
            extraction_params
        )
        self.verbose = verbose
        log.info("FeatureExtractor initialized")

    def _get_extraction_param_path(self, extraction_params: PathLike) -> Path:
        default_extraction_param_dir = Path(config.PARAM_DIR)
        if Path(extraction_params).is_file():
            result = Path(extraction_params)
        elif (default_extraction_param_dir / str(extraction_params)).is_file():
            result = default_extraction_param_dir / extraction_params
        else:
            raise ValueError(
                f"Extraction parameter file {extraction_params} not found."
            )
        return result

    def extract_features(self, num_threads: int = 1):
        """
        Run feature extraction process for a set of images.
        """
        # Get the feature extractor
        log.info("Initializing feature extractor")
        log.info(f"Using extraction params from {self.extraction_params}")
        self._initialize_extractor()

        # Get the feature values
        log.info("Extracting features")
        if num_threads > 1:
            feature_df = self.get_features_parallel(num_threads)
        else:
            feature_df = self.get_features()
        feature_df.to_csv(self.out_path, index=False)

    def _initialize_extractor(self):
        if self.feature_set == "pyradiomics":
            self.extractor = featureextractor.RadiomicsFeatureExtractor(
                str(self.extraction_params)
            )
        else:
            raise ValueError("Feature set not supported")
        return self

    def _get_features_for_single_case(
        self, case: pd.Series
    ) -> pd.Series | None:
        """
        Run extraction for one case and append results to feature_df
        Args:
            case: a single row of the dataset.df
        Returns:
            feature_series: concatenated pd.Series of features and case
        """
        image_path = case[self.dataset.image_colname]
        mask_path = case[self.dataset.mask_colname]
        id_ = case[self.dataset.ID_colname]
        if not Path(image_path).is_file():
            log.warning(
                f"Image not found. Skipping case... (path={image_path}"
            )
            return None
        if not Path(mask_path).is_file():
            log.warning(f"Mask not found. Skipping case... (path={mask_path}")
            return None
        try:
            feature_vector = self.extractor.execute(image_path, mask_path)
        except ValueError:
            log.error(f"Error extracting features for case {id_}")
            raise ValueError(f"Error extracting features for case {id_}")
        # copy the all the metadata for the case
        feature_series = pd.concat([case, pd.Series(feature_vector)])

        return feature_series

    @time_it
    def get_features(self) -> pd.DataFrame:
        """
        Run extraction for all cases.
        """
        feature_df_rows = []
        df = self.dataset.get_df()
        rows = df.iterrows()
        for _, row in tqdm(rows):
            feature_series = self._get_features_for_single_case(row)
            if feature_series is not None:
                feature_df_rows.append(feature_series)
        feature_df = pd.concat(feature_df_rows, axis=1).T
        return feature_df

    @time_it
    def get_features_parallel(self, num_threads: int) -> pd.DataFrame:
        df = self.dataset.get_df()
        try:
            with Parallel(n_jobs=num_threads) as parallel:
                results = parallel(
                    delayed(self._get_features_for_single_case)(df_row)
                    for _, df_row in df.iterrows()
                )
            feature_df = pd.concat(results, axis=1).T
            return feature_df
        except Exception:
            raise RuntimeError("Multiprocessing failed! :/")

    def get_feature_names(
        self, image_path: PathLike, mask_path: PathLike
    ) -> list[str]:
        """Get names of features from running it on the first case"""
        if not Path(image_path).is_file():
            raise ValueError(f"Image not found: {image_path}")
        if not Path(mask_path).is_file():
            raise ValueError(f"Mask not found: {mask_path}")
        feature_vector = self.extractor.execute(image_path, mask_path)
        feature_names = list(feature_vector.keys())
        return feature_names
