#
#             Zhadevv Project
#             --MIT License--
#
# Feed Me Starnya Bang:>
# Project 100% Open Source
# Bebas Recode, Deploy Production. KECUALI
# Diperjual-Belikan.
#
# Project ini Sepenuhnya Gratis, Makannua ksih Bintang Dong anj:>
# *bercanda ajahh
#
# Regards
# Zhadevv
#

from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field

class DonghuaHomeSlider(BaseModel):
    title: str
    slug: str
    thumbnail: str
    description: str
    url: str
    
class DonghuaHomePopular(BaseModel):
    title: str
    slug: str
    thumbnail: str
    episode: str
    type: str
    badge: str
    url: str
    
class DonghuaHomeLatest(BaseModel):
    title: str
    slug: str
    thumbnail: str
    episode: str
    type: str
    badge: str
    url: str
    
class DonghuaHomeRecommendationTab(BaseModel):
    id: str
    name: str
    active: bool
    
class DonghuaHomeRecommendationItem(BaseModel):
    status: str
    type: str
    title: str
    slug: str
    thumbnail: str
    episode: str
    badge: str
    url: str
    
class DonghuaHomeOngoingSeries(BaseModel):
    title: str
    slug: str
    episode: str
    url: str
    
class DonghuaHomePopularSeriesItem(BaseModel):
    top: str
    title: str
    slug: str
    thumbnail: str
    genre: List[str]
    rating: str
    url: str
    
class DonghuaHomeNewMovie(BaseModel):
    title: str
    slug: str
    thumbnail: str
    genres: List[str]
    release_date: str
    url: str
    
class DonghuaHomeGenre(BaseModel):
    title: str
    slug: str
    url: str
    
class DonghuaHomeSeason(BaseModel):
    title: str
    slug: str
    count: str
    url: str
    
class DonghuaHomeResponse(BaseModel):
    slider: List[DonghuaHomeSlider] = Field(default_factory=list)
    popular_today: List[DonghuaHomePopular] = Field(default_factory=list)
    latest_release: List[DonghuaHomeLatest] = Field(default_factory=list)
    recommendation: Dict[str, Any] = Field(default_factory=dict)
    ongoing_series: List[DonghuaHomeOngoingSeries] = Field(default_factory=list)
    popular_series: Dict[str, List[DonghuaHomePopularSeriesItem]] = Field(default_factory=dict)
    new_movie: List[DonghuaHomeNewMovie] = Field(default_factory=list)
    genre: List[DonghuaHomeGenre] = Field(default_factory=list)
    season: List[DonghuaHomeSeason] = Field(default_factory=list)
    
class DonghuaSearchItem(BaseModel):
    title: str
    slug: str
    thumbnail: str
    episode: Optional[str] = ""
    type: str
    badge: str
    url: str
    
class DonghuaSearchPagination(BaseModel):
    previous: str = ""
    current_page: str = "1"
    next: str = ""
    
class DonghuaSearchResponse(BaseModel):
    items: List[DonghuaSearchItem] = Field(default_factory=list)
    pagination: DonghuaSearchPagination = Field(default_factory=DonghuaSearchPagination)
    
class DonghuaScheduleDay(BaseModel):
    title: str
    slug: str
    thumbnail: str
    countdown: Dict[str, str] = Field(default_factory=dict)
    release_time: Dict[str, str] = Field(default_factory=dict)
    current_episode: str = ""
    url: str
    
class DonghuaScheduleResponse(BaseModel):
    monday: Dict[str, List[DonghuaScheduleDay]] = Field(default_factory=dict)
    tuesday: Dict[str, List[DonghuaScheduleDay]] = Field(default_factory=dict)
    wednesday: Dict[str, List[DonghuaScheduleDay]] = Field(default_factory=dict)
    thursday: Dict[str, List[DonghuaScheduleDay]] = Field(default_factory=dict)
    friday: Dict[str, List[DonghuaScheduleDay]] = Field(default_factory=dict)
    saturday: Dict[str, List[DonghuaScheduleDay]] = Field(default_factory=dict)
    sunday: Dict[str, List[DonghuaScheduleDay]] = Field(default_factory=dict)
    
class DonghuaListResponse(BaseModel):
    items: List[DonghuaSearchItem] = Field(default_factory=list)
    pagination: Dict[str, str] = Field(default_factory=dict)
    genre_title: str = ""
    
class DonghuaComletedResponse(BaseModel):
    items: List[DonghuaSearchItem] = Field(default_factory=list)
    pagination: Dict[str, str] = Field(default_factory=dict)
    
