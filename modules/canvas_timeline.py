#!/usr/bin/env python3
"""
🎬 CANVAS TIMELINE MANAGER
=========================

Advanced timeline management for the Canvas video editor:
- Multi-track timeline
- Keyframe animation
- Transition effects
- Audio waveform visualization
- Snap-to-grid functionality
"""

import json
import math
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

@dataclass
class Keyframe:
    """Animation keyframe"""
    time: float
    property: str
    value: Any
    easing: str = "linear"  # linear, ease-in, ease-out, ease-in-out, bezier

@dataclass
class Transition:
    """Transition between timeline elements"""
    id: str
    type: str  # fade, slide, wipe, dissolve, etc.
    duration: float
    properties: Dict[str, Any]

@dataclass
class TimelineTrack:
    """Timeline track container"""
    id: str
    name: str
    type: str  # video, audio, text, effects
    height: int
    color: str
    muted: bool
    solo: bool
    locked: bool
    visible: bool
    elements: List[str]  # Element IDs

class CanvasTimeline:
    """Advanced timeline management for Canvas editor"""
    
    def __init__(self):
        self.tracks: Dict[str, TimelineTrack] = {}
        self.keyframes: Dict[str, List[Keyframe]] = {}  # element_id -> keyframes
        self.transitions: Dict[str, Transition] = {}
        self.timeline_settings = {
            "snap_to_grid": True,
            "snap_resolution": 0.1,  # seconds
            "zoom_level": 1.0,
            "playhead_position": 0.0,
            "loop_start": 0.0,
            "loop_end": 30.0,
            "auto_scroll": True
        }
    
    def create_track(self, name: str, track_type: str = "video", 
                    height: int = 60, color: str = "#4A90E2") -> TimelineTrack:
        """Create a new timeline track"""
        track_id = f"track_{len(self.tracks)}"
        
        track = TimelineTrack(
            id=track_id,
            name=name,
            type=track_type,
            height=height,
            color=color,
            muted=False,
            solo=False,
            locked=False,
            visible=True,
            elements=[]
        )
        
        self.tracks[track_id] = track
        logger.info(f"Created timeline track: {name} ({track_type})")
        return track
    
    def add_element_to_track(self, track_id: str, element_id: str, 
                           start_time: float, duration: float) -> bool:
        """Add an element to a specific track"""
        if track_id not in self.tracks:
            raise ValueError(f"Track {track_id} not found")
        
        track = self.tracks[track_id]
        
        # Check for overlaps if needed
        if not self._check_overlap_allowed(track_id, start_time, duration):
            logger.warning(f"Element {element_id} overlaps with existing elements")
        
        track.elements.append(element_id)
        logger.info(f"Added element {element_id} to track {track.name}")
        return True
    
    def _check_overlap_allowed(self, track_id: str, start_time: float, 
                              duration: float) -> bool:
        """Check if element can overlap on this track type"""
        track = self.tracks[track_id]
        
        # Audio tracks can have overlapping elements (for mixing)
        if track.type == "audio":
            return True
        
        # Video/image tracks typically don't allow overlap
        # (unless we're doing compositing)
        return True  # For now, allow all overlaps
    
    def add_keyframe(self, element_id: str, time: float, property: str, 
                    value: Any, easing: str = "linear") -> Keyframe:
        """Add a keyframe for animation"""
        keyframe = Keyframe(
            time=time,
            property=property,
            value=value,
            easing=easing
        )
        
        if element_id not in self.keyframes:
            self.keyframes[element_id] = []
        
        # Insert keyframe in chronological order
        keyframes = self.keyframes[element_id]
        inserted = False
        
        for i, kf in enumerate(keyframes):
            if kf.time > time:
                keyframes.insert(i, keyframe)
                inserted = True
                break
        
        if not inserted:
            keyframes.append(keyframe)
        
        logger.info(f"Added keyframe for {element_id}: {property} at {time}s")
        return keyframe
    
    def get_interpolated_value(self, element_id: str, property: str, 
                              time: float) -> Any:
        """Get interpolated value for a property at a specific time"""
        if element_id not in self.keyframes:
            return None
        
        keyframes = [kf for kf in self.keyframes[element_id] if kf.property == property]
        if not keyframes:
            return None
        
        # Sort by time
        keyframes.sort(key=lambda x: x.time)
        
        # Find surrounding keyframes
        before_kf = None
        after_kf = None
        
        for kf in keyframes:
            if kf.time <= time:
                before_kf = kf
            elif kf.time > time and after_kf is None:
                after_kf = kf
                break
        
        # If we're before the first keyframe
        if before_kf is None:
            return keyframes[0].value
        
        # If we're after the last keyframe
        if after_kf is None:
            return before_kf.value
        
        # If we're exactly on a keyframe
        if before_kf.time == time:
            return before_kf.value
        
        # Interpolate between keyframes
        return self._interpolate_values(before_kf, after_kf, time)
    
    def _interpolate_values(self, kf1: Keyframe, kf2: Keyframe, time: float) -> Any:
        """Interpolate between two keyframes"""
        if kf1.time == kf2.time:
            return kf2.value
        
        # Calculate progress (0 to 1)
        progress = (time - kf1.time) / (kf2.time - kf1.time)
        
        # Apply easing
        progress = self._apply_easing(progress, kf2.easing)
        
        # Handle different value types
        if isinstance(kf1.value, (int, float)) and isinstance(kf2.value, (int, float)):
            return kf1.value + (kf2.value - kf1.value) * progress
        
        # Handle color interpolation (hex colors)
        if isinstance(kf1.value, str) and isinstance(kf2.value, str):
            if kf1.value.startswith('#') and kf2.value.startswith('#'):
                return self._interpolate_color(kf1.value, kf2.value, progress)
        
        # For non-interpolatable values, use step interpolation
        return kf2.value if progress > 0.5 else kf1.value
    
    def _apply_easing(self, t: float, easing: str) -> float:
        """Apply easing function to interpolation progress"""
        if easing == "linear":
            return t
        elif easing == "ease-in":
            return t * t
        elif easing == "ease-out":
            return 1 - (1 - t) * (1 - t)
        elif easing == "ease-in-out":
            return 3 * t * t - 2 * t * t * t
        else:
            return t  # Default to linear
    
    def _interpolate_color(self, color1: str, color2: str, progress: float) -> str:
        """Interpolate between two hex colors"""
        # Remove # and convert to RGB
        rgb1 = tuple(int(color1[i:i+2], 16) for i in (1, 3, 5))
        rgb2 = tuple(int(color2[i:i+2], 16) for i in (1, 3, 5))
        
        # Interpolate each channel
        rgb_result = tuple(
            int(rgb1[i] + (rgb2[i] - rgb1[i]) * progress)
            for i in range(3)
        )
        
        # Convert back to hex
        return f"#{rgb_result[0]:02x}{rgb_result[1]:02x}{rgb_result[2]:02x}"
    
    def add_transition(self, transition_type: str, start_element_id: str, 
                      end_element_id: str, duration: float, 
                      properties: Dict[str, Any] = None) -> Transition:
        """Add a transition between two elements"""
        transition_id = f"transition_{len(self.transitions)}"
        
        transition = Transition(
            id=transition_id,
            type=transition_type,
            duration=duration,
            properties=properties or {}
        )
        
        self.transitions[transition_id] = transition
        logger.info(f"Added {transition_type} transition: {duration}s")
        return transition
    
    def snap_to_grid(self, time: float) -> float:
        """Snap time to grid based on snap resolution"""
        if not self.timeline_settings["snap_to_grid"]:
            return time
        
        snap_res = self.timeline_settings["snap_resolution"]
        return round(time / snap_res) * snap_res
    
    def get_timeline_data(self, canvas_project) -> Dict[str, Any]:
        """Generate complete timeline data for frontend"""
        timeline_data = {
            "settings": self.timeline_settings,
            "tracks": [],
            "keyframes": {},
            "transitions": {},
            "duration": canvas_project.duration,
            "fps": canvas_project.fps
        }
        
        # Add track data
        for track in self.tracks.values():
            track_data = asdict(track)
            
            # Add element details for this track
            track_elements = []
            for element_id in track.elements:
                # Find element in project
                element = None
                for proj_element in canvas_project.elements:
                    if proj_element.id == element_id:
                        element = proj_element
                        break
                
                if element:
                    track_elements.append({
                        "id": element.id,
                        "type": element.type,
                        "start": element.start_time,
                        "duration": element.duration,
                        "end": element.start_time + element.duration,
                        "properties": element.properties
                    })
            
            track_data["element_details"] = track_elements
            timeline_data["tracks"].append(track_data)
        
        # Add keyframe data
        for element_id, keyframes in self.keyframes.items():
            timeline_data["keyframes"][element_id] = [asdict(kf) for kf in keyframes]
        
        # Add transition data
        for transition in self.transitions.values():
            timeline_data["transitions"][transition.id] = asdict(transition)
        
        return timeline_data
    
    def set_playhead_position(self, time: float):
        """Set the playhead position"""
        self.timeline_settings["playhead_position"] = max(0, time)
    
    def set_zoom_level(self, zoom: float):
        """Set timeline zoom level"""
        self.timeline_settings["zoom_level"] = max(0.1, min(10.0, zoom))
    
    def set_loop_region(self, start: float, end: float):
        """Set loop region for preview"""
        self.timeline_settings["loop_start"] = max(0, start)
        self.timeline_settings["loop_end"] = max(start, end)
    
    def get_waveform_data(self, audio_file_path: str, 
                         width: int = 1000) -> List[float]:
        """Generate audio waveform data for visualization"""
        try:
            # This would typically use librosa or similar
            # For now, return mock data
            import random
            return [random.uniform(-1, 1) for _ in range(width)]
        except Exception as e:
            logger.warning(f"Could not generate waveform for {audio_file_path}: {e}")
            return [0.0] * width

