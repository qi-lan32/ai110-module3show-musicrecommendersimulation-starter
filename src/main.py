"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs


PROFILES = {
    "Default": {
        # Common user profile test
        "favorite_genre": "pop",
        "favorite_mood":  "happy",
        "target_energy":  0.66,
        "likes_acoustic": 0.6,
        "target_valence": 0.45,
        "target_tempo":   85,
    },

    "Contradictory (High Energy + Sad Mood)": {
        # Tests: mood preference conflicts with energy target.
        # Only 1 sad song (Mississippi Tears, energy 0.44) — recommender
        # should pick it for mood but its energy penalty may push it down.
        "favorite_genre": "blues",
        "favorite_mood":  "sad",
        "target_energy":  0.90,      # conflicts: high energy for sad song
        "likes_acoustic": 0.0,
        "target_valence": 0.25,
        "target_tempo":   100,
    },

    "Acoustic Float Bug Probe": {
        # Tests: likes_acoustic=0.1 should differ from 0.9 but doesn't —
        # both are truthy, both score identical +0.12. Bug surface test.
        "favorite_genre": "folk",
        "favorite_mood":  "melancholic",
        "target_energy":  0.35,
        "likes_acoustic": 0.1,      
        "target_valence": 0.40,
        "target_tempo":   76,
    },

    "Nonexisting Genre": {
        # Tests: genre+mood combo doesn't exist in catalog (country/romantic).
        # Forces the recommender to rank purely on energy/acoustic/valence.
        # Validates that non-matching songs are still meaningfully ranked.
        "favorite_genre": "country",
        "favorite_mood":  "romantic",  # no country+romantic song exists
        "target_energy":  0.50,
        "likes_acoustic": 0.8,
        "target_valence": 0.75,
        "target_tempo":   90,
    },

}


def main() -> None:
    songs = load_songs("../data/songs.csv")

    for profile_name, user_prefs in PROFILES.items():
        recommendations = recommend_songs(user_prefs, songs, k=5)

        width = 60
        print("\n" + "=" * width)
        print(f" PROFILE: {profile_name}".center(width))
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
