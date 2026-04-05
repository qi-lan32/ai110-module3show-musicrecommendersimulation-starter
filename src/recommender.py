from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: float
    target_valence: float
    target_tempo: float

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def _score_song(self, user: UserProfile, song: Song) -> Tuple[float, List[str]]:
        """Returns (score, reasons) for a single song against a user profile."""
        reasons = []

        # Genre match (weight 0.35)
        if song.genre == user.favorite_genre:
            genre_score = 1.0
            reasons.append(f"Matches your favorite genre '{user.favorite_genre}' (+0.35)")
        else:
            genre_score = 0.0

        # Mood match (weight 0.25)
        if song.mood == user.favorite_mood:
            mood_score = 1.0
            reasons.append(f"Matches your preferred mood '{user.favorite_mood}' (+0.25)")
        else:
            mood_score = 0.0

        # Energy proximity (weight 0.20)
        energy_score = 1.0 - abs(song.energy - user.target_energy)
        reasons.append(
            f"Energy level {song.energy:.2f} is "
            f"{'close to' if energy_score >= 0.8 else 'somewhat near'} "
            f"your target {user.target_energy:.2f} (+{energy_score * 0.20:.2f})"
        )

        # Acoustic preference (weight 0.12)
        if (user.likes_acoustic and song.acousticness > 0.5) or \
           (not user.likes_acoustic and song.acousticness <= 0.5):
            acoustic_score = 1.0
            pref = "acoustic" if user.likes_acoustic else "non-acoustic"
            reasons.append(f"Fits your {pref} preference (acousticness {song.acousticness:.2f}) (+0.12)")
        else:
            acoustic_score = 0.0

        # Valence proximity (weight 0.08)
        valence_score = 1.0 - abs(song.valence - user.target_valence)
        reasons.append(
            f"Positivity/valence {song.valence:.2f} aligns with "
            f"your target {user.target_valence:.2f} (+{valence_score * 0.08:.2f})"
        )

        score = (genre_score    * 0.35
               + mood_score     * 0.25
               + energy_score   * 0.20
               + acoustic_score * 0.12
               + valence_score  * 0.08)

        return round(score, 4), reasons

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        scored = [
            (song, self._score_song(user, song)[0])
            for song in self.songs
        ]
        scored.sort(key=lambda x: x[1], reverse=True)
        return [song for song, _ in scored[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        score, reasons = self._score_song(user, song)
        lines = [f"Why '{song.title}' by {song.artist} was recommended (score: {score:.4f}):"]
        for i, reason in enumerate(reasons, 1):
            lines.append(f"  {i}. {reason}")
        return "\n".join(lines)

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    import csv
    print(f"Loading songs from {csv_path}...")
    songs = []
    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            songs.append({
                'id': int(row['id']),
                'title': row['title'],
                'artist': row['artist'],
                'genre': row['genre'],
                'mood': row['mood'],
                'energy': float(row['energy']),
                'tempo_bpm': float(row['tempo_bpm']),
                'valence': float(row['valence']),
                'danceability': float(row['danceability']),
                'acousticness': float(row['acousticness']),
            })
    return songs

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py

    Returns a list of (song_dict, score, explanation) tuples, sorted by score descending.
    """
    results = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        results.append((song, score, ", ".join(reasons)))
    results.sort(key=lambda x: x[1], reverse=True)
    return results[:k]

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences using the weighted formula:
        score = genre(0.35) + mood(0.25) + energy(0.20) + acoustic(0.12) + valence(0.08)

    Returns:
        (score, reasons) where reasons is a list of human-readable contribution strings.
    """
    reasons = []

    # Genre match (weight 0.35)
    if song['genre'] == user_prefs['favorite_genre']:
        genre_score = 1.0
        reasons.append(f"genre match (+{1.0 * 0.35:.2f})")
    else:
        genre_score = 0.0

    # Mood match (weight 0.25)
    if song['mood'] == user_prefs['favorite_mood']:
        mood_score = 1.0
        reasons.append(f"mood match (+{1.0 * 0.25:.2f})")
    else:
        mood_score = 0.0

    # Energy proximity (weight 0.20)
    energy_score = 1.0 - abs(song['energy'] - user_prefs['target_energy'])
    reasons.append(f"energy fit (+{energy_score * 0.20:.2f})")

    # Acoustic preference (weight 0.12)
    likes_acoustic = user_prefs.get('likes_acoustic', False)
    if (likes_acoustic and song['acousticness'] > 0.5) or \
       (not likes_acoustic and song['acousticness'] <= 0.5):
        acoustic_score = 1.0
        reasons.append(f"acoustic preference match (+{1.0 * 0.12:.2f})")
    else:
        acoustic_score = 0.0

    # Valence proximity (weight 0.08)
    valence_score = 1.0 - abs(song['valence'] - user_prefs['target_valence'])
    reasons.append(f"valence fit (+{valence_score * 0.08:.2f})")

    score = (genre_score    * 0.35
           + mood_score     * 0.25
           + energy_score   * 0.20
           + acoustic_score * 0.12
           + valence_score  * 0.08)

    return round(score, 4), reasons