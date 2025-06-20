# NLP Processing Guide - AI Video Generator

## 🧠 Natural Language Processing Deep Dive

This guide provides detailed information about the NLP processing capabilities of the AI Video Generator, including character extraction, emotion detection, and coreference resolution.

## 📋 Table of Contents

1. [Overview](#overview)
2. [Text Processing Pipeline](#text-processing-pipeline)
3. [Character Extraction](#character-extraction)
4. [Emotion Detection](#emotion-detection)
5. [Coreference Resolution](#coreference-resolution)
6. [Scene Segmentation](#scene-segmentation)
7. [Advanced Features](#advanced-features)
8. [Performance Optimization](#performance-optimization)
9. [Troubleshooting](#troubleshooting)

## 🎯 Overview

The NLP processing system uses state-of-the-art libraries and models to analyze text stories and extract meaningful information for video generation:

- **spaCy**: Industrial-strength NLP for text processing
- **Coreferee**: Coreference resolution for pronoun linking
- **Transformers**: Emotion detection using pre-trained models
- **Custom algorithms**: Character validation and scene segmentation

## 🔄 Text Processing Pipeline

### 1. Input Processing
```python
def process_text_input(text):
    """
    Initial text processing and validation
    """
    # Text cleaning and normalization
    cleaned_text = clean_and_normalize(text)
    
    # Language detection
    language = detect_language(cleaned_text)
    
    # Text segmentation
    sentences = segment_sentences(cleaned_text)
    
    return cleaned_text, language, sentences
```

### 2. spaCy Analysis
```python
def analyze_with_spacy(text):
    """
    Advanced linguistic analysis using spaCy
    """
    # Load model with fallback strategy
    nlp = load_spacy_model()
    
    # Process text
    doc = nlp(text)
    
    # Extract linguistic features
    tokens = [token for token in doc]
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    pos_tags = [(token.text, token.pos_) for token in doc]
    
    return doc, tokens, entities, pos_tags
```

### 3. Feature Extraction
```python
def extract_features(doc):
    """
    Extract relevant features for video generation
    """
    features = {
        'characters': extract_characters(doc),
        'locations': extract_locations(doc),
        'actions': extract_actions(doc),
        'emotions': extract_emotions(doc),
        'temporal_markers': extract_time_markers(doc)
    }
    
    return features
```

## 👥 Character Extraction

### Character Detection Algorithm

The system uses multiple strategies to identify characters in stories:

#### 1. Named Entity Recognition (NER)
```python
def extract_person_entities(doc):
    """
    Extract PERSON entities using spaCy NER
    """
    persons = []
    
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            persons.append({
                'name': ent.text,
                'start': ent.start_char,
                'end': ent.end_char,
                'confidence': ent._.confidence if hasattr(ent._, 'confidence') else 1.0
            })
    
    return persons
```

#### 2. Pronoun Analysis
```python
def analyze_pronouns(doc):
    """
    Analyze pronouns for gender and character linking
    """
    pronouns = {
        'male': ['he', 'him', 'his', 'himself'],
        'female': ['she', 'her', 'hers', 'herself'],
        'neutral': ['they', 'them', 'their', 'themselves']
    }
    
    pronoun_data = []
    
    for token in doc:
        if token.text.lower() in sum(pronouns.values(), []):
            gender = next((k for k, v in pronouns.items() if token.text.lower() in v), 'neutral')
            
            pronoun_data.append({
                'text': token.text,
                'gender': gender,
                'position': token.i,
                'sentence': token.sent.text
            })
    
    return pronoun_data
```

#### 3. Gender Detection
```python
def detect_character_gender(character_name, context_text, pronouns):
    """
    Detect character gender using multiple signals
    """
    # Common name patterns
    male_names = ['john', 'bob', 'david', 'michael', 'james']
    female_names = ['alice', 'sarah', 'mary', 'jennifer', 'lisa']
    
    name_lower = character_name.lower()
    
    # Check common names
    if any(name in name_lower for name in male_names):
        return 'male'
    elif any(name in name_lower for name in female_names):
        return 'female'
    
    # Analyze pronouns in context
    context_lower = context_text.lower()
    male_pronouns = context_lower.count('he ') + context_lower.count('him ') + context_lower.count('his ')
    female_pronouns = context_lower.count('she ') + context_lower.count('her ') + context_lower.count('hers ')
    
    if male_pronouns > female_pronouns:
        return 'male'
    elif female_pronouns > male_pronouns:
        return 'female'
    
    return 'neutral'
```

### Character Validation and Deduplication
```python
def validate_characters(raw_characters):
    """
    Validate and deduplicate character list
    """
    validated = []
    seen_names = set()
    
    for char in raw_characters:
        # Normalize name
        normalized_name = normalize_name(char['name'])
        
        # Skip if already seen (case-insensitive)
        if normalized_name.lower() in seen_names:
            continue
        
        # Validate name format
        if is_valid_character_name(normalized_name):
            validated.append({
                'name': normalized_name,
                'gender': char.get('gender', 'neutral'),
                'mentions': char.get('mentions', 1),
                'first_appearance': char.get('first_appearance', 0)
            })
            seen_names.add(normalized_name.lower())
    
    return validated
```

## 😊 Emotion Detection

### Emotion Analysis Pipeline

The system uses transformer models to detect emotions in text segments:

#### 1. Model Configuration
```python
EMOTION_CONFIG = {
    'model_name': 'j-hartmann/emotion-english-distilroberta-base',
    'labels': ['joy', 'sadness', 'anger', 'fear', 'surprise', 'neutral'],
    'confidence_threshold': 0.5,
    'batch_size': 16,
    'max_length': 512
}
```

#### 2. Emotion Detection Function
```python
def detect_emotion_advanced(text_segment):
    """
    Advanced emotion detection with context awareness
    """
    # Load emotion detection model
    classifier = pipeline(
        "text-classification",
        model=EMOTION_CONFIG['model_name'],
        device=0 if torch.cuda.is_available() else -1
    )
    
    # Process text
    result = classifier(text_segment)
    
    # Extract emotion with confidence
    emotion = result[0]['label'].lower()
    confidence = result[0]['score']
    
    # Apply confidence threshold
    if confidence < EMOTION_CONFIG['confidence_threshold']:
        emotion = 'neutral'
    
    return {
        'emotion': emotion,
        'confidence': confidence,
        'raw_results': result
    }
```

#### 3. Context-Aware Emotion Analysis
```python
def analyze_emotion_with_context(text, window_size=3):
    """
    Analyze emotion considering surrounding context
    """
    sentences = split_into_sentences(text)
    emotions = []
    
    for i, sentence in enumerate(sentences):
        # Get context window
        start_idx = max(0, i - window_size)
        end_idx = min(len(sentences), i + window_size + 1)
        context = ' '.join(sentences[start_idx:end_idx])
        
        # Detect emotion with context
        emotion_data = detect_emotion_advanced(context)
        emotion_data['sentence'] = sentence
        emotion_data['position'] = i
        
        emotions.append(emotion_data)
    
    return emotions
```

### Emotion Mapping and Visualization
```python
def map_emotions_to_colors(emotion):
    """
    Map emotions to visual colors for video generation
    """
    emotion_colors = {
        'joy': {
            'primary': (255, 223, 0),      # Golden yellow
            'secondary': (255, 165, 0),    # Orange
            'background': (255, 248, 220)  # Cornsilk
        },
        'sadness': {
            'primary': (70, 130, 180),     # Steel blue
            'secondary': (100, 149, 237),  # Cornflower blue
            'background': (176, 196, 222)  # Light steel blue
        },
        'anger': {
            'primary': (220, 20, 60),      # Crimson
            'secondary': (255, 69, 0),     # Red orange
            'background': (255, 160, 122)  # Light salmon
        },
        'fear': {
            'primary': (128, 128, 128),    # Gray
            'secondary': (169, 169, 169),  # Dark gray
            'background': (211, 211, 211)  # Light gray
        },
        'surprise': {
            'primary': (255, 20, 147),     # Deep pink
            'secondary': (255, 105, 180),  # Hot pink
            'background': (255, 182, 193)  # Light pink
        },
        'neutral': {
            'primary': (119, 136, 153),    # Light slate gray
            'secondary': (176, 196, 222),  # Light steel blue
            'background': (240, 248, 255)  # Alice blue
        }
    }
    
    return emotion_colors.get(emotion, emotion_colors['neutral'])
```

## 🔗 Coreference Resolution

### Coreferee Integration
```python
def setup_coreference_resolution():
    """
    Setup coreference resolution with multiple fallback strategies
    """
    strategies = [
        # Strategy 1: Full coreferee integration
        lambda nlp: nlp.add_pipe('coreferee'),
        
        # Strategy 2: Manual coreferee processing
        lambda nlp: setup_manual_coreferee(nlp),
        
        # Strategy 3: Rule-based pronoun linking
        lambda nlp: setup_rule_based_linking(nlp)
    ]
    
    for i, strategy in enumerate(strategies, 1):
        try:
            nlp = spacy.load("en_core_web_sm")
            strategy(nlp)
            print(f"✅ Coreference Strategy {i} successful")
            return nlp
        except Exception as e:
            print(f"❌ Strategy {i} failed: {e}")
            continue
    
    print("⚠️ All coreference strategies failed, using basic NLP")
    return spacy.load("en_core_web_sm")
```

### Manual Coreference Processing
```python
def resolve_coreferences_manually(doc, characters):
    """
    Manual coreference resolution when coreferee fails
    """
    resolved_references = []
    
    for token in doc:
        if token.pos_ == 'PRON':
            # Find nearest character mention
            nearest_char = find_nearest_character(token, characters, doc)
            
            if nearest_char:
                resolved_references.append({
                    'pronoun': token.text,
                    'position': token.i,
                    'resolved_to': nearest_char['name'],
                    'confidence': calculate_resolution_confidence(token, nearest_char, doc)
                })
    
    return resolved_references
```

### Rule-Based Pronoun Linking
```python
def link_pronouns_to_characters(doc, characters):
    """
    Rule-based approach to link pronouns to characters
    """
    links = []
    
    for sent in doc.sents:
        sent_characters = [char for char in characters if char['name'] in sent.text]
        
        for token in sent:
            if token.pos_ == 'PRON':
                # Apply linking rules
                linked_char = apply_linking_rules(token, sent_characters, sent)
                
                if linked_char:
                    links.append({
                        'pronoun': token.text,
                        'character': linked_char['name'],
                        'sentence': sent.text,
                        'rule_applied': get_applied_rule(token, linked_char)
                    })
    
    return links
```

## 🎭 Scene Segmentation

### Scene Boundary Detection
```python
def detect_scene_boundaries(doc):
    """
    Detect natural scene boundaries in the story
    """
    boundaries = []
    
    # Sentence-level analysis
    sentences = list(doc.sents)
    
    for i, sent in enumerate(sentences):
        # Check for scene transition markers
        if has_scene_transition_markers(sent):
            boundaries.append({
                'position': i,
                'type': 'explicit_transition',
                'sentence': sent.text
            })
        
        # Check for temporal markers
        elif has_temporal_markers(sent):
            boundaries.append({
                'position': i,
                'type': 'temporal_transition',
                'sentence': sent.text
            })
        
        # Check for character focus shifts
        elif has_character_shift(sent, sentences[max(0, i-1):i+2]):
            boundaries.append({
                'position': i,
                'type': 'character_shift',
                'sentence': sent.text
            })
    
    return boundaries
```

### Scene Content Analysis
```python
def analyze_scene_content(scene_text):
    """
    Analyze the content of a scene for video generation
    """
    doc = nlp(scene_text)
    
    analysis = {
        'characters': extract_scene_characters(doc),
        'location': detect_scene_location(doc),
        'actions': extract_scene_actions(doc),
        'emotions': detect_scene_emotions(doc),
        'dialogue': extract_dialogue(doc),
        'setting': {
            'time_of_day': detect_time_of_day(doc),
            'weather': detect_weather(doc),
            'indoor_outdoor': detect_indoor_outdoor(doc)
        }
    }
    
    return analysis
```

## 🚀 Advanced Features

### Multi-Language Support
```python
def detect_and_process_language(text):
    """
    Detect language and use appropriate processing models
    """
    # Language detection
    detected_lang = detect_language(text)
    
    # Load appropriate spaCy model
    model_map = {
        'en': 'en_core_web_sm',
        'es': 'es_core_news_sm',
        'fr': 'fr_core_news_sm',
        'de': 'de_core_news_sm'
    }
    
    model_name = model_map.get(detected_lang, 'en_core_web_sm')
    
    try:
        nlp = spacy.load(model_name)
        return nlp, detected_lang
    except OSError:
        print(f"Model {model_name} not found, falling back to English")
        return spacy.load('en_core_web_sm'), 'en'
```

### Batch Processing
```python
def process_multiple_stories(stories, batch_size=5):
    """
    Process multiple stories efficiently
    """
    results = []
    
    for i in range(0, len(stories), batch_size):
        batch = stories[i:i + batch_size]
        
        # Process batch
        batch_results = []
        for story in batch:
            try:
                characters, scenes = parse_characters_and_scenes(story)
                batch_results.append({
                    'story': story,
                    'characters': characters,
                    'scenes': scenes,
                    'status': 'success'
                })
            except Exception as e:
                batch_results.append({
                    'story': story,
                    'error': str(e),
                    'status': 'failed'
                })
        
        results.extend(batch_results)
        
        # Optional: yield results for streaming processing
        yield batch_results
    
    return results
```

## 📊 Performance Optimization

### Model Caching
```python
class NLPModelCache:
    """
    Cache NLP models for improved performance
    """
    def __init__(self):
        self._models = {}
        self._emotion_classifier = None
    
    def get_spacy_model(self, model_name='en_core_web_sm'):
        """Get cached spaCy model"""
        if model_name not in self._models:
            self._models[model_name] = spacy.load(model_name)
        return self._models[model_name]
    
    def get_emotion_classifier(self):
        """Get cached emotion classifier"""
        if self._emotion_classifier is None:
            self._emotion_classifier = pipeline(
                "text-classification",
                model="j-hartmann/emotion-english-distilroberta-base"
            )
        return self._emotion_classifier
    
    def clear_cache(self):
        """Clear model cache to free memory"""
        self._models.clear()
        self._emotion_classifier = None
        gc.collect()

# Global cache instance
model_cache = NLPModelCache()
```

### Memory Management
```python
def process_large_text(text, chunk_size=1000):
    """
    Process large texts in chunks to manage memory
    """
    chunks = split_text_into_chunks(text, chunk_size)
    all_characters = []
    all_scenes = []
    
    for chunk in chunks:
        try:
            characters, scenes = parse_characters_and_scenes(chunk)
            all_characters.extend(characters)
            all_scenes.extend(scenes)
            
            # Clear memory after each chunk
            gc.collect()
            
        except Exception as e:
            print(f"Error processing chunk: {e}")
            continue
    
    # Deduplicate and merge results
    merged_characters = deduplicate_characters(all_characters)
    merged_scenes = merge_scenes(all_scenes)
    
    return merged_characters, merged_scenes
```

## 🐛 Troubleshooting

### Common NLP Issues

#### Character Detection Problems
```python
def diagnose_character_detection(text):
    """
    Diagnose character detection issues
    """
    doc = nlp(text)
    
    diagnostics = {
        'total_entities': len(doc.ents),
        'person_entities': len([ent for ent in doc.ents if ent.label_ == 'PERSON']),
        'tokens': len(doc),
        'sentences': len(list(doc.sents)),
        'potential_names': []
    }
    
    # Look for capitalized words that might be names
    for token in doc:
        if token.is_title and token.pos_ in ['NOUN', 'PROPN']:
            diagnostics['potential_names'].append(token.text)
    
    return diagnostics
```

#### Emotion Detection Issues
```python
def debug_emotion_detection(text):
    """
    Debug emotion detection problems
    """
    try:
        result = detect_emotion(text)
        
        debug_info = {
            'detected_emotion': result,
            'text_length': len(text),
            'word_count': len(text.split()),
            'contains_emotion_words': check_emotion_keywords(text),
            'preprocessing_needed': needs_preprocessing(text)
        }
        
        return debug_info
        
    except Exception as e:
        return {
            'error': str(e),
            'text_sample': text[:100] + '...' if len(text) > 100 else text,
            'possible_causes': [
                'Text too short or long',
                'Special characters causing issues',
                'Model loading problems'
            ]
        }
```

### Performance Monitoring
```python
def monitor_nlp_performance():
    """
    Monitor NLP processing performance
    """
    import psutil
    import time
    
    start_time = time.time()
    start_memory = psutil.virtual_memory().used
    
    # Process sample text
    sample_text = "Alice met Bob in the park. She was happy to see him."
    characters, scenes = parse_characters_and_scenes(sample_text)
    
    end_time = time.time()
    end_memory = psutil.virtual_memory().used
    
    performance_metrics = {
        'processing_time': end_time - start_time,
        'memory_used': end_memory - start_memory,
        'characters_found': len(characters),
        'scenes_found': len(scenes),
        'words_per_second': len(sample_text.split()) / (end_time - start_time)
    }
    
    return performance_metrics
```

---

This guide provides comprehensive information about the NLP processing capabilities of the AI Video Generator. For more specific implementation details, refer to the source code in `main.py` and the API reference documentation.
