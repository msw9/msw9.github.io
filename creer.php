<?php
$nom=$prenom="";
$nom=$_POST["nom"];
$prenom=$_POST["prenom"];
if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    // Path to the existing image on the server
    $baseImagePath = 'images/carte_orange.png';
    
    // Check if the file was uploaded without errors
    if (isset($_FILES['userImage']) && $_FILES['userImage']['error'] == 0) {
        // Load the existing image
        $baseImage = imagecreatefrompng(filename: $baseImagePath);
        
        // Load the uploaded image
        $uploadedImage = imagecreatefrompng($_FILES['userImage']['tmp_name']);
        
        // Define the position where the uploaded image will be pasted
        $x = 15; // X position
        $y = 150; // Y position
        
        // Paste the uploaded image onto the existing image
        imagecopy($baseImage, $uploadedImage, $x, $y, 0, 0, imagesx($uploadedImage), imagesy($uploadedImage));
        
        // Set the content type header
        header('Content-Type: image/png');
        
        // Output the final image
        imagejpeg($baseImage);
        
        // Free up memory
        imagedestroy($baseImage);
        imagedestroy($uploadedImage);
    } else {
        echo "Error uploading the image.";
    }
    // Save the final image to a file
    $finalImagePath = 'download/final_image.jpg';
    imagejpeg($baseImage, $finalImagePath);

    // Provide a download link
    //echo "<a href='$finalImagePath'>Download Edited Image</a>";
}
?>