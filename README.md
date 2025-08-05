# Hactazia's Posters for Udon VRChat

A package for managing dynamic poster displays in VRChat worlds using Udon Sharp. This system allows you to display and update posters dynamically by loading images from external sources, with support for texture atlases and automated content management.

## Requirements

- Unity 2022.3 or later
- VRChat SDK3 (Udon)
- UdonSharp

### For the server-side features:
- PHP 8.4 or later
- Python 3.13 or later

## Installation

### Unity Package Manager (UPM)
Add the package using Unity Package Manager with the Git URL:
```
https://github.com/hactazia/udon-posters.git
```

1. Open Unity Package Manager (`Window > Package Manager`)
2. Click the `+` button and select `Add package from git URL...`
3. Enter the URL above and click `Add`

### VRChat Package Manager (VPM)
Check the VPM repository for the latest version:

[https://vpm.hactazia.fr/](https://vpm.hactazia.fr/)

Add the package using [VRChat Creator Companion](https://vcc.docs.vrchat.com/):

[https://vpm.hactazia.fr/index.json](https://vpm.hactazia.fr/index.json)

1. Open VRChat Creator Companion
2. Go to `Settings > Packages`
3. Add the repository URL above
4. Install "Hactazia - Posters" from the available packages

## Setup Guide

### 1. Basic Setup

1. **Add PosterManager to Scene**:
   - Drag `Prefab/Manager.prefab` into your scene
   - Configure the `metaUrl` to point to your metadata JSON
   - Set up `atlasUrls` array with your texture atlas URLs

2. **Configure Individual Posters**:
> Note: The order of posters in the array should match the metadata indices.
   - Add `Prefab/Poster.prefab` instances to your scene
   - Assign them to the `posters` array in PosterManager
   - Optionally: Set up click interactions and animations

### 2. Server Setup (Optional)

If you want to use the dynamic generation features:

1. **Go to the `Generator/` folder**:
   - This contains Python scripts for generating metadata and atlases.

2. **Install Python Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Prepare Input Images**:
   - Place your images in `Generator/input_images/`
   - Run `make_metadata.py` to generate metadata
   - You can add additional properties like titles and redirect URLs in the metadata JSON. If you change the order of metadata, it changes the index of the posters, so be careful with that.
   - Run `generate_posters.py` to create atlases. If you have many images, it is possible it may take a long time to generate the atlases, so be patient.

4. **Deploy Web Server**:
    - Production:
        - Copy the `api.php` file to your web server
        - Ensure PHP is available for the API
        - Update URLs in your Unity setup
    - Local Testing:
        - Use the `start_server.bat` or `start_server.sh` script to run a local server for testing purposes. This will serve the metadata and atlas images from your local machine. You need to run the script in the folder where your `output_atlases` are located.

## Core Components

### PosterManager
The main controller that handles:
- Metadata loading from external sources
- Atlas image downloading
- Poster synchronization and updates
- Error handling and fallbacks

### Poster
Individual poster displays that support:
- Dynamic texture assignment
- Aspect ratio adjustment
- Click interactions
- State animations (Loading, Display, Error)
- VRChat Store and Avatar integration

### Generator Tools
Python-based utilities for:
- **`make_metadata.py`**: Generates JSON metadata for poster configurations.
  This is used to define poster properties and atlas mappings like title and redirect URLs.
- **`generate_posters.py`**: Creates optimized texture atlases from input images.
- **`api.php`**: Web API for serving atlas data and images.

### 3. Configuration

**In Metadata JSON**:
The order of entries in the metadata JSON should match the order of posters in the `posters` array. Each entry should include:
- **title**: Display name for the poster
- **url**: Redirect URL

**Redirect URL Formats**:
- VRChat Store Groups: `grp_[group_id]#store`
- VRChat Products: `prod_[product_id]`
- Avatar Listings: `avtr_[avatar_id]#listing`
- Avatar Pedestals: `avtr_[avatar_id]`

## Troubleshooting

### Common Issues

1. **Images Not Loading**:
   - Check URL accessibility
   - Verify CORS headers on your server
   - Ensure image formats are supported (PNG, JPG)

2. **Metadata Errors**:
   - Validate JSON format
   - Check array indices match available atlases

## Contributing

Contributions are welcome! Please follow the existing code style and include appropriate documentation for new features.

## Credits

### Icons
This package uses icons from [Google Fonts Icons](https://fonts.google.com/icons?icon.style=Rounded&icon.size=512&icon.color=%23ffffff) with the Rounded style.
