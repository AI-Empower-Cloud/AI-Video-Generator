#!/usr/bin/env python3
"""
Advanced Animation System for AI Video Generator

Features:
- Sophisticated character movements and gestures
- Emotion-based facial expressions
- Walk cycles and pose transitions
- Interactive character behaviors
- Physics-based animations
- Particle effects and special effects
"""

import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from typing import List, Dict, Optional, Tuple
import math
import random
from dataclasses import dataclass
from enum import Enum

class AnimationType(Enum):
    IDLE = "idle"
    WALKING = "walking"
    TALKING = "talking"
    GESTURING = "gesturing"
    EMOTIONAL = "emotional"
    TRANSITION = "transition"

class EmotionIntensity(Enum):
    SUBTLE = 0.3
    MODERATE = 0.6
    STRONG = 1.0

@dataclass
class AnimationKeyframe:
    """Represents a single animation keyframe."""
    frame_number: int
    character_position: Tuple[int, int]
    character_rotation: float
    facial_expression: Dict[str, float]
    gesture_state: Dict[str, float]
    scale: float = 1.0
    alpha: float = 1.0

@dataclass
class CharacterRig:
    """Character rigging for advanced animation."""
    head_center: Tuple[int, int]
    body_center: Tuple[int, int]
    left_arm: List[Tuple[int, int]]
    right_arm: List[Tuple[int, int]]
    facial_landmarks: Dict[str, Tuple[int, int]]