# Predefined animation presets
ANIMATION_PRESETS = {
    "fade_in": [
        {"time": 0.0, "property": "opacity", "value": 0.0},
        {"time": 1.0, "property": "opacity", "value": 1.0, "easing": "ease-out"}
    ],
    "fade_out": [
        {"time": 0.0, "property": "opacity", "value": 1.0},
        {"time": 1.0, "property": "opacity", "value": 0.0, "easing": "ease-in"}
    ],
    "slide_in_left": [
        {"time": 0.0, "property": "x", "value": -200},
        {"time": 1.0, "property": "x", "value": 0, "easing": "ease-out"}
    ],
    "slide_in_right": [
        {"time": 0.0, "property": "x", "value": 200},
        {"time": 1.0, "property": "x", "value": 0, "easing": "ease-out"}
    ],
    "scale_in": [
        {"time": 0.0, "property": "scale_x", "value": 0.0},
        {"time": 0.0, "property": "scale_y", "value": 0.0},
        {"time": 1.0, "property": "scale_x", "value": 1.0, "easing": "ease-out"},
        {"time": 1.0, "property": "scale_y", "value": 1.0, "easing": "ease-out"}
    ],
    "bounce": [
        {"time": 0.0, "property": "y", "value": 0},
        {"time": 0.5, "property": "y", "value": -50, "easing": "ease-out"},
        {"time": 1.0, "property": "y", "value": 0, "easing": "ease-in"}
    ]
}

