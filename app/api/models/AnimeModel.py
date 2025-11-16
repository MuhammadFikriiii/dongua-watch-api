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

class AnimeHomePopular(BaseModel):
    title: str
    slug: str
    thumbnail: str
    episode: str
    type: str
    badge: str
    url: str
    
class AnimeHomeLatest(BaseModel):
    title: str
    slug: str
    thumbnail: str
    episode: str
    type: str
    badge: str
    url: str
    
class AnimeHomeRecommendationTab(BaseModel):
    id: str
    name: str
    active: bool
    
class AnimeHomeRecommendationItem(BaseModel):
    status: str
    type: str
    title: str
    slug: str
    thumbnail: str
    episode: str
    badge: str
    url: str
    
class AnimeHomeResponse(BaseModel):
    popular_today: List[AnimeHomePopular] = Field(default_factory=list)
    latest_release: List[AnimeHomeLatest] = Field(default_factory=list)
    recommendation: Dict[str, Any] = Field(default_factory=dict)
    
class AnimeSearchItem(BaseModel):
    title: str
    slug: str
    thumbnail: str
    episode: Optional[str] = ""
    type: str
    badge: str
    url: str
    
class AnimeSearchPagination(BaseModel):
    previous: str = ""
    current_page: str = "1"
    next: str = ""
    
class AnimeSearchResponse(BaseModel):
    items: List[AnimeSearchItem] = Field(default_factory=list)
    pagination: AnimeSearchPagination = Field(default_factory=AnimeSearchPagination)
    query: str = ""
    
class AnimeScheduleDay(BaseModel):
    title: str
    slug: str
    thumbnail: str
    countdown: Dict[str, str] = Field(default_factory=dict)
    release_time: Dict[str, str] = Field(default_factory=dict)
    current_episode: str = ""
    url: str
    
class AnimeScheduleResponse(BaseModel):
    monday: Dict[str, List[AnimeScheduleDay]] = Field(default_factory=dict)
    tuesday: Dict[str, List[AnimeScheduleDay]] = Field(default_factory=dict)
    wednesday: Dict[str, List[AnimeScheduleDay]] = Field(default_factory=dict)
    thursday: Dict[str, List[AnimeScheduleDay]] = Field(default_factory=dict)
    friday: Dict[str, List[AnimeScheduleDay]] = Field(default_factory=dict)
    saturday: Dict[str, List[AnimeScheduleDay]] = Field(default_factory=dict)
    sunday: Dict[str, List[AnimeScheduleDay]] = Field(default_factory=dict)
    
class AnimeListResponse(BaseModel):
    items: List[AnimeSearchItem] = Field(default_factory=list)
    pagination: Dict[str, str] = Field(default_factory=dict)
    
class AnimeCover(BaseModel):
    banner: str = ""
    thumbnail: str = ""
    
class AnimeInformation(BaseModel):
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
    
class AnimeGenre(BaseModel):
    title_genre: str
    slug: str
    url: str
    
class AnimeEpisodeNav(BaseModel):
    first_episode: Dict[str, str] = Field(default_factory=dict)
    new_episode: Dict[str, str] = Field(default_factory=dict)
    
class AnimeEpisodeItem(BaseModel):
    number: str
    title: str
    badge: Optional[str] = ""
    release_date: str = ""
    url: str
    
class AnimeDetailResponse(BaseModel):
    cover: AnimeCover = Field(default_factory=AnimeCover)
    slug: str
    title: str
    alter_title: str = ""
    bookmark_count: str = ""
    synopsis: str = ""
    information: AnimeInformation = Field(default_factory=AnimeInformation)
    genre: List[AnimeGenre] = Field(default_factory=list)
    download_batch: Dict[str, Any] = Field(default_factory=dict)
    episode_nav: AnimeEpisodeNav = Field(default_factory=AnimeEpisodeNav)
    episode: Dict[str, List[AnimeEpisodeItem]] = Field(default_factory=dict)
    url: str
    
class AnimeWatchServer(BaseModel):
    server_id: str
    server_name: str
    server_url: str
    
class AnimeWatchDownload(BaseModel):
    quality: str
    links: List[Dict[str, str]]
    
class AnimeWatchInformation(BaseModel):
    status: str = ""
    released: str = ""
    season: str = ""
    type: str = ""
    network: str = ""
    duration: str = ""
    country: str = ""
    total_episode: str = ""
    studio: str = ""
    
class AnimeWatchRelated(BaseModel):
    title: str
    slug: str
    thumbnail: str
    url: str
    
class AnimeWatchEpisode(BaseModel):
    title: str
    slug: str
    thumbnail: str
    episode: str = ""
    released_on: str = ""
    url: str
    
class AnimeWatchPagination(BaseModel):
    prev_episode: str = ""
    all_episode: str = ""
    next_episode: str = ""
    
class AnimeWatchResponse(BaseModel):
    title: str
    slug: str
    episode: str = ""
    thumbnail: str = ""
    released_on: str = ""
    server: List[AnimeWatchServer] = Field(default_factory=list)
    download: Dict[str, Any] = Field(default_factory=dict)
    synopsis: str = ""
    genre: List[AnimeGenre] = Field(default_factory=list)
    information: AnimeWatchInformation = Field(default_factory=AnimeWatchInformation)
    related_episode: List[AnimeWatchRelated] = Field(default_factory=list)
    episode_list: List[AnimeWatchEpisode] = Field(default_factory=list)
    pagination: AnimeWatchPagination = Field(default_factory=AnimeWatchPagination)
    url: str
    
class AnimeFilterOption(BaseModel):
    value: str
    label: str
    count: str
    
class AnimeFiltersResponse(BaseModel):
    status: List[AnimeFilterOption] = Field(default_factory=list)
    type: List[AnimeFilterOption] = Field(default_factory=list)
    sub: List[AnimeFilterOption] = Field(default_factory=list)
    order: List[AnimeFilterOption] = Field(default_factory=list)
    studio: List[AnimeFilterOption] = Field(default_factory=list)
    season: List[AnimeFilterOption] = Field(default_factory=list)
    genre: List[AnimeFilterOption] = Field(default_factory=list)
    
class AnimeRandomResponse(BaseModel):
    random_selection: Dict[str, Any] = Field(default_factory=dict)
    cover: AnimeCover = Field(default_factory=AnimeCover)
    slug: str
    title: str
    alter_title: str = ""
    bookmark_count: str = ""
    synopsis: str = ""
    information: AnimeInformation = Field(default_factory=AnimeInformation)
    genre: List[AnimeGenre] = Field(default_factory=list)
    download_batch: Dict[str, Any] = Field(default_factory=dict)
    episode_nav: AnimeEpisodeNav = Field(default_factory=AnimeEpisodeNav)
    episode: Dict[str, List[AnimeEpisodeItem]] = Field(default_factory=dict)
    url: str