# emotion-data-fusion
Bridging the gap between RAVDESS and ASVP-ESD datasets for advanced emotion analysis.

# RAVDESS-ASVP-ESD Audio Dataset Merger

This repository hosts a Python script developed to merge two distinct audio datasets, namely RAVDESS and ASVP-ESD. These datasets, while both valuable for emotion recognition tasks, employ different file and folder naming conventions. The provided script effectively renames and restructures the ASVP-ESD files to align with the RAVDESS format, ensuring the preservation of the additional information unique to the ASVP-ESD dataset.

## Datasets Overview

RAVDESS and ASVP-ESD are popular audio datasets utilized in emotion recognition research. However, their distinct naming conventions and folder structures present challenges when attempting to combine them. RAVDESS employs a 7-part numerical identifier, while ASVP-ESD uses a more complex system with up to a 10-part identifier. Each segment of these identifiers represents different characteristics, including modality, vocal channel, emotion, intensity, statement, repetition, actor, and in the case of ASVP-ESD, additional information such as age, source, language, and recording quality.

## Methodology

The primary objective was to adapt the ASVP-ESD files to be compatible with the RAVDESS format, without discarding the extra information that ASVP-ESD provides. The following steps were taken to achieve this:

1. **Emotion Mapping:** A mapping was created to align the emotion codes of the two datasets. Some emotions in ASVP-ESD were mapped to their closest equivalent in RAVDESS, while others were assigned to a new category.

2. **Vocal Channel Adjustment:** A new category was defined for non-speech data in ASVP-ESD to ensure compatibility with RAVDESS.

3. **Statement Code Renaming:** Statement codes in both datasets were adjusted to prevent conflicts. The range 0 to 999 was reserved for ASVP-ESD and 1001 and 1002 for RAVDESS.

4. **Actor Code Renaming:** The script keeps track of the maximum actor number in RAVDESS and begins renaming ASVP-ESD actor codes from this number plus one, adhering to the gender logic (odd-numbered actors are male, even-numbered actors are female).

5. **Recording Quality Indication:** A code was appended at the end of each filename to indicate the recording quality. For RAVDESS, a clean/no-noise recording was assumed. For ASVP-ESD, the provided codes (66 for mixed voices, 77 for high noise environment) were used.

6. **Folder Structure Alignment:** The decision was made to adhere to the RAVDESS folder structure and modify the ASVP-ESD structure accordingly. The baby sounds from the "Bonus" folder in ASVP-ESD were excluded as they might affect the emotion recognition results.

## Usage

The script can be executed from the command line with the following command:

- To perform both restructuring and cleanup: `python emomerger.py /path/to/your/directory --merge`

Where `/path/to/your/directory` is the folder where you have both datasets.

If you have some tasks to complete before the cleanup, you can simply merge by executing these commands one by one:
- `python emomerger.py /path/to/your/directory --restructure`
- `python emomerger.py /path/to/your/directory --cleanup`

## Licensing

The RAVDESS dataset is released under a Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License. The ASVP-ESD dataset's licensing terms should be checked with the dataset provider. 

As for the script provided in this repository, it is licensed under the MIT License. However, please note that while the script itself is licensed under MIT, the datasets it operates on may have their own licenses that you need to comply with. Always ensure you are in compliance with the licensing terms of all datasets you use.

## Conclusion

The developed solution facilitates the merging of the two datasets while preserving as much information as possible from the ASVP-ESD dataset, and ensuring compatibility with the RAVDESS format. This is crucial for machine learning tasks that require a large and diverse dataset for training, thereby enhancing the robustness and accuracy of emotion recognition models.