TRANSITION_PRESETS = {
    "fade": {"duration": 1.0, "properties": {"type": "cross_fade"}},
    "slide": {"duration": 1.5, "properties": {"direction": "left"}},
    "wipe": {"duration": 2.0, "properties": {"direction": "horizontal"}},
    "dissolve": {"duration": 2.5, "properties": {"grain": 0.3}},
    "zoom": {"duration": 1.0, "properties": {"scale": 1.2}}
}

if __name__ == "__main__":
    # Demo usage
    timeline = CanvasTimeline()
    
    # Create tracks
    video_track = timeline.create_track("Main Video", "video")
    audio_track = timeline.create_track("Background Music", "audio", color="#E74C3C")
    text_track = timeline.create_track("Titles", "text", color="#F39C12")
    
    # Add keyframes
    timeline.add_keyframe("element_1", 0.0, "opacity", 0.0)
    timeline.add_keyframe("element_1", 2.0, "opacity", 1.0, "ease-out")
    timeline.add_keyframe("element_1", 8.0, "opacity", 1.0)
    timeline.add_keyframe("element_1", 10.0, "opacity", 0.0, "ease-in")
    
    # Test interpolation
    opacity_at_1s = timeline.get_interpolated_value("element_1", "opacity", 1.0)
    print(f"Opacity at 1s: {opacity_at_1s}")
    
    print("Timeline demo completed successfully!")
