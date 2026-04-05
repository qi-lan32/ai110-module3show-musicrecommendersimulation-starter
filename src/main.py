"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("../data/songs.csv") 

    # Taste profile — defines what the recommender scores songs against
    user_prefs = {
        "favorite_genre": "pop",      # categorical: boosts songs whose genre matches
        "favorite_mood":  "chill",    # categorical: boosts songs whose mood matches
        "target_energy":  0.66,       # float 0–1: penalizes songs far from this energy level
        "likes_acoustic": 0.6,       # bool: gives a bonus to high-acousticness songs
        "target_valence": 0.45,   # chill ≠ sad; anchors the mood numerically
        "target_tempo": 85,     # strongly separates lofi (75) from rock (140)
    }

    recommendations = recommend_songs(user_prefs, songs, k=5)

    width = 60
    print("\n" + "=" * width)
    print(" MUSIC RECOMMENDATIONS".center(width))
    print("=" * width)

    for rank, (song, score, explanation) in enumerate(recommendations, 1):
        print(f"\n  #{rank}  {song['title']}  —  {song['artist']}")
        print(f"       {song['genre'].upper()} | {song['mood']} | {song['tempo_bpm']:.0f} BPM")
        print(f"       Score: {score:.4f}  {'█' * int(score * 20):<20} {score * 100:.1f}%")
        print(f"       Why this song:")
        for reason in explanation.split(", "):
            print(f"         • {reason}")
        print("  " + "-" * (width - 2))

    print("=" * width + "\n")

if __name__ == "__main__":
    main()