class AdvancedAnimationEngine:
    """Advanced animation system for character movements and expressions."""
    
    def __init__(self):
        self.animation_cache = {}
        self.expression_templates = self._create_expression_templates()
        self.gesture_patterns = self._create_gesture_patterns()
        self.physics_enabled = True
        
    def _create_expression_templates(self) -> Dict[str, Dict]:
        """Create facial expression templates."""
        return {
            'joy': {
                'mouth_curve': 0.8,
                'eye_opening': 0.7,
                'eyebrow_height': 0.2,
                'cheek_raise': 0.5
            },
            'sadness': {
                'mouth_curve': -0.6,
                'eye_opening': 0.3,
                'eyebrow_height': -0.3,
                'cheek_raise': -0.2
            },
            'anger': {
                'mouth_curve': -0.4,
                'eye_opening': 0.9,
                'eyebrow_height': -0.7,
                'cheek_raise': 0.0
            },
            'surprise': {
                'mouth_curve': 0.0,
                'eye_opening': 1.0,
                'eyebrow_height': 0.8,
                'cheek_raise': 0.1
            },
            'fear': {
                'mouth_curve': -0.2,
                'eye_opening': 1.0,
                'eyebrow_height': 0.5,
                'cheek_raise': -0.1
            },
            'neutral': {
                'mouth_curve': 0.0,
                'eye_opening': 0.5,
                'eyebrow_height': 0.0,
                'cheek_raise': 0.0
            }
        }
    
    def _create_gesture_patterns(self) -> Dict[str, List]:
        """Create gesture animation patterns."""
        return {
            'talking': [
                {'hand_position': (0.2, 0.3), 'intensity': 0.5},
                {'hand_position': (0.1, 0.4), 'intensity': 0.7},
                {'hand_position': (0.3, 0.2), 'intensity': 0.6},
                {'hand_position': (0.0, 0.5), 'intensity': 0.4}
            ],
            'explaining': [
                {'hand_position': (0.5, 0.2), 'intensity': 0.8},
                {'hand_position': (0.7, 0.3), 'intensity': 0.9},
                {'hand_position': (0.3, 0.4), 'intensity': 0.6},
                {'hand_position': (0.1, 0.3), 'intensity': 0.5}
            ],
            'greeting': [
                {'hand_position': (0.8, 0.1), 'intensity': 1.0},
                {'hand_position': (0.9, 0.0), 'intensity': 0.8},
                {'hand_position': (0.7, 0.2), 'intensity': 0.6},
                {'hand_position': (0.5, 0.3), 'intensity': 0.3}
            ]
        }
    
    def generate_character_rig(self, character_center: Tuple[int, int], 
                             size: int = 200) -> CharacterRig:
        """Generate character rigging for animation."""
        cx, cy = character_center
        
        # Character proportions
        head_size = size // 4
        body_height = size // 2
        arm_length = size // 3
        
        # Head center
        head_center = (cx, cy - size // 3)
        
        # Body center
        body_center = (cx, cy)
        
        # Arm joints (shoulder, elbow, wrist)
        left_arm = [
            (cx - size // 6, cy - size // 6),  # Shoulder
            (cx - size // 4, cy),              # Elbow
            (cx - size // 3, cy + size // 6)   # Wrist
        ]
        
        right_arm = [
            (cx + size // 6, cy - size // 6),  # Shoulder
            (cx + size // 4, cy),              # Elbow
            (cx + size // 3, cy + size // 6)   # Wrist
        ]
        
        # Facial landmarks
        facial_landmarks = {
            'left_eye': (head_center[0] - head_size // 4, head_center[1] - head_size // 6),
            'right_eye': (head_center[0] + head_size // 4, head_center[1] - head_size // 6),
            'nose': (head_center[0], head_center[1]),
            'mouth': (head_center[0], head_center[1] + head_size // 4),
            'left_eyebrow': (head_center[0] - head_size // 4, head_center[1] - head_size // 3),
            'right_eyebrow': (head_center[0] + head_size // 4, head_center[1] - head_size // 3)
        }
        
        return CharacterRig(
            head_center=head_center,
            body_center=body_center,
            left_arm=left_arm,
            right_arm=right_arm,
            facial_landmarks=facial_landmarks
        )
    
    def create_animation_sequence(self, animation_type: AnimationType, 
                                duration_frames: int, 
                                character_info: Dict,
                                emotion: str = 'neutral') -> List[AnimationKeyframe]:
        """Create a sequence of animation keyframes."""
        keyframes = []
        
        for frame in range(duration_frames):
            progress = frame / duration_frames
            
            keyframe = self._generate_keyframe(
                frame, progress, animation_type, character_info, emotion
            )
            keyframes.append(keyframe)
        
        return keyframes
    
    def _generate_keyframe(self, frame_num: int, progress: float, 
                         animation_type: AnimationType, character_info: Dict,
                         emotion: str) -> AnimationKeyframe:
        """Generate a single animation keyframe."""
        base_position = (200, 200)  # Default character position
        
        # Animation-specific positioning
        if animation_type == AnimationType.WALKING:
            # Walking animation with bobbing motion
            x_offset = math.sin(progress * math.pi * 4) * 10
            y_offset = abs(math.sin(progress * math.pi * 8)) * 5
            position = (base_position[0] + x_offset, base_position[1] + y_offset)
        
        elif animation_type == AnimationType.TALKING:
            # Subtle head movement while talking
            x_offset = math.sin(progress * math.pi * 6) * 3
            y_offset = math.cos(progress * math.pi * 4) * 2
            position = (base_position[0] + x_offset, base_position[1] + y_offset)
        
        elif animation_type == AnimationType.GESTURING:
            # More animated movement for gesturing
            x_offset = math.sin(progress * math.pi * 3) * 8
            y_offset = math.cos(progress * math.pi * 2) * 4
            position = (base_position[0] + x_offset, base_position[1] + y_offset)
        
        else:  # IDLE or other
            # Subtle breathing animation
            y_offset = math.sin(progress * math.pi * 2) * 2
            position = (base_position[0], base_position[1] + y_offset)
        
        # Get facial expression based on emotion
        facial_expression = self._interpolate_expression(emotion, progress)
        
        # Get gesture state
        gesture_state = self._get_gesture_state(animation_type, progress)
        
        return AnimationKeyframe(
            frame_number=frame_num,
            character_position=position,
            character_rotation=0.0,
            facial_expression=facial_expression,
            gesture_state=gesture_state,
            scale=1.0 + math.sin(progress * math.pi * 2) * 0.02,  # Subtle scaling
            alpha=1.0
        )
    
    def _interpolate_expression(self, emotion: str, progress: float) -> Dict[str, float]:
        """Interpolate facial expression over time."""
        base_expression = self.expression_templates.get(emotion, self.expression_templates['neutral'])
        
        # Add subtle animation to expression
        animated_expression = {}
        for feature, value in base_expression.items():
            # Add slight variation over time
            variation = math.sin(progress * math.pi * 4) * 0.1
            animated_expression[feature] = value + variation
        
        return animated_expression
    
    def _get_gesture_state(self, animation_type: AnimationType, progress: float) -> Dict[str, float]:
        """Get gesture state for the current animation."""
        if animation_type == AnimationType.TALKING:
            pattern = self.gesture_patterns['talking']
        elif animation_type == AnimationType.GESTURING:
            pattern = self.gesture_patterns['explaining']
        else:
            return {'hand_position': (0.0, 0.0), 'intensity': 0.0}
        
        # Cycle through gesture pattern
        pattern_index = int(progress * len(pattern)) % len(pattern)
        return pattern[pattern_index]
    
    def render_animated_character(self, img: Image.Image, character_rig: CharacterRig,
                                keyframe: AnimationKeyframe, character_info: Dict) -> Image.Image:
        """Render an animated character on the image."""
        draw = ImageDraw.Draw(img)
        
        # Apply keyframe transformations
        position = keyframe.character_position
        expression = keyframe.facial_expression
        gesture = keyframe.gesture_state
        
        # Render head with expression
        self._render_animated_head(draw, character_rig, position, expression, character_info)
        
        # Render body
        self._render_animated_body(draw, character_rig, position, gesture)
        
        # Render arms with gestures
        self._render_animated_arms(draw, character_rig, position, gesture)
        
        return img
    
    def _render_animated_head(self, draw: ImageDraw.Draw, rig: CharacterRig,
                            position: Tuple[int, int], expression: Dict,
                            character_info: Dict):
        """Render animated head with expressions."""
        head_x, head_y = position
        head_size = 80
        
        # Get character colors
        skin_tone = character_info.get('skin_tone', (255, 220, 177))
        hair_color = character_info.get('hair_color', (139, 69, 19))
        eye_color = character_info.get('eye_color', (139, 69, 19))
        
        # Draw head
        draw.ellipse([
            head_x - head_size//2, head_y - head_size//2,
            head_x + head_size//2, head_y + head_size//2
        ], fill=skin_tone, outline=(0, 0, 0), width=2)
        
        # Draw hair
        hair_y = head_y - head_size//2
        draw.ellipse([
            head_x - head_size//2, hair_y - head_size//4,
            head_x + head_size//2, hair_y + head_size//4
        ], fill=hair_color, outline=(0, 0, 0), width=1)
        
        # Animated eyes based on expression
        eye_opening = expression.get('eye_opening', 0.5)
        eye_size = int(12 * eye_opening)
        eyebrow_offset = int(expression.get('eyebrow_height', 0.0) * 10)
        
        # Left eye
        left_eye_x = head_x - 20
        left_eye_y = head_y - 10
        draw.ellipse([
            left_eye_x - eye_size//2, left_eye_y - eye_size//2,
            left_eye_x + eye_size//2, left_eye_y + eye_size//2
        ], fill=(255, 255, 255), outline=(0, 0, 0), width=1)
        
        # Eye pupil
        pupil_size = max(2, eye_size // 3)
        draw.ellipse([
            left_eye_x - pupil_size//2, left_eye_y - pupil_size//2,
            left_eye_x + pupil_size//2, left_eye_y + pupil_size//2
        ], fill=eye_color)
        
        # Right eye
        right_eye_x = head_x + 20
        right_eye_y = head_y - 10
        draw.ellipse([
            right_eye_x - eye_size//2, right_eye_y - eye_size//2,
            right_eye_x + eye_size//2, right_eye_y + eye_size//2
        ], fill=(255, 255, 255), outline=(0, 0, 0), width=1)
        
        draw.ellipse([
            right_eye_x - pupil_size//2, right_eye_y - pupil_size//2,
            right_eye_x + pupil_size//2, right_eye_y + pupil_size//2
        ], fill=eye_color)
        
        # Animated eyebrows
        left_brow_y = head_y - 25 + eyebrow_offset
        right_brow_y = head_y - 25 + eyebrow_offset
        
        draw.arc([
            left_eye_x - 15, left_brow_y - 5,
            left_eye_x + 15, left_brow_y + 5
        ], 0, 180, fill=(hair_color), width=3)
        
        draw.arc([
            right_eye_x - 15, right_brow_y - 5,
            right_eye_x + 15, right_brow_y + 5
        ], 0, 180, fill=(hair_color), width=3)
        
        # Animated mouth based on expression
        mouth_curve = expression.get('mouth_curve', 0.0)
        mouth_y = head_y + 20
        mouth_width = 25
        
        if mouth_curve > 0:  # Smile
            draw.arc([
                head_x - mouth_width, mouth_y - int(mouth_curve * 15),
                head_x + mouth_width, mouth_y + int(mouth_curve * 15)
            ], 0, 180, fill=(200, 100, 100), width=3)
        elif mouth_curve < 0:  # Frown
            draw.arc([
                head_x - mouth_width, mouth_y + int(abs(mouth_curve) * 15),
                head_x + mouth_width, mouth_y - int(abs(mouth_curve) * 15)
            ], 180, 360, fill=(200, 100, 100), width=3)
        else:  # Neutral
            draw.ellipse([
                head_x - mouth_width//3, mouth_y - 5,
                head_x + mouth_width//3, mouth_y + 5
            ], fill=(200, 100, 100), outline=(0, 0, 0), width=1)
        
        # Nose
        draw.ellipse([
            head_x - 4, head_y - 4,
            head_x + 4, head_y + 4
        ], fill=tuple(max(0, c-20) for c in skin_tone))
    
    def _render_animated_body(self, draw: ImageDraw.Draw, rig: CharacterRig,
                            position: Tuple[int, int], gesture: Dict):
        """Render animated body."""
        body_x, body_y = position
        body_y += 60  # Offset below head
        
        # Body (rectangle)
        body_width = 50
        body_height = 80
        
        draw.rectangle([
            body_x - body_width//2, body_y,
            body_x + body_width//2, body_y + body_height
        ], fill=(100, 100, 200), outline=(0, 0, 0), width=2)
    
    def _render_animated_arms(self, draw: ImageDraw.Draw, rig: CharacterRig,
                            position: Tuple[int, int], gesture: Dict):
        """Render animated arms with gestures."""
        body_x, body_y = position
        shoulder_y = body_y + 20
        
        # Get gesture parameters
        hand_pos = gesture.get('hand_position', (0.0, 0.0))
        intensity = gesture.get('intensity', 0.0)
        
        # Animate arm positions based on gesture
        arm_offset_x = int(hand_pos[0] * 50 * intensity)
        arm_offset_y = int(hand_pos[1] * 30 * intensity)
        
        # Left arm
        left_shoulder = (body_x - 25, shoulder_y)
        left_hand = (left_shoulder[0] - 30 + arm_offset_x, left_shoulder[1] + 40 + arm_offset_y)
        
        draw.line([left_shoulder, left_hand], fill=(139, 69, 19), width=8)
        draw.ellipse([
            left_hand[0] - 8, left_hand[1] - 8,
            left_hand[0] + 8, left_hand[1] + 8
        ], fill=(255, 220, 177), outline=(0, 0, 0), width=1)
        
        # Right arm
        right_shoulder = (body_x + 25, shoulder_y)
        right_hand = (right_shoulder[0] + 30 - arm_offset_x, right_shoulder[1] + 40 + arm_offset_y)
        
        draw.line([right_shoulder, right_hand], fill=(139, 69, 19), width=8)
        draw.ellipse([
            right_hand[0] - 8, right_hand[1] - 8,
            right_hand[0] + 8, right_hand[1] + 8
        ], fill=(255, 220, 177), outline=(0, 0, 0), width=1)
    
    def create_particle_effect(self, img: Image.Image, effect_type: str,
                             center: Tuple[int, int], intensity: float = 1.0) -> Image.Image:
        """Add particle effects to the image."""
        draw = ImageDraw.Draw(img)
        
        if effect_type == 'sparkles':
            self._render_sparkles(draw, center, intensity)
        elif effect_type == 'magic':
            self._render_magic_particles(draw, center, intensity)
        elif effect_type == 'emotion_burst':
            self._render_emotion_particles(draw, center, intensity)
        
        return img
    
    def _render_sparkles(self, draw: ImageDraw.Draw, center: Tuple[int, int], intensity: float):
        """Render sparkle particles."""
        cx, cy = center
        num_sparkles = int(10 * intensity)
        
        for _ in range(num_sparkles):
            # Random position around center
            offset_x = random.randint(-50, 50)
            offset_y = random.randint(-50, 50)
            
            sparkle_x = cx + offset_x
            sparkle_y = cy + offset_y
            
            # Random sparkle size
            size = random.randint(2, 6)
            
            # Draw sparkle as star shape
            points = []
            for i in range(8):
                angle = i * math.pi / 4
                if i % 2 == 0:
                    radius = size
                else:
                    radius = size // 2
                
                x = sparkle_x + radius * math.cos(angle)
                y = sparkle_y + radius * math.sin(angle)
                points.append((x, y))
            
            draw.polygon(points, fill=(255, 255, 0), outline=(255, 255, 255))
    
    def _render_magic_particles(self, draw: ImageDraw.Draw, center: Tuple[int, int], intensity: float):
        """Render magical particle effects."""
        cx, cy = center
        num_particles = int(15 * intensity)
        
        colors = [(255, 0, 255), (0, 255, 255), (255, 255, 0), (255, 0, 0)]
        
        for i in range(num_particles):
            # Spiral pattern
            angle = i * 2 * math.pi / num_particles
            radius = 30 + i * 2
            
            particle_x = cx + radius * math.cos(angle)
            particle_y = cy + radius * math.sin(angle)
            
            color = random.choice(colors)
            size = random.randint(3, 8)
            
            draw.ellipse([
                particle_x - size, particle_y - size,
                particle_x + size, particle_y + size
            ], fill=color, outline=(255, 255, 255))
    
    def _render_emotion_particles(self, draw: ImageDraw.Draw, center: Tuple[int, int], intensity: float):
        """Render emotion-based particle effects."""
        cx, cy = center
        num_particles = int(8 * intensity)
        
        # Heart shapes for positive emotions
        for i in range(num_particles):
            offset_x = random.randint(-40, 40)
            offset_y = random.randint(-40, 40)
            
            heart_x = cx + offset_x
            heart_y = cy + offset_y
            
            # Simple heart shape using two circles and a triangle
            draw.ellipse([heart_x - 5, heart_y - 3, heart_x + 1, heart_y + 3], fill=(255, 0, 0))
            draw.ellipse([heart_x - 1, heart_y - 3, heart_x + 5, heart_y + 3], fill=(255, 0, 0))
            draw.polygon([(heart_x - 5, heart_y + 1), (heart_x + 5, heart_y + 1), (heart_x, heart_y + 8)], fill=(255, 0, 0))

# Test the advanced animation system
def test_advanced_animations():
    """Test the advanced animation system."""
    print("🎭 Testing Advanced Animation System...")
    
    engine = AdvancedAnimationEngine()
    
    # Create test image
    img = Image.new('RGB', (400, 400), (200, 200, 255))
    
    # Create character rig
    character_center = (200, 200)
    rig = engine.generate_character_rig(character_center)
    
    # Create animation sequence
    character_info = {
        'name': 'TestCharacter',
        'skin_tone': (255, 220, 177),
        'hair_color': (139, 69, 19),
        'eye_color': (0, 100, 0)
    }
    
    # Test different animation types
    animations = [
        (AnimationType.TALKING, 'joy'),
        (AnimationType.GESTURING, 'surprise'),
        (AnimationType.WALKING, 'neutral')
    ]
    
    for anim_type, emotion in animations:
        print(f"  Testing {anim_type.value} animation with {emotion} emotion...")
        
        keyframes = engine.create_animation_sequence(
            anim_type, 10, character_info, emotion
        )
        
        # Render a sample frame
        test_img = img.copy()
        sample_keyframe = keyframes[5]  # Middle frame
        
        animated_img = engine.render_animated_character(
            test_img, rig, sample_keyframe, character_info
        )
        
        # Add particle effects
        if anim_type == AnimationType.GESTURING:
            animated_img = engine.create_particle_effect(
                animated_img, 'sparkles', character_center, 0.8
            )
        
        # Save test frame
        output_path = f"test_animation_{anim_type.value}_{emotion}.png"
        animated_img.save(output_path)
        print(f"    ✅ Saved test frame: {output_path}")
    
    print("🎭 Advanced animation system test completed!")

if __name__ == "__main__":
    test_advanced_animations()
