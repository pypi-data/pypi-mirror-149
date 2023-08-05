
from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from .aoi import AOI



class SceneBase(BaseModel):
    request_id: str
    scene_id: str



class SceneSummary(SceneBase):
    scene_name: str
    tile: str
    tile_intersection_w_aoi: Optional[float]
    date_time: datetime

    thumbnail_url: Optional[str]

    subset_cloud_coverage: Optional[float]
    subset_no_data_percetange: Optional[float]
    overall_data_coverage: Optional[float]
    overall_data_perc_of_aoi:  Optional[float]
    scene_grade:  Optional[float]



class Scene(SceneSummary):
    aoi: Optional[AOI]
    scl_href_url: Optional[str]
    blue_channel_href: Optional[str]
    tile_cloud_coverage: Optional[float]
    mean_blue_channel: Optional[float]
    normalised_blue_channel: Optional[float]