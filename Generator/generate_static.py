#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour générer une version statique des atlas
Copie les images avec un renommage par index et génère un JSON équivalent à l'API /atlas
"""

import json
import os
import shutil
from pathlib import Path


def compress_atlas_data(data):
    """
    Compresse les données JSON (remplace les clés string par des index)
    Équivalent de la fonction PHP compressAtlasData
    """
    compressed_data = {
        'mapping': [],
        'atlases': []
    }
    
    # Créer un mapping des noms d'images vers des index basé sur l'ordre des métadonnées
    image_name_to_index = {}
    image_index = 0

    # Utiliser l'ordre des métadonnées pour déterminer les index
    for image_name, metadata in data['metadata'].items():
        image_name_to_index[image_name] = image_index
        compressed_data['mapping'].append(metadata)
        image_index += 1

    # Compresser les atlas
    for atlas in data['atlases']:
        compressed_atlas = {
            'scale': atlas['scale'],
            'width': atlas['width'],
            'height': atlas['height'],
            'uv': {}
        }

        # Remplacer les clés string par des index numériques
        for image_name, uv in atlas['uv'].items():
            index = image_name_to_index[image_name]
            compressed_atlas['uv'][str(index)] = uv

        compressed_data['atlases'].append(compressed_atlas)
    
    return compressed_data


def copy_and_rename_images(atlas_folder, output_static_folder, atlas_data):
    """
    Copie les images des atlas en les renommant avec leur index
    """
    images_folder = output_static_folder / 'atlas'
    images_folder.mkdir(exist_ok=True)
    
    copied_files = []
    
    for index, atlas in enumerate(atlas_data['atlases']):
        if 'file' in atlas:
            source_file = atlas_folder / atlas['file']
            if source_file.exists():
                # Obtenir l'extension du fichier original
                extension = source_file.suffix
                # Nouveau nom avec l'index
                new_filename = f"{index}{extension}"
                destination_file = images_folder / new_filename
                
                # Copier le fichier
                shutil.copy2(source_file, destination_file)
                copied_files.append({
                    'original': atlas['file'],
                    'new': new_filename,
                    'index': index
                })
                print(f"Copié: {atlas['file']} -> {new_filename}")
            else:
                print(f"Attention: Fichier non trouvé: {source_file}")
    
    return copied_files


def generate_static_version():
    """
    Fonction principale pour générer la version statique
    """
    # Demander le dossier d'entrée
    input_path = input("Dossier des atlas d'entrée (par défaut: 'output_atlases'):  ").strip()
    if not input_path:
        # Utiliser le dossier par défaut
        script_dir = Path(__file__).parent
        atlas_folder = script_dir / 'output_atlases'
        print(f"Utilisation du dossier par défaut: {atlas_folder}")
    else:
        atlas_folder = Path(input_path)
    
    # Vérifier que le dossier d'entrée existe
    if not atlas_folder.exists():
        print(f"Erreur: Le dossier d'entrée {atlas_folder} n'existe pas")
        return
    
    json_file = atlas_folder / 'atlas_data.json'
    if not json_file.exists():
        print(f"Erreur: Le fichier {json_file} n'existe pas")
        print("Assurez-vous que le dossier contient le fichier atlas_data.json")
        return
    
    # Demander le dossier de sortie
    output_path = input("Dossier de sortie (par défaut: 'output_static'): ").strip()
    if not output_path:
        # Utiliser le dossier par défaut
        output_static_folder = Path('output_static')
        print(f"Utilisation du dossier de sortie par défaut: {output_static_folder}")
    else:
        output_static_folder = Path(output_path)
    output_static_folder.mkdir(exist_ok=True)
    print(f"Dossier de sortie: {output_static_folder}")
    
    # Charger les données JSON
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            atlas_data = json.load(f)
        print(f"Données JSON chargées depuis: {json_file}")
    except Exception as e:
        print(f"Erreur lors du chargement du JSON: {e}")
        return
    
    # Compresser les données (comme fait l'API PHP)
    compressed_data = compress_atlas_data(atlas_data)
    
    # Sauvegarder le JSON compressé (équivalent de la réponse /atlas)
    atlas_json_file = output_static_folder / 'atlas.json'
    try:
        with open(atlas_json_file, 'w', encoding='utf-8') as f:
            json.dump(compressed_data, f, indent=2, ensure_ascii=False)
        print(f"JSON compressé sauvegardé: {atlas_json_file}")
    except Exception as e:
        print(f"Erreur lors de la sauvegarde du JSON: {e}")
        return
    
    # Copier et renommer les images
    copied_files = copy_and_rename_images(atlas_folder, output_static_folder, atlas_data)
    
    print(f"\n✅ Version statique générée avec succès dans: {output_static_folder}")
    print(f"📁 Fichiers générés:")
    print(f"   - atlas.json (équivalent de l'API /atlas)")
    print(f"   - atlas/ (images renommées par index)")
    print(f"\n📊 Statistiques:")
    print(f"   - {len(copied_files)} images copiées")
    print(f"   - {len(compressed_data['atlases'])} atlas")
    print(f"   - {len(compressed_data['mapping'])} images dans le mapping")


if __name__ == '__main__':
    generate_static_version()
