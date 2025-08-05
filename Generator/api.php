<?php
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET');
header('Access-Control-Allow-Headers: Content-Type');

// Configuration
$atlas_folder = __DIR__ . '/output_atlases';
$json_file = $atlas_folder . '/atlas_data.json';

// Fonction pour charger les données JSON
function loadAtlasData($json_file) {
    if (!file_exists($json_file)) {
        http_response_code(404);
        echo json_encode(['error' => 'Atlas data not found']);
        exit;
    }
    
    $json_content = file_get_contents($json_file);
    $data = json_decode($json_content, true);
    
    if ($data === null) {
        http_response_code(500);
        echo json_encode(['error' => 'Invalid JSON data']);
        exit;
    }

    return $data;
}

// Fonction pour compresser les données JSON (remplacer les clés string par des index)
function compressAtlasData($data) {
    $compressed_data = [
        'mapping' => [],
        'atlases' => []
    ];
    
    // Créer un mapping des noms d'images vers des index basé sur l'ordre des métadonnées
    $image_name_to_index = [];
    $image_index = 0;

    // Utiliser l'ordre des métadonnées pour déterminer les index
    foreach ($data['metadata'] as $image_name => $metadata) {
        $image_name_to_index[$image_name] = $image_index;
        $compressed_data['mapping'][$image_index] = $metadata;
        $image_index++;
    }

    // Compresser les atlas
    foreach ($data['atlases'] as $atlas) {
        $compressed_atlas = [
            'scale' => $atlas['scale'],
            'width' => $atlas['width'],
            'height' => $atlas['height'],
            'uv' => (object)[] // Forcer à être un objet/dictionnaire
        ];

        // Remplacer les clés string par des index numériques
        foreach ($atlas['uv'] as $image_name => $uv) {
            $index = $image_name_to_index[$image_name];
            $compressed_atlas['uv']->$index = $uv;
        }

        $compressed_data['atlases'][] = $compressed_atlas;
    }
    
    return $compressed_data;
}

// Fonction pour obtenir le type MIME basé sur l'extension
function getMimeType($file_path) {
    $extension = strtolower(pathinfo($file_path, PATHINFO_EXTENSION));
    
    $mime_types = [
        'png' => 'image/png',
        'jpg' => 'image/jpeg',
        'jpeg' => 'image/jpeg',
        'gif' => 'image/gif',
        'bmp' => 'image/bmp',
        'webp' => 'image/webp',
        'tiff' => 'image/tiff',
        'tif' => 'image/tiff',
        'svg' => 'image/svg+xml'
    ];
    
    return isset($mime_types[$extension]) ? $mime_types[$extension] : 'application/octet-stream';
}

// Fonction pour servir une image
function serveImage($file_path) {
    if (!file_exists($file_path)) {
        http_response_code(404);
        echo json_encode(['error' => 'Image not found']);
        exit;
    }
    
    $mime_type = getMimeType($file_path);
    header('Content-Type: ' . $mime_type);
    header('Content-Length: ' . filesize($file_path));
    header('Cache-Control: public, max-age=86400'); // Cache 1 jour
    
    readfile($file_path);
    exit;
}

// Router simple
$request_uri = $_SERVER['REQUEST_URI'];
$path = parse_url($request_uri, PHP_URL_PATH);

// Route: GET /atlas - Retourne le fichier JSON complet compressé
if ($path === '/atlas.json') {
    $data = loadAtlasData($json_file);
    $compressed_data = compressAtlasData($data);
    echo json_encode($compressed_data, JSON_PRETTY_PRINT);
    exit;
}

// Route: GET /atlas/{index} - Retourne l'image de l'atlas contenant l'image à l'index donné (basé sur les métadonnées)
if (preg_match('/^\/atlas\/(\d+).png$/', $path, $matches)) {
    $requested_index = intval($matches[1]);
    $data = loadAtlasData($json_file);
    
    $atlas = $data['atlases'];
    
    if (!isset($atlas[$requested_index])) {
        http_response_code(404);
        echo json_encode(['error' => "Atlas with index $requested_index not found"]);
        exit;
    }
    
    $found_atlas = $atlas[$requested_index];
    
    if ($found_atlas === null) {
        http_response_code(404);
        echo json_encode(['error' => "Atlas containing image with index $requested_index not found"]);
        exit;
    }
    
    // Servir l'image de l'atlas
    $image_path = $atlas_folder . '/' . $found_atlas['file'];
    serveImage($image_path);
}

// Route par défaut - Documentation de l'API
http_response_code(404);
echo json_encode([
    'error' => 'Route not found',
    'available_routes' => [
        'GET /atlas.json' => 'Retourne le fichier JSON complet des atlas',
        'GET /atlas/{index}.png' => 'Retourne l\'image de l\'atlas à l\'index donné'
    ],
    'examples' => [
        '/atlas.json' => 'Données JSON complètes',
        '/atlas/0.png' => 'Premier atlas (index 0)',
        '/atlas/1.png' => 'Deuxième atlas (index 1)'
    ]
], JSON_PRETTY_PRINT);
?>
