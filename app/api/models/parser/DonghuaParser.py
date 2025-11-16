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

import requests
import re
import random
import time
from bs4 import BeautifulSoup
from typing import Dict, List, Optional, Any
from urllib.parse import urljoin, urlparse
from datetime import datetime, timedelta

class DonghuaParser:
    def __init__(self):
        self.base_url = "https://anichin.cafe"
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Referer": self.base_url,
            "Origin": self.base_url
        })
        self.last_request_time = 0
        self.request_delay = 1
        
    def extract_slug(self, url: str) -> str:
        if not url:
            return ""
        parsed_url = urlparse(url)
        path = parsed_url.path.strip('/')
        if path.startswith('seri/'):
            return path.replace('seri/', '')
        elif path.startswith('genres/'):
            return path.replace('genres/', '')
        elif path.startswith('season/'):
            return path.replace('season/', '')
        elif '-episode-' in path:
            return re.sub(r'-episode-\d+-subtitle-indonesia.*', '', path)
        else:
            return path
            
    def get_page(self, url: str) -> Optional[BeautifulSoup]:
        elapsed = time.time() - self.last_request_time
        if elapsed < self.request_delay:
            time.sleep(self.request_delay - elapsed)
            
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            self.last_request_time = time.time()
            return BeautifulSoup(response.content, 'html.parser')
        except requests.exceptions.RequestException as e:
            print(f"Network error fetching {url}: {e}")
        except Exception as e:
            print(f"Unexpected error fetching page: {e}")
        return None
            
    def format_countdown(self, seconds_str: str) -> str:
        if not seconds_str or not seconds_str.lstrip('-').isdigit():
            return "Unknown"
            
        seconds = int(seconds_str)
        
        if seconds < 0:
            return "Already released"
            
        days = seconds // (24 * 3600)
        seconds %= (24 * 3600)
        hours = seconds // 3600
        seconds %= 3600
        minutes = seconds // 60
        
        if days > 0:
            return f"{days}d {hours}h {minutes}m"
        elif hours > 0:
            return f"{hours}h {minutes}m"
        else:
            return f"{minutes}m"
            
    def format_release_time(self, timestamp_str: str) -> str:
        if not timestamp_str:
            return "Unknown"
            
        if timestamp_str.isdigit():
            try:
                timestamp = int(timestamp_str)
                if timestamp > 253402300800:
                    timestamp = timestamp // 1000
                dt = datetime.fromtimestamp(timestamp)
                return dt.strftime("At %H:%M")
            except (ValueError, OSError):
                pass
              
        return timestamp_str if timestamp_str else "Unknown"
        
    def format_season_title(self, url: str) -> str:
        if not url or "/season/" not in url:
            return "Unknown Season"
            
        try:
            season_part = url.split("/season/")[-1].split("/")[0].strip()
            if not season_part:
                return "Unknown Season"
                
            if season_part.replace("-", "").isdigit():
                return f"Season {season_part}"
                
            if "-" in season_part:
                parts = season_part.split("-")
                if len(parts) == 2 and parts[1].isdigit():
                    season_name = parts[0].title()
                    year = parts[1]
                    return f"{season_name} {year}"
                    
            formatted = season_part.replace("-", " ").title()
            return f"Season {formatted}"
            
        except Exception:
            return "Unknown Season"
            
    def get_random(self) -> Dict[str, Any]:
        try:
            list_mode_url = f"{self.base_url}/seri/list-mode/"
            soup = self.get_page(list_mode_url)
            
            if not soup:
                return {"error": "Failed to fetch series list", "data": None}
                
            all_series = []
            
            blix_containers = soup.select(".blix")
            for container in blix_containers:
                for item in container.select("li a.series"):
                    title = item.get_text(strip=True)
                    url = item.get("href", "")
                    slug = self.extract_slug(url)
                    
                    if title and slug:
                        all_series.append({
                            "title": title,
                            "slug": slug,
                            "url": url
                        })
                        
            if not all_series:
                return {"error": "No series found", "data": None}
                
            random_series = random.choice(all_series)
            selected_slug = random_series["slug"]
            selected_title = random_series["title"]
            
            detail_data = self.parse_detail(selected_slug)
            
            if detail_data:
                detail_data["random_selection"] = {
                    "total_available": len(all_series),
                    "selected_from": selected_title
                }
                return detail_data
            else:
                return {"error": "Failed to parse detail", "data": None}
            
        except Exception as e:
            print(f"Error getting random donghua: {e}")
            return {"error": f"Failed to get random donghua: {str(e)}", "data": None}
            
    def parse_home(self, page: str = "1") -> Dict[str, Any]:
        url = f"{self.base_url}/page/{page}/" if page != "1" else self.base_url + "/"
        soup = self.get_page(url)
        if not soup:
            return {"error": "Failed to fetch home page", "data": None}
            
        results = {
            "slider": [],
            "popular_today": [],
            "latest_release": [],
            "recommendation": {"tabs": [], "data": {}},
            "ongoing_series": [],
            "popular_series": {"weekly": [], "monthly": [], "all_time": []},
            "new_movie": [],
            "genre": [],
            "season": []
        }
        
        try:
            slider_container = soup.select_one("#slidertwo")
            if slider_container:
                for item in slider_container.select(".swiper-slide.item"):
                    title_elem = item.select_one("h2 a")
                    title = title_elem.get("data-jtitle", "").strip() if title_elem else ""
                    watch_elem = item.select_one(".watch")
                    slug = self.extract_slug(watch_elem.get("href", "")) if watch_elem else ""
                    thumbnail_style = item.select_one(".backdrop").get("style", "") if item.select_one(".backdrop") else ""
                    thumbnail = re.search(r"url\(['\"]?(.*?)['\"]?\)", thumbnail_style).group(1) if thumbnail_style else ""
                    description = item.select_one(".info p").get_text(strip=True) if item.select_one(".info p") else ""
                    url = watch_elem.get("href", "") if watch_elem else ""
                    
                    if title:
                        results["slider"].append({
                            "title": title,
                            "slug": slug,
                            "thumbnail": thumbnail,
                            "description": description,
                            "url": urljoin(self.base_url, url) if url else ""
                        })
                        
            popular_container = soup.select_one(".listupd.normal")
            if popular_container:
                for item in popular_container.select(".bs .bsx"):
                    title_elem = item.select_one(".tt h2")
                    title = title_elem.get_text(strip=True) if title_elem else ""
                    link_elem = item.select_one("a")
                    slug = self.extract_slug(link_elem.get("href", "")) if link_elem else ""
                    thumbnail_elem = item.select_one("img")
                    thumbnail = thumbnail_elem.get("src", "") if thumbnail_elem else ""
                    episode = item.select_one(".epx").get_text(strip=True) if item.select_one(".epx") else ""
                    type_elem = item.select_one(".typez")
                    media_type = type_elem.get_text(strip=True) if type_elem else ""
                    badge = item.select_one(".sb.Sub").get_text(strip=True) if item.select_one(".sb.Sub") else ""
                    url = link_elem.get("href", "") if link_elem else ""
                    
                    if title:
                        results["popular_today"].append({
                            "title": title,
                            "slug": slug,
                            "thumbnail": urljoin(self.base_url, thumbnail) if thumbnail else "",
                            "episode": episode,
                            "type": media_type,
                            "badge": badge,
                            "url": urljoin(self.base_url, url) if url else ""
                        })
                        
            latest_container = soup.select_one(".releases.latesthome")
            if latest_container:
                view_all_elem = latest_container.select_one(".vl")
                view_all = view_all_elem.get("href", "") if view_all_elem else ""
                items_container = soup.select_one(".listupd.normal")
                if items_container:
                    for item in items_container.select(".bs .bsx"):
                        title_elem = item.select_one(".tt h2")
                        title = title_elem.get_text(strip=True) if title_elem else ""
                        link_elem = item.select_one("a")
                        slug = self.extract_slug(link_elem.get("href", "")) if link_elem else ""
                        thumbnail_elem = item.select_one("img")
                        thumbnail = thumbnail_elem.get("src", "") if thumbnail_elem else ""
                        episode = item.select_one(".epx").get_text(strip=True) if item.select_one(".epx") else ""
                        type_elem = item.select_one(".typez")
                        media_type = type_elem.get_text(strip=True) if type_elem else ""
                        badge = item.select_one(".sb.Sub").get_text(strip=True) if item.select_one(".sb.Sub") else ""
                        url = link_elem.get("href", "") if link_elem else ""
                        
                        if title:
                            results["latest_release"].append({
                                "title": title,
                                "slug": slug,
                                "thumbnail": urljoin(self.base_url, thumbnail) if thumbnail else "",
                                "episode": episode,
                                "type": media_type,
                                "badge": badge,
                                "url": urljoin(self.base_url, url) if url else ""
                            })
                            
                pagination_container = soup.select_one(".hpage")
                if pagination_container:
                    prev_elem = pagination_container.select_one("a.l")
                    next_elem = pagination_container.select_one("a.r")
                    
                    results["latest_release_pagination"] = {
                        "view_all": urljoin(self.base_url, view_all) if view_all else "",
                        "prev": urljoin(self.base_url, prev_elem.get("href", "")) if prev_elem else "",
                        "next": urljoin(self.base_url, next_elem.get("href", "")) if next_elem else ""
                    }
                    
            recommendation_container = soup.select_one(".series-gen")
            if recommendation_container:
                tabs_container = recommendation_container.select_one("ul.nav-tabs")
                if tabs_container:
                    for tab in tabs_container.select("li"):
                        tab_link = tab.select_one("a")
                        if tab_link:
                            tab_id = tab_link.get("href", "").replace("#", "")
                            tab_name = tab_link.get_text(strip=True)
                            is_active = "active" in tab.get("class", [])
                            results["recommendation"]["tabs"].append({
                                "id": tab_id,
                                "name": tab_name,
                                "active": is_active
                            })
                            
                tabs_content = recommendation_container.select(".tab-pane")
                for tab_content in tabs_content:
                    tab_id = tab_content.get("id", "")
                    items = []
                    for item in tab_content.select(".bs .bsx"):
                        status_elem = item.select_one(".status")
                        status = status_elem.get_text(strip=True) if status_elem else ""
                        type_elem = item.select_one(".typez")
                        media_type = type_elem.get_text(strip=True) if type_elem else ""
                        
                        title_elem = item.select_one(".tt h2")
                        title = title_elem.get_text(strip=True) if title_elem else ""
                        link_elem = item.select_one("a")
                        slug = self.extract_slug(link_elem.get("href", "")) if link_elem else ""
                        thumbnail_elem = item.select_one("img")
                        thumbnail = thumbnail_elem.get("src", "") if thumbnail_elem else ""
                        episode = item.select_one(".epx").get_text(strip=True) if item.select_one(".epx") else ""
                        badge = item.select_one(".sb.Sub").get_text(strip=True) if item.select_one(".sb.Sub") else ""
                        url = link_elem.get("href", "") if link_elem else ""
                        
                        if title:
                            items.append({
                                "status": status,
                                "type": media_type,
                                "title": title,
                                "slug": slug,
                                "thumbnail": urljoin(self.base_url, thumbnail) if thumbnail else "",
                                "episode": episode,
                                "badge": badge,
                                "url": urljoin(self.base_url, url) if url else ""
                            })
                            
                    if tab_id and items:
                        results["recommendation"]["data"][tab_id] = items
                        
            ongoing_container = soup.select_one(".ongoingseries")
            if ongoing_container:
                for item in ongoing_container.select("li"):
                    title_elem = item.select_one(".l")
                    title = title_elem.get_text(strip=True) if title_elem else ""
                    link_elem = item.select_one("a")
                    slug = self.extract_slug(link_elem.get("href", "")) if link_elem else ""
                    episode = item.select_one(".r").get_text(strip=True) if item.select_one(".r") else ""
                    url = link_elem.get("href", "") if link_elem else ""
                    
                    if title:
                        results["ongoing_series"].append({
                            "title": title,
                            "slug": slug,
                            "episode": episode,
                            "url": urljoin(self.base_url, url) if url else ""
                        })
                        
            popular_series_container = soup.select_one("#wpop-items")
            if popular_series_container:
                ranges = ["weekly", "monthly", "alltime"]
                for range_type in ranges:
                    range_items = popular_series_container.select(f".wpop-{range_type} li")
                    for item in range_items:
                        top = item.select_one(".ctr").get_text(strip=True) if item.select_one(".ctr") else ""
                        title_elem = item.select_one("h4 a")
                        title = title_elem.get_text(strip=True) if title_elem else ""
                        slug = self.extract_slug(title_elem.get("href", "")) if title_elem else ""
                        thumbnail_elem = item.select_one("img")
                        thumbnail = thumbnail_elem.get("src", "") if thumbnail_elem else ""
                        genres = [genre.get_text(strip=True) for genre in item.select(".leftseries span a")]
                        rating = item.select_one(".numscore").get_text(strip=True) if item.select_one(".numscore") else ""
                        url = title_elem.get("href", "") if title_elem else ""
                        
                        if title:
                            range_key = "weekly" if range_type == "weekly" else "monthly" if range_type == "monthly" else "all_time"
                            results["popular_series"][range_key].append({
                                "top": top,
                                "title": title,
                                "slug": slug,
                                "thumbnail": urljoin(self.base_url, thumbnail) if thumbnail else "",
                                "genre": genres,
                                "rating": rating,
                                "url": urljoin(self.base_url, url) if url else ""
                            })
                            
            sections = soup.find_all("div", class_="section")
            for section in sections:
                new_movie_header = section.select_one(".releases h3 span")
                if new_movie_header and "NEW MOVIE" in new_movie_header.get_text():
                    view_all_elem = section.select_one(".vl")
                    view_all = view_all_elem.get("href", "") if view_all_elem else ""
                    series_list = section.select_one(".serieslist")
                    if series_list:
                        for item in series_list.select("li"):
                            title_elem = item.select_one("h4 a")
                            title = title_elem.get_text(strip=True) if title_elem else ""
                            slug = self.extract_slug(title_elem.get("href", "")) if title_elem else ""
                            thumbnail_elem = item.select_one("img")
                            thumbnail = thumbnail_elem.get("src", "") if thumbnail_elem else ""
                            genres = []
                            genre_links = item.select(".leftseries a[href*='genres']")
                            for genre_link in genre_links:
                                genre_name = genre_link.get_text(strip=True)
                                if genre_name and genre_name not in ["Genres", "View all series in"]:
                                    genres.append(genre_name)
                            release_date = ""
                            spans = item.select(".leftseries span")
                            for span in spans:
                                text = span.get_text(strip=True)
                                if re.match(r'[A-Za-z]+ \d{1,2}, \d{4}', text) or re.match(r'\d{4}', text):
                                    release_date = text
                                    break
                            url = title_elem.get("href", "") if title_elem else ""
                            
                            if title:
                                results["new_movie"].append({
                                    "title": title,
                                    "slug": slug,
                                    "thumbnail": urljoin(self.base_url, thumbnail) if thumbnail else "",
                                    "genres": genres,
                                    "release_date": release_date,
                                    "url": urljoin(self.base_url, url) if url else ""
                                })
                                
                    results["new_movie_pagination"] = {
                        "view_all": urljoin(self.base_url, view_all) if view_all else ""
                    }
                    break
                  
            for section in sections:
                genre_header = section.select_one(".releases h3")
                if genre_header and "Genres" in genre_header.get_text():
                    genre_container = section.select_one("ul.genre")
                    if genre_container:
                        for item in genre_container.select("li"):
                            link_elem = item.select_one("a")
                            title = link_elem.get_text(strip=True) if link_elem else ""
                            slug = self.extract_slug(link_elem.get("href", "")) if link_elem else ""
                            url = link_elem.get("href", "") if link_elem else ""
                            
                            if title:
                                results["genre"].append({
                                    "title": title,
                                    "slug": slug,
                                    "url": urljoin(self.base_url, url) if url else ""
                                })
                    break
                  
            for section in sections:
                season_header = section.select_one(".releases h3")
                if season_header and "Season" in season_header.get_text():
                    season_container = section.select_one("ul.season")
                    if season_container:
                        for item in season_container.select("li"):
                            link_elem = item.select_one("a")
                            if link_elem:
                                url = link_elem.get("href", "")
                                title = self.format_season_title(url)
                                slug = self.extract_slug(url)
                                count_elem = item.select_one("span")
                                count = count_elem.get_text(strip=True) if count_elem else ""
                                
                                if title != "Unknown Season":
                                    results["season"].append({
                                        "title": title,
                                        "slug": slug,
                                        "count": count,
                                        "url": urljoin(self.base_url, url) if url else ""
                                    })
                    break
                  
        except Exception as e:
            print(f"Error parsing home: {e}")
            return {"error": f"Failed to parse home: {str(e)}", "data": None}
            
        return results
        
    def parse_search(self, query: str, page: str = "1") -> Dict[str, Any]:
        if page == "1":
            url = f"{self.base_url}/?s={query}"
        else:
            url = f"{self.base_url}/page/{page}/?s={query}"
            
        soup = self.get_page(url)
        if not soup:
            return {"error": "Failed to fetch search results", "data": None}
            
        results = {
            "items": [],
            "pagination": {}
        }
        
        try:
            container = soup.select_one(".listupd")
            if container:
                for item in container.select(".bs .bsx"):
                    title_elem = item.select_one(".tt h2")
                    title = title_elem.get_text(strip=True) if title_elem else ""
                    link_elem = item.select_one("a")
                    slug = self.extract_slug(link_elem.get("href", "")) if link_elem else ""
                    thumbnail_elem = item.select_one("img")
                    thumbnail = thumbnail_elem.get("src", "") if thumbnail_elem else ""
                    type_elem = item.select_one(".typez")
                    media_type = type_elem.get_text(strip=True) if type_elem else ""
                    episode = item.select_one(".epx").get_text(strip=True) if item.select_one(".epx") else ""
                    badge = item.select_one(".sb.Sub").get_text(strip=True) if item.select_one(".sb.Sub") else ""
                    url = link_elem.get("href", "") if link_elem else ""
                    
                    if title:
                        results["items"].append({
                            "title": title,
                            "slug": slug,
                            "thumbnail": urljoin(self.base_url, thumbnail) if thumbnail else "",
                            "episode": episode,
                            "type": media_type,
                            "badge": badge,
                            "url": urljoin(self.base_url, url) if url else ""
                        })
                        
            pagination_container = soup.select_one(".pagination")
            if pagination_container:
                prev_elem = pagination_container.select_one(".prev.page-numbers")
                next_elem = pagination_container.select_one(".next.page-numbers")
                current_elem = pagination_container.select_one(".page-numbers.current")
                
                results["pagination"] = {
                    "previous": urljoin(self.base_url, prev_elem.get("href", "")) if prev_elem else "",
                    "current_page": current_elem.get_text(strip=True) if current_elem else "1",
                    "next": urljoin(self.base_url, next_elem.get("href", "")) if next_elem else ""
                }
                
        except Exception as e:
            print(f"Error parsing search: {e}")
            return {"error": f"Failed to parse search: {str(e)}", "data": None}
            
        return results

    def parse_schedule(self) -> Dict[str, Any]:
        url = f"{self.base_url}/schedule/"
        soup = self.get_page(url)
        if not soup:
            return {"error": "Failed to fetch schedule", "data": None}
            
        results = {
            "monday": {"list": []},
            "tuesday": {"list": []},
            "wednesday": {"list": []},
            "thursday": {"list": []},
            "friday": {"list": []},
            "saturday": {"list": []},
            "sunday": {"list": []}
        }
        
        try:
            schedule_sections = soup.select('[class*="sch_"]')
            for section in schedule_sections:
                class_names = section.get('class', [])
                day = None
                for class_name in class_names:
                    if class_name.startswith('sch_'):
                        day = class_name.replace('sch_', '')
                        break
                    
                if day and day in results:
                    items = section.select('.bsx')
                    for item in items:
                        title_elem = item.select_one('.tt')
                        title = title_elem.get_text(strip=True) if title_elem else ""
                        if title:
                            link_elem = item.select_one('a')
                            slug = self.extract_slug(link_elem.get('href', '')) if link_elem else ""
                            thumbnail_elem = item.select_one('img')
                            thumbnail = thumbnail_elem.get('src', '') if thumbnail_elem else ""
                            countdown_elem = item.select_one(".epx.cndwn")
                            raw_countdown = countdown_elem.get("data-cndwn", "") if countdown_elem else ""
                            raw_release_time = countdown_elem.get("data-rlsdt", "") if countdown_elem else ""
                            formatted_countdown = self.format_countdown(raw_countdown)
                            formatted_release_time = self.format_release_time(raw_release_time)
                            episode_elem = item.select_one('.sb.Sub')
                            current_episode = episode_elem.get_text(strip=True) if episode_elem else ""
                            url = link_elem.get('href', '') if link_elem else ""
                            
                            results[day]["list"].append({
                                "title": title,
                                "slug": slug,
                                "thumbnail": urljoin(self.base_url, thumbnail) if thumbnail else "",
                                "countdown": {
                                    "raw": raw_countdown,
                                    "formatted": formatted_countdown
                                },
                                "release_time": {
                                    "raw": raw_release_time,
                                    "formatted": formatted_release_time
                                },
                                "current_episode": current_episode,
                                "url": urljoin(self.base_url, url) if url else ""
                            })
                          
        except Exception as e:
            print(f"Error parsing schedule: {e}")
            return {"error": f"Failed to parse schedule: {str(e)}", "data": None}
          
        return results
      
    def parse_ongoing(self, page: str = "1") -> Dict[str, Any]:
        if page == "1":
            url = f"{self.base_url}/ongoing/"
        else:
            url = f"{self.base_url}/ongoing/page/{page}/"
            
        soup = self.get_page(url)
        if not soup:
            return {"error": "Failed to fetch ongoing series", "data": None}
            
        results = {
            "items": [],
            "pagination": {}
        }
        
        try:
            container = soup.select_one(".bixbox .listupd")
            if container:
                for item in container.select(".bs .bsx"):
                    status = item.select_one(".epx").get_text(strip=True) if item.select_one(".epx") else ""
                    title_elem = item.select_one(".tt h2")
                    title = title_elem.get_text(strip=True) if title_elem else ""
                    link_elem = item.select_one("a")
                    slug = self.extract_slug(link_elem.get("href", "")) if link_elem else ""
                    thumbnail_elem = item.select_one("img")
                    thumbnail = thumbnail_elem.get("src", "") if thumbnail_elem else ""
                    type_elem = item.select_one(".typez")
                    media_type = type_elem.get_text(strip=True) if type_elem else ""
                    badge = item.select_one(".sb.Sub").get_text(strip=True) if item.select_one(".sb.Sub") else ""
                    url = link_elem.get("href", "") if link_elem else ""
                    
                    if title:
                        results["items"].append({
                            "status": status,
                            "title": title,
                            "slug": slug,
                            "thumbnail": urljoin(self.base_url, thumbnail) if thumbnail else "",
                            "type": media_type,
                            "badge": badge,
                            "url": urljoin(self.base_url, url) if url else ""
                        })
                        
            pagination_container = soup.select_one(".pagination")
            if pagination_container:
                prev_elem = pagination_container.select_one(".prev.page-numbers")
                next_elem = pagination_container.select_one(".next.page-numbers")
                current_elem = pagination_container.select_one(".page-numbers.current")
                
                results["pagination"] = {
                    "previous": urljoin(self.base_url, prev_elem.get("href", "")) if prev_elem else "",
                    "current_page": current_elem.get_text(strip=True) if current_elem else "",
                    "next": urljoin(self.base_url, next_elem.get("href", "")) if next_elem else ""
                }
                
        except Exception as e:
            print(f"Error parsing ongoing: {e}")
            return {"error": f"Failed to parse ongoing: {str(e)}", "data": None}
            
        return results
        
    def parse_completed(self, page: str = "1") -> Dict[str, Any]:
        if page == "1":
            url = f"{self.base_url}/completed"
        else:
            url = f"{self.base_url}/completed/page/{page}/"
            
        soup = self.get_page(url)
        if not soup:
            return {"error": "Failed to fetch completed series", "data": None}
            
        results = {
            "items": [],
            "pagination": {}
        }
        
        try:
            container = soup.select_one(".bixbox .listupd")
            if container:
                for item in container.select(".bs .bsx"):
                    status = item.select_one(".epx").get_text(strip=True) if item.select_one(".epx") else ""
                    title_elem = item.select_one(".tt h2")
                    title = title_elem.get_text(strip=True) if title_elem else ""
                    link_elem = item.select_one("a")
                    slug = self.extract_slug(link_elem.get("href", "")) if link_elem else ""
                    thumbnail_elem = item.select_one("img")
                    thumbnail = thumbnail_elem.get("src", "") if thumbnail_elem else ""
                    type_elem = item.select_one(".typez")
                    media_type = type_elem.get_text(strip=True) if type_elem else ""
                    badge = item.select_one(".sb.Sub").get_text(strip=True) if item.select_one(".sb.Sub") else ""
                    url = link_elem.get("href", "") if link_elem else ""
                    
                    if title:
                        results["items"].append({
                            "status": status,
                            "title": title,
                            "slug": slug,
                            "thumbnail": urljoin(self.base_url, thumbnail) if thumbnail else "",
                            "type": media_type,
                            "badge": badge,
                            "url": urljoin(self.base_url, url) if url else ""
                        })
                        
            pagination_container = soup.select_one(".pagination")
            if pagination_container:
                prev_elem = pagination_container.select_one(".prev.page-numbers")
                next_elem = pagination_container.select_one(".next.page-numbers")
                current_elem = pagination_container.select_one(".page-numbers.current")
                
                results["pagination"] = {
                    "previous": urljoin(self.base_url, prev_elem.get("href", "")) if prev_elem else "",
                    "current_page": current_elem.get_text(strip=True) if current_elem else "",
                    "next": urljoin(self.base_url, next_elem.get("href", "")) if next_elem else ""
                }
                
        except Exception as e:
            print(f"Error parsing completed: {e}")
            return {"error": f"Failed to parse completed: {str(e)}", "data": None}
            
        return results
        
    def parse_genres(self, slug: str, page: str = "1") -> Dict[str, Any]:
        if page == "1":
            url = f"{self.base_url}/genres/{slug}/"
        else:
            url = f"{self.base_url}/genres/{slug}/page/{page}/"
            
        soup = self.get_page(url)
        if not soup:
            return {"error": "Failed to fetch genre page", "data": None}
            
        results = {
            "items": [],
            "pagination": {},
            "genre_title": ""
        }
        
        try:
            genre_title_elem = soup.select_one(".releases h1 span")
            results["genre_title"] = genre_title_elem.get_text(strip=True) if genre_title_elem else ""
            
            container = soup.select_one(".listupd")
            if container:
                for item in container.select(".bs .bsx"):
                    title_elem = item.select_one(".tt h2")
                    title = title_elem.get_text(strip=True) if title_elem else ""
                    link_elem = item.select_one("a")
                    slug = self.extract_slug(link_elem.get("href", "")) if link_elem else ""
                    thumbnail_elem = item.select_one("img")
                    thumbnail = thumbnail_elem.get("src", "") if thumbnail_elem else ""
                    type_elem = item.select_one(".typez")
                    media_type = type_elem.get_text(strip=True) if type_elem else ""
                    episode = item.select_one(".epx").get_text(strip=True) if item.select_one(".epx") else ""
                    badge = item.select_one(".sb.Sub").get_text(strip=True) if item.select_one(".sb.Sub") else ""
                    url = link_elem.get("href", "") if link_elem else ""
                    
                    if title:
                        results["items"].append({
                            "title": title,
                            "slug": slug,
                            "thumbnail": urljoin(self.base_url, thumbnail) if thumbnail else "",
                            "type": media_type,
                            "episode": episode,
                            "badge": badge,
                            "url": urljoin(self.base_url, url) if url else ""
                        })
                        
            pagination_container = soup.select_one(".pagination")
            if pagination_container:
                prev_elem = pagination_container.select_one(".prev.page-numbers")
                next_elem = pagination_container.select_one(".next.page-numbers")
                current_elem = pagination_container.select_one(".page-numbers.current")
                
                results["pagination"] = {
                    "previous": urljoin(self.base_url, prev_elem.get("href", "")) if prev_elem else "",
                    "current_page": current_elem.get_text(strip=True) if current_elem else "",
                    "next": urljoin(self.base_url, next_elem.get("href", "")) if next_elem else ""
                }
                
        except Exception as e:
            print(f"Error parsing genres: {e}")
            return {"error": f"Failed to parse genres: {str(e)}", "data": None}
            
        return results
        
    def parse_az_list(self, show: str = "", page: str = "1") -> Dict[str, Any]:
        if show:
            if page == "1":
                url = f"{self.base_url}/az-lists/?show={show}"
            else:
                url = f"{self.base_url}/az-lists/page/{page}/?show={show}"
        else:
            if page == "1":
                url = f"{self.base_url}/az-lists"
            else:
                url = f"{self.base_url}/az-lists/page/{page}/"
                
        soup = self.get_page(url)
        if not soup:
            return {"error": "Failed to fetch AZ list", "data": None}
            
        results = {
            "items": [],
            "pagination": {}
        }
        
        try:
            container = soup.select_one(".listupd")
            if container:
                for item in container.select(".bs .bsx"):
                    status = item.select_one(".epx").get_text(strip=True) if item.select_one(".epx") else ""
                    title_elem = item.select_one(".tt h2")
                    title = title_elem.get_text(strip=True) if title_elem else ""
                    link_elem = item.select_one("a")
                    slug = self.extract_slug(link_elem.get("href", "")) if link_elem else ""
                    thumbnail_elem = item.select_one("img")
                    thumbnail = thumbnail_elem.get("src", "") if thumbnail_elem else ""
                    type_elem = item.select_one(".typez")
                    media_type = type_elem.get_text(strip=True) if type_elem else ""
                    badge = item.select_one(".sb.Sub").get_text(strip=True) if item.select_one(".sb.Sub") else ""
                    url = link_elem.get("href", "") if link_elem else ""
                    
                    if title:
                        results["items"].append({
                            "status": status,
                            "title": title,
                            "slug": slug,
                            "thumbnail": urljoin(self.base_url, thumbnail) if thumbnail else "",
                            "type": media_type,
                            "badge": badge,
                            "url": urljoin(self.base_url, url) if url else ""
                        })
                        
            pagination_container = soup.select_one(".pagination")
            if pagination_container:
                prev_elem = pagination_container.select_one(".prev.page-numbers")
                next_elem = pagination_container.select_one(".next.page-numbers")
                current_elem = pagination_container.select_one(".page-numbers.current")
                
                results["pagination"] = {
                    "previous": urljoin(self.base_url, prev_elem.get("href", "")) if prev_elem else "",
                    "current_page": current_elem.get_text(strip=True) if current_elem else "",
                    "next": urljoin(self.base_url, next_elem.get("href", "")) if next_elem else ""
                }
                
        except Exception as e:
            print(f"Error parsing AZ list: {e}")
            return {"error": f"Failed to parse AZ list: {str(e)}", "data": None}
            
        return results
        
    def parse_detail(self, slug: str) -> Dict[str, Any]:
        url = f"{self.base_url}/seri/{slug}/"
        soup = self.get_page(url)
        if not soup:
            return {"error": "Failed to fetch detail page", "data": None}
            
        results = {
            "cover": {"banner": "", "thumbnail": ""},
            "slug": slug,
            "title": "",
            "alter_title": "",
            "bookmark_count": "",
            "synopsis": "",
            "information": {},
            "genre": [],
            "download_batch": {},
            "episode_nav": {},
            "episode": {"list": []},
            "url": url
        }
        
        try:
            container = soup.select_one(".animefull")
            if not container:
                return {"error": "Detail container not found", "data": None}
                
            banner_elem = container.select_one(".bigcover img")
            if banner_elem:
                results["cover"]["banner"] = urljoin(self.base_url, banner_elem.get("src", ""))
            thumbnail_elem = container.select_one(".thumb img")
            if thumbnail_elem:
                results["cover"]["thumbnail"] = urljoin(self.base_url, thumbnail_elem.get("src", ""))
            title_elem = container.select_one(".entry-title")
            if title_elem:
                results["title"] = title_elem.get_text(strip=True)
            alter_title_elem = container.select_one(".alter")
            if alter_title_elem:
                results["alter_title"] = alter_title_elem.get_text(strip=True)
            bookmark_elem = container.select_one(".bmc")
            if bookmark_elem:
                results["bookmark_count"] = bookmark_elem.get_text(strip=True)
                
            synopsis_container = soup.select_one(".bixbox.synp")
            if synopsis_container:
                synopsis_elem = synopsis_container.select_one(".entry-content p")
                if synopsis_elem:
                    results["synopsis"] = synopsis_elem.get_text(strip=True)
                else:
                    synopsis_elem = synopsis_container.select_one(".entry-content")
                    if synopsis_elem:
                        results["synopsis"] = synopsis_elem.get_text(strip=True)
                        
            info_container = container.select_one(".spe")
            if info_container:
                info_items = {}
                
                def extract_info(keyword):
                    spans = info_container.find_all("span")
                    for span in spans:
                        text = span.get_text(strip=True)
                        if keyword.lower() in text.lower():
                            value = text.replace(f"{keyword}:", "").replace(f"{keyword}", "").strip()
                            if span.find("a"):
                                value = span.find("a").get_text(strip=True)
                            return value
                    return ""
                    
                info_items["status"] = extract_info("Status")
                info_items["network"] = extract_info("Network")
                info_items["studio"] = extract_info("Studio")
                info_items["released"] = extract_info("Released")
                info_items["duration"] = extract_info("Duration")
                info_items["season"] = extract_info("Season")
                info_items["country"] = extract_info("Country")
                info_items["type"] = extract_info("Type")
                info_items["episode"] = extract_info("Episodes")
                released_on_elem = info_container.find("span", string=lambda text: text and "Released on:" in text)
                if not released_on_elem:
                    released_on_elem = info_container.find("span", class_="split")
                if released_on_elem:
                    time_elem = released_on_elem.select_one("time")
                    info_items["released_on"] = time_elem.get_text(strip=True) if time_elem else released_on_elem.get_text(strip=True).replace("Released on:", "").strip()
                updated_on_elem = info_container.find("span", string=lambda text: text and "Updated on:" in text)
                if updated_on_elem:
                    time_elem = updated_on_elem.select_one("time")
                    info_items["updated_on"] = time_elem.get_text(strip=True) if time_elem else ""
                    
                results["information"] = info_items
                
            genre_container = container.select_one(".genxed")
            if genre_container:
                for item in genre_container.select("a"):
                    name = item.get_text(strip=True)
                    genre_slug = self.extract_slug(item.get("href", ""))
                    genre_url = item.get("href", "")
                    
                    results["genre"].append({
                        "title_genre": name,
                        "slug": genre_slug,
                        "url": urljoin(self.base_url, genre_url) if genre_url else ""
                    })
                    
            download_container = soup.select_one(".mctnx")
            if not download_container:
                download_container = soup.find("div", class_="bixbox", string=lambda text: text and "Download" in text)
                if download_container:
                    download_container = download_container.find_next_sibling("div", class_="mctnx")
                    
            if download_container:
                qualities = {}
                for section in download_container.select(".soraddlx"):
                    title_elem = section.select_one(".sorattlx h3")
                    if title_elem:
                        title = title_elem.get_text(strip=True)
                        quality_links = {}
                        for quality_section in section.select(".soraurlx"):
                            quality_elem = quality_section.select_one("strong")
                            if quality_elem:
                                quality = quality_elem.get_text(strip=True)
                                links = []
                                for link_elem in quality_section.select("a"):
                                    link_name = link_elem.get_text(strip=True)
                                    link_url = link_elem.get("href", "")
                                    links.append({
                                        "name": link_name,
                                        "link": urljoin(self.base_url, link_url) if link_url else ""
                                    })
                                quality_links[quality] = links
                        qualities[title] = quality_links
                results["download_batch"] = qualities
                
            episode_nav_container = soup.select_one(".inepcx")
            if not episode_nav_container:
                episode_nav_container = soup.select_one(".lastend")
            if episode_nav_container:
                first_episode_elem = episode_nav_container.select_one(".epcur.epcurfirst")
                first_episode_url_elem = episode_nav_container.select_one("a:first-child")
                new_episode_elem = episode_nav_container.select_one(".epcur.epcurlast")
                new_episode_url_elem = episode_nav_container.select_one("a:last-child")
                
                results["episode_nav"] = {
                    "first_episode": {
                        "number": first_episode_elem.get_text(strip=True) if first_episode_elem else "",
                        "url": urljoin(self.base_url, first_episode_url_elem.get("href", "")) if first_episode_url_elem else ""
                    },
                    "new_episode": {
                        "number": new_episode_elem.get_text(strip=True) if new_episode_elem else "",
                        "url": urljoin(self.base_url, new_episode_url_elem.get("href", "")) if new_episode_url_elem else ""
                    }
                }
                
            episode_list_container = soup.select_one(".eplister ul")
            if episode_list_container:
                for item in episode_list_container.select("li"):
                    number_elem = item.select_one(".epl-num")
                    number = number_elem.get_text(strip=True) if number_elem else ""
                    title_elem = item.select_one(".epl-title")
                    title = title_elem.get_text(strip=True) if title_elem else ""
                    subtitle_elem = item.select_one(".epl-sub .status")
                    badge = subtitle_elem.get_text(strip=True) if subtitle_elem else ""
                    date_elem = item.select_one(".epl-date")
                    release_date = date_elem.get_text(strip=True) if date_elem else ""
                    url_elem = item.select_one("a")
                    episode_url = url_elem.get("href", "") if url_elem else ""
                    
                    results["episode"]["list"].append({
                        "number": number,
                        "title": title,
                        "badge": badge,
                        "release_date": release_date,
                        "url": urljoin(self.base_url, episode_url) if episode_url else ""
                    })
                    
        except Exception as e:
            print(f"Error parsing detail: {e}")
            return {"error": f"Failed to parse detail: {str(e)}", "data": None}
            
        return results
        
    def parse_watch(self, slug: str, episode: str = "") -> Dict[str, Any]:
        if episode:
            url = f"{self.base_url}/{slug}-episode-{episode}-subtitle-indonesia/"
        else:
            url = f"{self.base_url}/seri/{slug}/"
            
        soup = self.get_page(url)
        if not soup:
            return {"error": "Failed to fetch watch page", "data": None}
            
        results = {
            "title": "",
            "slug": slug,
            "thumbnail": "",
            "released_on": "",
            "server": [],
            "download": {},
            "synopsis": "",
            "genre": [],
            "information": {},
            "related_episode": [],
            "episode_list": [],
            "pagination": {},
            "url": url
        }
        
        try:
            title_elem = soup.select_one(".entry-title")
            results["title"] = title_elem.get_text(strip=True) if title_elem else ""
            released_elem = soup.select_one(".updated")
            if not released_elem:
                released_elem = soup.select_one(".year .updated")
            results["released_on"] = released_elem.get_text(strip=True) if released_elem else ""
            thumbnail_elem = soup.select_one(".thumb img")
            if not thumbnail_elem:
                thumbnail_elem = soup.select_one(".tb img")
            results["thumbnail"] = urljoin(self.base_url, thumbnail_elem.get("src", "")) if thumbnail_elem else ""
            
            servers_container = soup.select_one("select.mirror")
            if servers_container:
                for option in servers_container.select("option[value!='']"):
                    server_id = option.get("data-index", "")
                    server_name = option.get_text(strip=True)
                    embed_data = option.get("value", "")
                    
                    results["server"].append({
                        "server_id": server_id,
                        "server_name": server_name,
                        "server_url": embed_data
                    })
                    
            download_container = soup.select_one(".soraddlx")
            if download_container:
                qualities = {}
                for quality_section in download_container.select(".soraurlx"):
                    quality_elem = quality_section.select_one("strong")
                    if quality_elem:
                        quality = quality_elem.get_text(strip=True)
                        links = []
                        for link_elem in quality_section.select("a"):
                            name = link_elem.get_text(strip=True)
                            download_link = link_elem.get("href", "")
                            links.append({
                                "name": name,
                                "link": urljoin(self.base_url, download_link) if download_link else ""
                            })
                        qualities[quality] = links
                results["download"] = qualities
                
            synopsis_elem = soup.select_one(".desc")
            if not synopsis_elem:
                synopsis_elem = soup.select_one(".desc.mindes")
            if not synopsis_elem:
                synopsis_elem = soup.select_one(".entry-content p")
            results["synopsis"] = synopsis_elem.get_text(strip=True) if synopsis_elem else ""
            
            genre_container = soup.select_one(".genxed")
            if genre_container:
                for item in genre_container.select("a"):
                    name = item.get_text(strip=True)
                    genre_slug = self.extract_slug(item.get("href", ""))
                    genre_url = item.get("href", "")
                    
                    results["genre"].append({
                        "title_genre": name,
                        "slug": genre_slug,
                        "url": urljoin(self.base_url, genre_url) if genre_url else ""
                    })
                    
            info_container = soup.select_one(".spe")
            if info_container:
                info_items = {}
                
                def extract_info(keyword):
                    spans = info_container.find_all("span")
                    for span in spans:
                        text = span.get_text(strip=True)
                        if keyword.lower() in text.lower():
                            value = text.replace(f"{keyword}:", "").replace(f"{keyword}", "").strip()
                            if span.find("a"):
                                value = span.find("a").get_text(strip=True)
                            return value
                    return ""
                    
                info_items["status"] = extract_info("Status")
                info_items["released"] = extract_info("Released")
                info_items["season"] = extract_info("Season")
                info_items["type"] = extract_info("Type")
                info_items["network"] = extract_info("Network")
                info_items["duration"] = extract_info("Duration")
                info_items["country"] = extract_info("Country")
                info_items["total_episode"] = extract_info("Episodes")
                info_items["studio"] = extract_info("Studio")
                
                results["information"] = info_items
                
            related_container = soup.select_one(".listupd")
            if related_container:
                for item in related_container.select(".bsx"):
                    title_elem = item.select_one("h2")
                    title = title_elem.get_text(strip=True) if title_elem else ""
                    link_elem = item.select_one("a")
                    related_slug = self.extract_slug(link_elem.get("href", "")) if link_elem else ""
                    thumbnail_elem = item.select_one("img")
                    thumbnail = thumbnail_elem.get("src", "") if thumbnail_elem else ""
                    url = link_elem.get("href", "") if link_elem else ""
                    
                    if title:
                        results["related_episode"].append({
                            "title": title,
                            "slug": related_slug,
                            "thumbnail": urljoin(self.base_url, thumbnail) if thumbnail else "",
                            "url": urljoin(self.base_url, url) if url else ""
                        })
                        
            episode_list_container = soup.select_one("#singlepisode .episodelist")
            if episode_list_container:
                for item in episode_list_container.select("li"):
                    title_elem = item.select_one(".playinfo h4")
                    title = title_elem.get_text(strip=True) if title_elem else ""
                    link_elem = item.select_one("a")
                    episode_slug = self.extract_slug(link_elem.get("href", "")) if link_elem else ""
                    thumbnail_elem = item.select_one(".thumbnel img")
                    thumbnail = thumbnail_elem.get("src", "") if thumbnail_elem else ""
                    playinfo_text = item.select_one(".playinfo span").get_text(strip=True) if item.select_one(".playinfo span") else ""
                    episode_match = re.search(r"Eps\s+(\d+)", playinfo_text)
                    episode_num = episode_match.group(1) if episode_match else ""
                    release_match = re.search(r"-\s+([^-]+)$", playinfo_text)
                    released_on = release_match.group(1).strip() if release_match else ""
                    url = link_elem.get("href", "") if link_elem else ""
                    
                    results["episode_list"].append({
                        "title": title,
                        "slug": episode_slug,
                        "thumbnail": urljoin(self.base_url, thumbnail) if thumbnail else "",
                        "episode": episode_num,
                        "released_on": released_on,
                        "url": urljoin(self.base_url, url) if url else ""
                    })
                    
            pagination_container = soup.select_one(".naveps")
            if pagination_container:
                prev_elem = pagination_container.select_one(".nvs a[rel='prev']")
                all_episode_elem = pagination_container.select_one(".nvsc a")
                next_elem = pagination_container.select_one(".nvs a[rel='next']")
                
                results["pagination"] = {
                    "prev_episode": urljoin(self.base_url, prev_elem.get("href", "")) if prev_elem else "",
                    "all_episode": urljoin(self.base_url, all_episode_elem.get("href", "")) if all_episode_elem else "",
                    "next_episode": urljoin(self.base_url, next_elem.get("href", "")) if next_elem else ""
                }
                
        except Exception as e:
            print(f"Error parsing watch: {e}")
            return {"error": f"Failed to parse watch: {str(e)}", "data": None}
            
        return results
        
    def parse_advanced_search_filters(self) -> Dict[str, Any]:
        url = f"{self.base_url}/seri/"
        soup = self.get_page(url)
        if not soup:
            return {"error": "Failed to fetch advanced search filters", "data": None}
            
        results = {
            "status": [],
            "type": [],
            "sub": [],
            "order": [],
            "studio": [],
            "season": [],
            "genre": []
        }
        
        try:
            advanced_search = soup.select_one(".quickfilter")
            if not advanced_search:
                return results
                
            genre_container = advanced_search.select_one(".filter.dropdown:has(button:contains('Genre'))")
            if genre_container:
                results["genre"] = []
                for input_elem in genre_container.select("input[name='genre[]']"):
                    label = input_elem.find_next("label")
                    if label:
                        results["genre"].append({
                            "value": input_elem.get("value"),
                            "label": label.get_text(strip=True),
                            "count": "All"
                        })
                        
            status_container = advanced_search.select_one(".filter.dropdown:has(button:contains('Status'))")
            if status_container:
                results["status"] = []
                for input_elem in status_container.select("input[name='status']"):
                    label = input_elem.find_next("label")
                    if label:
                        results["status"].append({
                            "value": input_elem.get("value"),
                            "label": label.get_text(strip=True),
                            "count": "All"
                        })
                        
            type_container = advanced_search.select_one(".filter.dropdown:has(button:contains('Type'))")
            if type_container:
                results["type"] = []
                for input_elem in type_container.select("input[name='type']"):
                    label = input_elem.find_next("label")
                    if label:
                        results["type"].append({
                            "value": input_elem.get("value"),
                            "label": label.get_text(strip=True),
                            "count": "All"
                        })
                        
            sub_container = advanced_search.select_one(".filter.dropdown:has(button:contains('Sub'))")
            if sub_container:
                results["sub"] = []
                for input_elem in sub_container.select("input[name='sub']"):
                    label = input_elem.find_next("label")
                    if label:
                        results["sub"].append({
                            "value": input_elem.get("value"),
                            "label": label.get_text(strip=True),
                            "count": "All"
                        })
                        
            order_container = advanced_search.select_one(".filter.dropdown:has(button:contains('Order by'))")
            if order_container:
                results["order"] = []
                for input_elem in order_container.select("input[name='order']"):
                    label = input_elem.find_next("label")
                    if label:
                        results["order"].append({
                            "value": input_elem.get("value"),
                            "label": label.get_text(strip=True),
                            "count": "All"
                        })
                        
            studio_container = advanced_search.select_one(".filter.dropdown:has(button:contains('Studio'))")
            if studio_container:
                results["studio"] = []
                for input_elem in studio_container.select("input[name='studio[]']"):
                    label = input_elem.find_next("label")
                    if label:
                        results["studio"].append({
                            "value": input_elem.get("value"),
                            "label": label.get_text(strip=True),
                            "count": "All"
                        })
                        
            season_container = advanced_search.select_one(".filter.dropdown:has(button:contains('Season'))")
            if season_container:
                results["season"] = []
                for input_elem in season_container.select("input[name='season[]']"):
                    label = input_elem.find_next("label")
                    if label:
                        results["season"].append({
                            "value": input_elem.get("value"),
                            "label": label.get_text(strip=True),
                            "count": "All"
                        })
                        
        except Exception as e:
            print(f"Error parsing advanced search filters: {e}")
            return {"error": f"Failed to parse advanced search filters: {str(e)}", "data": None}
            
        return results
        
    def parse_advanced_search_image(self, filters: Dict[str, str], page: str = "1") -> Dict[str, Any]:
        base_url = f"{self.base_url}/seri/"
        params = {}
        
        for key, value in filters.items():
            if value:
                params[key] = value
                
        if page != "1":
            params["page"] = page
            
        query_string = "&".join([f"{k}={v}" for k, v in params.items()])
        url = f"{base_url}?{query_string}" if query_string else base_url
        
        soup = self.get_page(url)
        if not soup:
            return {"error": "Failed to fetch advanced search results", "data": None}
            
        results = {
            "items": [],
            "pagination": {}
        }
        
        try:
            container = soup.select_one(".listupd")
            if container:
                for item in container.select(".bs .bsx"):
                    title_elem = item.select_one(".tt h2")
                    title = title_elem.get_text(strip=True) if title_elem else ""
                    link_elem = item.select_one("a")
                    slug = self.extract_slug(link_elem.get("href", "")) if link_elem else ""
                    thumbnail_elem = item.select_one("img")
                    thumbnail = thumbnail_elem.get("src", "") if thumbnail_elem else ""
                    type_elem = item.select_one(".typez")
                    media_type = type_elem.get_text(strip=True) if type_elem else ""
                    badge = item.select_one(".sb.Sub").get_text(strip=True) if item.select_one(".sb.Sub") else ""
                    url = link_elem.get("href", "") if link_elem else ""
                    
                    if title:
                        results["items"].append({
                            "title": title,
                            "slug": slug,
                            "thumbnail": urljoin(self.base_url, thumbnail) if thumbnail else "",
                            "type": media_type,
                            "badge": badge,
                            "url": urljoin(self.base_url, url) if url else ""
                        })
                        
            pagination_container = soup.select_one(".hpage")
            if pagination_container:
                prev_elem = pagination_container.select_one("a.l")
                next_elem = pagination_container.select_one("a.r")
                
                results["pagination"] = {
                    "prev": urljoin(self.base_url, prev_elem.get("href", "")) if prev_elem else "",
                    "next": urljoin(self.base_url, next_elem.get("href", "")) if next_elem else ""
                }
                
        except Exception as e:
            print(f"Error parsing advanced search image: {e}")
            return {"error": f"Failed to parse advanced search image: {str(e)}", "data": None}
            
        return results
        
    def parse_advanced_search_text(self) -> Dict[str, Any]:
        url = f"{self.base_url}/seri/list-mode/"
        soup = self.get_page(url)
        if not soup:
            return {"error": "Failed to fetch advanced search text", "data": None}
            
        results = {}
        
        try:
            blix_containers = soup.select(".blix")
            for container in blix_containers:
                letter_elem = container.select_one("span a")
                
                if letter_elem:
                    letter = letter_elem.get("name") or letter_elem.get_text(strip=True)
                    if letter:
                        results[letter] = []
                        
                        for item in container.select("li a.series"):
                            title = item.get_text(strip=True)
                            slug = self.extract_slug(item.get("href", ""))
                            url = item.get("href", "")
                            
                            if title:
                                results[letter].append({
                                    "title": title,
                                    "slug": slug,
                                    "url": urljoin(self.base_url, url) if url else ""
                                })
                                
        except Exception as e:
            print(f"Error parsing advanced search text: {e}")
            return {"error": f"Failed to parse advanced search text: {str(e)}", "data": None}
            
        return results