class DonghuaOngoingResponse(BaseModel):
    items: List[DonghuaSearchItem] = Field(default_factory=list)
    pagination: Dict[str, str] = Field(default_factory=dict)
    
class DonghuaCover(BaseModel):
    banner: str = ""
    thumbnail: str = ""
    
class DonghuaInformation(BaseModel):
    status: str = ""
    network: str = ""
    studio: str = ""
    released: str = ""
    duration: str = ""
    season: str = ""
    country: str = ""
    type: str = ""
    episode: str = ""
    released_on: str = ""
    updated_on: str = ""
    
class DonghuaGenre(BaseModel):
    title_genre: str
    slug: str
    url: str
    
class DonghuaEpisodeNav(BaseModel):
    first_episode: Dict[str, str] = Field(default_factory=dict)
    new_episode: Dict[str, str] = Field(default_factory=dict)
    
class DonghuaEpisodeItem(BaseModel):
    number: str
    title: str
    badge: Optional[str] = ""
    release_date: str = ""
    url: str
    
class DonghuaDetailResponse(BaseModel):
    cover: DonghuaCover = Field(default_factory=DonghuaCover)
    slug: str
    title: str
    alter_title: str = ""
    bookmark_count: str = ""
    synopsis: str = ""
    information: DonghuaInformation = Field(default_factory=DonghuaInformation)
    genre: List[DonghuaGenre] = Field(default_factory=list)
    download_batch: Dict[str, Any] = Field(default_factory=dict)
    episode_nav: DonghuaEpisodeNav = Field(default_factory=DonghuaEpisodeNav)
    episode: Dict[str, List[DonghuaEpisodeItem]] = Field(default_factory=dict)
    url: str
    
class DonghuaWatchServer(BaseModel):
    server_id: str
    server_name: str
    server_url: str
    
class DonghuaWatchDownload(BaseModel):
    quality: str
    links: List[Dict[str, str]]
    
class DonghuaWatchInformation(BaseModel):
    status: str = ""
    released: str = ""
    season: str = ""
    type: str = ""
    network: str = ""
    duration: str = ""
    country: str = ""
    total_episode: str = ""
    studio: str = ""
    
class DonghuaWatchRelated(BaseModel):
    title: str
    slug: str
    thumbnail: str
    url: str
    
class DonghuaWatchEpisode(BaseModel):
    title: str
    slug: str
    thumbnail: str
    episode: str = ""
    released_on: str = ""
    url: str
    
class DonghuaWatchPagination(BaseModel):
    prev_episode: str = ""
    all_episode: str = ""
    next_episode: str = ""
    
class DonghuaWatchResponse(BaseModel):
    title: str
    slug: str
    episode: str = ""
    thumbnail: str = ""
    released_on: str = ""
    server: List[DonghuaWatchServer] = Field(default_factory=list)
    download: Dict[str, Any] = Field(default_factory=dict)
    synopsis: str = ""
    genre: List[DonghuaGenre] = Field(default_factory=list)
    information: DonghuaWatchInformation = Field(default_factory=DonghuaWatchInformation)
    related_episode: List[DonghuaWatchRelated] = Field(default_factory=list)
    episode_list: List[DonghuaWatchEpisode] = Field(default_factory=list)
    pagination: DonghuaWatchPagination = Field(default_factory=DonghuaWatchPagination)
    url: str
    
class DonghuaFilterOption(BaseModel):
    value: str
    label: str
    count: str
    
class DonghuaFiltersResponse(BaseModel):
    status: List[DonghuaFilterOption] = Field(default_factory=list)
    type: List[DonghuaFilterOption] = Field(default_factory=list)
    sub: List[DonghuaFilterOption] = Field(default_factory=list)
    order: List[DonghuaFilterOption] = Field(default_factory=list)
    studio: List[DonghuaFilterOption] = Field(default_factory=list)
    season: List[DonghuaFilterOption] = Field(default_factory=list)
    genre: List[DonghuaFilterOption] = Field(default_factory=list)
    
class DonghuaRandomResponse(BaseModel):
    random_selection: Dict[str, Any] = Field(default_factory=dict)
    cover: DonghuaCover = Field(default_factory=DonghuaCover)
    slug: str
    title: str
    alter_title: str = ""
    bookmark_count: str = ""
    synopsis: str = ""
    information: DonghuaInformation = Field(default_factory=DonghuaInformation)
    genre: List[DonghuaGenre] = Field(default_factory=list)
    download_batch: Dict[str, Any] = Field(default_factory=dict)
    episode_nav: DonghuaEpisodeNav = Field(default_factory=DonghuaEpisodeNav)
    episode: Dict[str, List[DonghuaEpisodeItem]] = Field(default_factory=dict)
    url: str