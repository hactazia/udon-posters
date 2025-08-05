import os
import json
from PIL import Image

def main():
    """Fonction principale"""
    # Configuration
    input_folder = input("Dossier des images d'entrée (par défaut: 'input_images'): ").strip()
    if not input_folder:
        input_folder = "input_images"
    
    if not os.path.exists(input_folder):
        print(f"Le dossier {input_folder} n'existe pas.")
        return
        
    # Vérifier qu'il existe un fichier metadata.json
    metadata = {}
    metadata_file = f"{input_folder}/metadata.json"
    try:
        with open(metadata_file, 'r', encoding='utf-8') as file:
            metadata = json.load(file)
            print(f"Métadonnées existantes chargées depuis {metadata_file}")
    except FileNotFoundError:
        print(f"Le fichier {metadata_file} n'existe pas. Création d'un nouveau fichier de métadonnées.")
    except json.JSONDecodeError:
        print(f"Le fichier {metadata_file} n'est pas un JSON valide. Création d'un nouveau fichier.")
    
    # Extensions d'images supportées
    supported_extensions = {'.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.tif', '.webp', '.gif'}
    
    # Parcourir toutes les images dans le dossier
    image_files = []
    for filename in sorted(os.listdir(input_folder)):
        if os.path.isfile(os.path.join(input_folder, filename)):
            _, ext = os.path.splitext(filename.lower())
            if ext in supported_extensions:
                image_files.append(filename)
    
    if not image_files:
        print(f"Aucune image trouvée dans le dossier {input_folder}")
        return
    
    print(f"\nImages trouvées: {len(image_files)}")
    print("="*60)
    
    # Traiter chaque image automatiquement
    new_entries = 0
    updated_entries = 0
    
    for filename in image_files:
        # Créer ou mettre à jour l'entrée avec des valeurs vides par défaut
        if filename not in metadata:
            metadata[filename] = {
                "title": "",
                "url": ""
            }
            new_entries += 1
            print(f"✓ Nouvelle entrée créée pour: {filename}")
        else:
            # Vérifier si les champs existent et les créer s'ils sont manquants
            if "title" not in metadata[filename]:
                metadata[filename]["title"] = ""
                updated_entries += 1
            if "url" not in metadata[filename]:
                metadata[filename]["url"] = ""
                updated_entries += 1
            
            if updated_entries > 0:
                print(f"✓ Entrée mise à jour pour: {filename}")
    
    # Sauvegarder le fichier JSON
    try:
        # Trier les métadonnées par nom de clé
        sorted_metadata = dict(sorted(metadata.items()))
        
        with open(metadata_file, 'w', encoding='utf-8') as file:
            json.dump(sorted_metadata, file, indent=2, ensure_ascii=False)
        print(f"\n✓ Métadonnées sauvegardées dans {metadata_file}")
        
        # Afficher un résumé
        total_images = len(metadata)
        
        print(f"\nRÉSUMÉ:")
        print(f"  Total d'images: {total_images}")
        print(f"  Nouvelles entrées créées: {new_entries}")
        
    except Exception as e:
        print(f"Erreur lors de la sauvegarde: {e}")

if __name__ == "__main__":
    main()
