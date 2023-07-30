"""
Author: Juan Sugg <juanpedrosugg@gmail.com>
Date: 2023-07-29
Description: This script merges the RAVDESS and ASVP-ESD audio datasets, renaming and restructuring the ASVP-ESD files to align with the RAVDESS format, while preserving the additional information unique to the ASVP-ESD dataset.
License: This script is released under the MIT License. See the LICENSE file in the project root for more information.
"""

import os
import shutil
import argparse
from typing import Dict


def rename_files(directory: str) -> None:
    # Emotion mapping from ASVP-ESD to RAVDESS
    emotion_mapping: Dict[str, str] = {
        '01': '01',  # Boredom, sigh -> Neutral
        '02': '02',  # Neutral, calm -> Calm
        '03': '03',  # Happy, laugh, gaggle -> Happy
        '04': '04',  # Sad, cry -> Sad
        '05': '05',  # Angry, grunt, frustration -> Angry
        '06': '06',  # Fearful, scream, panic -> Fearful
        '07': '07',  # Disgust, dislike, contempt -> Disgust
        '08': '08',  # Surprised, gasp, amazed -> Surprised
        '09': '03',  # Excited -> Happy
        '10': '03',  # Pleasure -> Happy
        '11': '04',  # Pain, groan -> Sad
        '12': '04',  # Disappointment, disapproval -> Sad
        '13': '01'   # Breath -> Neutral
    }

    # Vocal channel mapping from ASVP-ESD to RAVDESS
    vocal_channel_mapping: Dict[str, str] = {
        '01': '01',  # Speech -> Speech
        '02': '03'   # Non-speech -> Non-speech (new category)
    }

    # Emotion subcategory mapping for ASVP-ESD
    emotion_subcategory_mapping: Dict[str, str] = {
        '13': '01',  # Laugh
        '23': '02',  # Gaggle
        '33': '03',  # Other happiness
        '14': '04',  # Cry
        '24': '05',  # Sigh
        '34': '06',  # Sniffle
        '44': '07',  # Suffering
        '16': '08',  # Scream
        '36': '09',  # Panic
        '15': '10',  # Rage
        '25': '11',  # Frustration
        '35': '12',  # Other anger
        '18': '13',  # Surprised
        '28': '14',  # Amazed
        '38': '15',  # Astonishment
        '48': '16',  # Other surprise
        '17': '17',  # Disgust
        '27': '18',  # Rejection
        '00': '00'   # Default for RAVDESS
    }

    # Keep track of the maximum actor number in RAVDESS
    max_actor_ravdess: int = 24

    # Keep track of the last male and female actors in ASVP-ESD
    last_male_actor_asvp: int = 0
    last_female_actor_asvp: int = 0

    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename.endswith(".wav"):
                parts = filename.split("-")
                # RAVDESS parts
                modality: str = parts[0]
                vocal_channel: str = vocal_channel_mapping[parts[1]]  # Map vocal channel to RAVDESS
                emotion: str = parts[2]  # Keep RAVDESS emotion code
                intensity: str = parts[3]
                statement: str = parts[4]
                actor: str = parts[5]
                # Check if it's a RAVDESS file (7 parts) or ASVP-ESD file (9 or 10 parts)
                if len(parts) == 7:
                    repetition: str = '01'  # Adding repetition value
                    language: str = '02'  # English language code in ASVP-ESD
                    # Adjust statement code for RAVDESS
                    statement = str(int(statement) + 1000)
                    recording_quality: str = '00'  # Clean/no-noise recording for RAVDESS
                    emotion_subcategory: str = '00'  # Default for RAVDESS
                    new_filename: str = f"{modality}-{vocal_channel}-{emotion}-{intensity}-{statement}-{repetition}-{actor}-{language}-{emotion_subcategory}-{recording_quality}.wav"
                else:  # ASVP-ESD file
                    repetition: str = '01'  # Adding repetition value
                    # ASVP-ESD extra parts
                    language: str = parts[8]
                    # Check if the file ends with '66' or '77'
                    if len(parts) > 9 and parts[9] in ['66', '77']:
                        recording_quality: str = parts[9]
                    else:
                        recording_quality: str = '00'  # Clean/no-noise
                    # Adjust emotion code for ASVP-ESD
                    emotion: str = emotion_mapping[parts[2]]  # Map emotion to RAVDESS
                    # Adjust actor code for ASVP-ESD
                    actor_asvp: int = int(parts[6]) + max_actor_ravdess
                    if actor_asvp % 2 == 0:  # Even, male
                        if actor_asvp - 1 != last_male_actor_asvp:
                            actor_asvp = last_male_actor_asvp + 1
                        last_male_actor_asvp = actor_asvp
                    else:  # Odd, female
                        if actor_asvp - 1 != last_female_actor_asvp:
                            actor_asvp = last_female_actor_asvp + 1
                        last_female_actor_asvp = actor_asvp
                    actor: str = str(actor_asvp)
                    # Adjust statement code for ASVP-ESD
                    statement: str = str(int(statement) + 1000)
                    # Get emotion subcategory for ASVP-ESD
                    emotion_subcategory: str = emotion_subcategory_mapping[parts[7]] if len(parts) > 7 else '00'
                    new_filename: str = f"{modality}-{vocal_channel}-{emotion}-{intensity}-{statement}-{repetition}-{actor}-{language}-{emotion_subcategory}-{recording_quality}.wav"
                # Rename file
                old_path: str = os.path.join(root, filename)
                new_path: str = os.path.join(directory, "Actor_" + actor.zfill(2), new_filename)
                os.makedirs(os.path.dirname(new_path), exist_ok=True)
                shutil.move(old_path, new_path)


def remove_empty_folders(directory: str) -> None:
    for root, dirs, _ in os.walk(directory):
        for dir in dirs:
            full_dir: str = os.path.join(root, dir)
            if not os.listdir(full_dir):
                os.rmdir(full_dir)


def main() -> None:
    parser = argparse.ArgumentParser(description='Rename and restructure audio files from RAVDESS and ASVP-ESD datasets.')
    parser.add_argument('directory', type=str, help='The directory containing the audio files.')
    parser.add_argument('--merge', action='store_true', help='Rename, restructure and remove empty directories.')
    parser.add_argument('--restructure', action='store_true', help='Rename and restructure the audio files.')
    parser.add_argument('--cleanup', action='store_true', help='Remove empty directories after restructuring.')
    args = parser.parse_args()

    if args.merge:
        rename_files(args.directory)
        remove_empty_folders(args.directory)
    if args.restructure:
        rename_files(args.directory)
    if args.cleanup:
        remove_empty_folders(args.directory)


if __name__ == "__main__":
    main()
