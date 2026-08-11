# Panorama Pro

Instagram panoramic carousel slicer for **Pythonista 3** on iPhone.

Load any photo, rotate it freely, then crop and export exactly **two 4:5
frames** (1080 x 1350 px each) that form a seamless panoramic carousel when
posted to Instagram.

## Features

- **Two-finger rotation** — place two fingers on the canvas and twist to
  rotate to any angle. A +90° button and Reset are also provided.
- **Interactive crop frame** — drag with one finger to reposition, pinch
  with two fingers to resize. The frame always maintains a 2 × 4:5 ratio.
- **Instant preview** — swipeable carousel shows both slices before saving.
- **Format preservation** — detects the original format (HEIC, JPEG, PNG)
  and saves in the same format. Falls back to JPEG if HEIC writing is
  unavailable.
- **Original filename** — saved files are named
  `{original_name}_car_1.{ext}` and `{original_name}_car_2.{ext}`.

## Requirements

| Dependency | Bundled with Pythonista 3? |
|------------|---------------------------|
| `ui`       | Yes                       |
| `photos`   | Yes                       |
| `console`  | Yes                       |
| `PIL`      | Yes (Pillow)              |
| `pillow_heif` | No — optional, for HEIC export |

## Workflow

```
┌─────────────────────────────────────┐
│  1. EDIT MODE                       │
│     • Tap Load to pick a photo      │
│     • Two-finger rotate or +90°     │
│     • Tap Crop >> when ready        │
├─────────────────────────────────────┤
│  2. CROP MODE                       │
│     • Drag the frame to position    │
│     • Pinch to resize               │
│     • Tap Slice to generate frames  │
│     • Tap Save to export            │
│     • Tap << Back to re-edit        │
└─────────────────────────────────────┘
```

## Usage

Open `app.py` in Pythonista 3 and tap **Run** (▶).

The app presents full-screen. All interaction is touch-based — no
external keyboards or accessories required.

## Project structure

```
pan_splitter/
├── app.py      # main application
├── app.pyui    # Pythonista UI descriptor (launch config)
└── README.md   # this file
```

## Output

Each slice is resized to **1080 × 1350 px** (Instagram's recommended 4:5
resolution). Post both images as a carousel in order — followers swipe to
see the full panorama.

## License

Personal use. No warranty.
